import itertools
import logging
from collections import defaultdict
from collections.abc import Collection, Iterable, Iterator, Sequence

from pyasn1.codec.der.encoder import encode as der_encode
from pyasn1_modules.rfc5280 import AuthorityKeyIdentifier, Certificate, SubjectKeyIdentifier

import siotls.trust
from siotls import TLSErrorGroup
from siotls.connection import TLSConnection
from siotls.contents import alerts
from siotls.contents.handshakes.certificate import X509Entry
from siotls.crypto import SignatureVerifyError
from siotls.iana import CertificateStatusType, ExtensionType
from siotls.verify import is_signature_valid, load_verify_ocsp, verify_signature
from siotls.x509 import certlib
from siotls.x509.cabforum import BaselineRequirementsError, verify_certificate_fullchain
from siotls.x509.load import DerCertificate, load_der_certificate
from siotls.x509.oid import ExtensionOID
from siotls.x509.pem import pem_encode

logger = logging.getLogger(__name__)


class X509Verifier(siotls.trust.X509Verifier):
    def __init__(
        self,
        der_ca_certificates: Collection[DerCertificate],
        network_service: siotls.trust.net.NetworkService | None,
    ):
        self.network_service = network_service
        self._many_ca_by_name = defaultdict(set)
        self._many_ca_by_ski = defaultdict(set)

        logger.debug('indexing %s ca certificates...', len(der_ca_certificates))
        for ca_der in der_ca_certificates:
            ca_cert = load_der_certificate(ca_der)
            subject = certlib.subject(ca_cert)
            self._many_ca_by_name[subject].add(ca_der)
            if len(self._many_ca_by_name[subject]) > 1:
                m =("Found multiple different CA certificates with the "
                    "same name: %s\n%s")
                logger.debug(m, '\n'.join(
                    pem_encode(cert_der, 'CERTIFICATE').decode()
                    for cert_der in self._many_ca_by_name[subject]
                ))

            if ski_ext := certlib.get_extension(
                ca_cert,
                ExtensionOID.SUBJECT_KEY_IDENTIFIER,
                SubjectKeyIdentifier,
                missing_ok=True
            ):
                self._many_ca_by_ski[ski_ext].add(ca_der)
                if len(self._many_ca_by_ski[ski_ext]) > 1:
                    m =("Found multiple different CA certificates with "
                        "the same SKI: %s\n%s")
                    logger.debug(m, '\n'.join(
                        pem_encode(cert_der, 'CERTIFICATE').decode()
                        for cert_der in self._many_ca_by_ski[subject]
                    ))
        logger.debug('done indexing')

    def is_trusted(self, certificate: Certificate):
        """
        Whether the given certificate is one of the trusted CA
        certificates.
        """
        if ski_ext := certlib.get_extension(
            certificate,
            ExtensionOID.SUBJECT_KEY_IDENTIFIER,
            SubjectKeyIdentifier,
            missing_ok=True
        ):
            return ski_ext in self._many_ca_by_ski
        return certlib.subject(certificate) in self._many_ca_by_name

    def find_issuer(self, subject: Certificate) -> Certificate | None:
        """
        Find the issuer CA certificate that signed the given subject
        certificate. Or ``None`` in no such issuer is found inside the
        trust store.

        When the subject certificate has a Authority Key Information
        (AKI) extension, the issuer is searched based on its Subject Key
        Information (SKI) extension only. In case several issuers match,
        the one with the most recent issued date (notBefore) is
        returned. An error is raised if an issuer match but fails to
        verify the signature.

        When the subject certificate lacks a Authority Key Information
        (AKI) extension, the issuer is seached based on its name. In
        case several issuers match, the one with the most recent issued
        date (notBefore) one capable of verifying the signature is
        returned. No certificate is returned in all issuers fail to
        verify the signature.
        """
        aki_ext = certlib.get_extension(
            subject,
            ExtensionOID.AUTHORITY_KEY_IDENTIFIER,
            AuthorityKeyIdentifier(),
            missing_ok=True,
        )
        if aki_ext:
            issuer = self._find_issuer_by_ski(aki_ext['keyIdentifier'].asOctets())
            if not issuer:
                return None
            verify_signature(subject, issuer)
            return issuer

        return next((
            issuer
            for issuer
            in self._find_issuers_by_name(certlib.issuer(subject))
            if is_signature_valid(subject, issuer)
        ), None)

    def _find_issuers_by_name(self, name: bytes) -> Collection[Certificate]:
        return sorted([
            load_der_certificate(cert_der)
            for cert_der
            in self._many_ca_by_ski.get(name, ())
        ], key=certlib.validity_sort_key, reverse=True)

    def _find_issuer_by_ski(self, ski: bytes) -> Certificate | None:
        certs = [
            load_der_certificate(cert_der)
            for cert_der
            in self._many_ca_by_ski.get(ski, ())
        ]
        if not certs:
            return None
        if len(certs) == 1:
            return certs[0]
        return max(certs, key=certlib.validity_sort_key)


    def verify_chain(self, conn: TLSConnection, entry_chain: Sequence[X509Entry]):
        fullchains = self._reorder_cert_chain(entry_chain[0], entry_chain[1:])
        if not fullchains:
            raise alerts.UnknownCa

        excs = []
        for fullchain in fullchains:
            try:
                for subject, issuer in itertools.pairwise(fullchain):
                    verify_signature(subject.asn1_certificate, issuer.asn1_certificate)
                verify_certificate_fullchain(conn.config.other_side, fullchain)
                for subject, issuer in itertools.pairwise(fullchain):
                    self.verify_online_status(subject, issuer)
            except (
                SignatureVerifyError,
                BaselineRequirementsError,
            ) as exc:
                excs.append(exc)

        if len(excs) == 1:
            raise alerts.BadCertificate from excs[0]
        elif excs:
            e =("the certificate chain has multiple trust anchors, but "
                "none of them could be validated")
            raise alerts.BadCertificate from TLSErrorGroup(e, excs)


    def _reorder_cert_chain(
        self,
        subject: X509Entry,
        issuers: Collection[X509Entry],
    ) -> Sequence[Sequence[X509Entry]]:
        if self.is_trusted(subject.asn1_certificate):
            return [[subject]]
        if not issuers:
            if asn1_issuer := self.find_issuer(subject.asn1_certificate):
                entry = X509Entry(der_encode(asn1_issuer), ())
                entry.asn1_certificate = asn1_issuer
                return [[subject, entry]]
            return []
        return sorted([
            [subject, direct_issuer, *chain]
            for direct_issuer in self._yield_direct_issuers(subject, issuers)
            for chain in self._reorder_cert_chain(direct_issuer, [
                issuer for issuer in issuers if issuer is not direct_issuer
            ])
        ], key=len)


    def _yield_direct_issuers(
        self,
        subject: X509Entry,
        issuers: Iterable[X509Entry],
    ) -> Iterator[X509Entry]:
        aki_ext = certlib.get_extension(
            subject.asn1_certificate,
            ExtensionOID.AUTHORITY_KEY_IDENTIFIER,
            AuthorityKeyIdentifier(),
            missing_ok=True,
        )
        if aki_ext:
            for issuer in issuers:
                ski_ext = certlib.get_extension(
                    issuer.asn1_certificate,
                    ExtensionOID.SUBJECT_KEY_IDENTIFIER,
                    SubjectKeyIdentifier(),
                    missing_ok=True,
                )
                if ski_ext and ski_ext == aki_ext['keyIdentifier']:
                    yield issuer
        else:
            issuer_name = certlib.issuer(subject.asn1_certificate)
            for issuer in issuers:
                if certlib.subject(issuer.asn1_certificate) == issuer_name:
                    yield issuer


    def verify_online_status(self, subject, issuer):
        if certlib.is_short_lived(subject.asn1_certificate):
            logger.debug("pass: short lived")
            return

        try:
            e = "TODO: verify online status"
            raise NotImplementedError(e)
        except NotImplementedError:
            logger.warning("not implemented section skipped", exc_info=True)
            return

        ocsp_request = ...  # TODO
        status = subject.extensions.get(ExtensionType.STATUS_REQUEST)
        if status and status.status_type == CertificateStatusType.OCSP:
            load_verify_ocsp(ocsp_request, status.ocsp_response, issuer.asn1_certificate)
            logger.debug("pass: ocsp stapling")
            return

        must_staple = ...  # TODO
        if must_staple:
            e = "Certificate %s has Must Staple feature, but no OCSP stapling found."
            raise alerts.CertificateUnknown(e)

        if not self.network_service:
            logger.debug("pass: no network service")
            return

        if self.network_service.get_cached_ocsp(ocsp_request):
            logger.debug("pass: cached ocsp")
            return

        crl_urls = certlib.get_crl_urls(subject.asn1_certificate)
        if crl := self.network_service.get_cached_crl(crl_urls):
            if ...:  # TODO
                e = "certificate %s found in online revocation list"
                raise alerts.CertificateRevoked(e)
            logger.debug("pass: cached crl")
            return

        if ocsp_urls := certlib.get_ocsp_urls(subject.asn1_certificate):
            self.network_service.request_ocsp(
                ocsp_urls[0],
                ocsp_request,
                issuer.asn1_certificate
            )
            logger.debug("pass: request ocsp")
            return

        crl = self.network_service.request_crl(crl_urls)
        if ...:  # TODO
            e = "certificate %s found in online revocation list"
            raise alerts.CertificateRevoked(e)
        logger.debug("pass: request crl")
