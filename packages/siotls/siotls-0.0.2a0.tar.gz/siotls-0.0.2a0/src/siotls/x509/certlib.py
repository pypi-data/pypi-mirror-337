from collections.abc import Sequence
from datetime import UTC, datetime, timedelta
from functools import partial

from pyasn1.codec.der.encoder import encode as der_encode

from siotls.utils import try_cast

from .load import load_der
from .oid import (
    AuthorityInformationAccessOID,
    ExtensionOID,
    oid_from_pyasn1,
    oid_to_tuple,
)
from .types import (
    Asn1AuthorityInfoAccessSyntax,
    Asn1Certificate,
    Asn1CRLDistributionPoints,
)

_sentinel = object()


class BadCertificateError(Exception):
    pass


class ExtensionMissingError(BadCertificateError, KeyError):
    pass


def not_before(cert: Asn1Certificate) -> datetime:
    return cert['tbsCertificate']['validity']['notBefore']['utcTime'].asDateTime


def not_after(cert: Asn1Certificate) -> datetime:
    return cert['tbsCertificate']['validity']['notAfter']['utcTime'].asDateTime


def subject(cert: Asn1Certificate) -> bytes:
    return der_encode(cert['tbsCertificate']['subject'])


def issuer(cert: Asn1Certificate) -> bytes:
    return der_encode(cert['tbsCertificate']['issuer'])


def pubkey(cert: Asn1Certificate) -> bytes:
    return der_encode(cert['tbsCertificate']['subjectPublicKeyInfo'])


def validity_sort_key(cert: Asn1Certificate):
    # validities:
    # cert1: ---
    # cert2:  ---
    # cert3:      ---
    # cert4:       ---
    # now:         ^
    # order: 1 < 2 < 3 < 4
    cert_not_before = not_before(cert)
    return cert_not_before <= datetime.now(UTC) <= not_after(cert), cert_not_before


def is_short_lived(cert: Asn1Certificate) -> bool:
    # CA-Browser Forum TLS BR 2.1.2
    # page 29 Short-lived Subscriber Certificate
    cert_not_before = not_before(cert)
    if cert_not_before < datetime(2024, 3, 15, tzinfo=UTC):
        return False

    validity_period = not_after(cert) - cert_not_before
    if cert_not_before < datetime(2026, 3, 15, tzinfo=UTC):
        return validity_period <= timedelta(days=10)

    return validity_period <= timedelta(days=7)


def get_extension(
    cert: Asn1Certificate,
    ext_oid: ExtensionOID,
    pyasn_obj,
    *,
    missing_ok=False,
):
    for extension in cert['tbsCertificate']['extensions']:
        if oid_from_pyasn1(partial(try_cast, ExtensionOID), extension['extnID']) == ext_oid:
            try:
                return load_der(extension['extnValue'].asOctets(), pyasn_obj)
            except ValueError as exc:
                raise BadCertificateError from exc
    if missing_ok:
        return None
    raise ExtensionMissingError(ext_oid)


def get_crl_urls(cert: Asn1Certificate) -> Sequence[bytes]:
    # CA-Browser Forum TLS BR 2.1.2
    # section 7.1.2.11.2 CRL Distribution Points

    # MUST be present in Subordinate CA
    # MUST be present in Subscriber UNLESS Short-lived / AIA OCSP
    try:
        ext_crl_dps = cert.get_extension(
            ExtensionOID.CRL_DISTRIBUTION_POINTS,
            Asn1CRLDistributionPoints,
        )
    except ExtensionMissingError:
        if cert.is_short_lived or cert.get_ocsp_urls():
            return []
        raise

    try:
        # MUST contain at least one DistributionPoint (DP)
        # more than one DP is NOT RECOMMANDED
        # MUST contain DP.distributionPoint.fullName
        # MUST NOT contain DP.reasons or DP.cRLIssuer
        general_names = ext_crl_dps[0]['distributionPoint']['fullName']

        # MUST contain at least one GeneralName, MAY contain more.
        # MUST be type uniformResourceIdentifier with scheme http://
        http_uris = [name['uniformResourceIdentifier'].asOctets() for name in general_names]
    except (IndexError, KeyError) as exc:
        raise BadCertificateError from exc

    if not http_uris or any(not uri.startswith(b'http://') for uri in http_uris):
        e = "missing URIs or use non http schemes"
        raise BadCertificateError(e)

    return http_uris


def get_ocsp_urls(cert: Asn1Certificate) -> Sequence[bytes]:
    # CA-Browser Forum TLS BR 2.1.2
    # section 7.1.2.7.7 Subscriber Certificate Authority Information Access

    ext_aia = cert.get_extension(
        ExtensionOID.AUTHORITY_INFORMATION_ACCESS,
        Asn1AuthorityInfoAccessSyntax,
        missing_ok=True,
    )
    if not ext_aia:
        return False

    id_ad_ocsp = oid_to_tuple(AuthorityInformationAccessOID.OCSP)
    try:
        http_uris = [
            access_description['accessLocation']['uniformResourceIdentifier'].asOctets()
            for access_description in ext_aia
            if access_description['accessMethod'].asTuple() == id_ad_ocsp
        ]
    except KeyError as exc:
        raise BadCertificateError from exc

    if http_uris and any(not uri.startswith(b'http://') for uri in http_uris):
        e = "URI scheme must be http"
        raise BadCertificateError(e)

    return http_uris
