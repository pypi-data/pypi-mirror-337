import logging

from pyasn1.codec.der.encoder import encode as der_encode
from pyasn1_modules.rfc5280 import Certificate
from pyasn1_modules.rfc6960 import BasicOCSPResponse

from siotls.contents import alerts
from siotls.crypto import SignatureKeyError, SignatureVerifyError, TLSSignatureScheme
from siotls.x509 import (
    OCSPResponseType,
    certlib,
    load_der_ocsp_basic_response,
    load_der_ocsp_request,
    load_der_ocsp_response,
    oid_from_pyasn1,
)
from siotls.x509.cabforum import BaselineRequirementsError, verify_ocsp_basic_response

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG


def verify_signature(
    subject: Certificate | BasicOCSPResponse,
    issuer: Certificate,
    tbs_key='tbsCertificate',
):
    issuer_suites = {
        suite.iana_id for suite in TLSSignatureScheme.for_key_algo(
            issuer['tbsCertificate']['subjectPublicKeyInfo']['algorithm'])
    }
    SignSuite = TLSSignatureScheme.for_signature_algo(subject['signatureAlgorithm'])
    if SignSuite.iana_id not in issuer_suites:
        e =(f"the object is signed using {SignSuite.iana_id} but the issuer "
            f"public key can only produce signatures for {issuer_suites}")
        raise SignatureKeyError(e)
    sign_algo = SignSuite(public_key=certlib.pubkey(issuer))
    sign_algo.verify(
        signature=subject['signature'].asOctets(),
        message=der_encode(subject[tbs_key]),
    )


def is_signature_valid(subject: Certificate, issuer: Certificate) -> bool:
    try:
        verify_signature(subject, issuer)
    except (SignatureKeyError, SignatureVerifyError):
        return False
    return True


def load_verify_ocsp(der_ocsp_req, der_ocsp_res, signer_cert) -> BasicOCSPResponse:

    # load the basic response
    try:
        ocsp_res = load_der_ocsp_response(der_ocsp_res)
    except ValueError as exc:
        e = "malformed OCSP response"
        raise alerts.BadCertificateStatusResponse(e) from exc
    if ocsp_res['responseStatus'] != 0:  # 0 is successful
        e = f"OCSP response status is not successful: {ocsp_res['responseStatus']}"
        raise alerts.BadCertificateStatusResponse(e)
    ocsp_res_type = oid_from_pyasn1(OCSPResponseType, ocsp_res['responseBytes']['responseType'])
    if ocsp_res_type != OCSPResponseType.OCSP_BASIC:
        e = f"OCSP response type is not {OCSPResponseType.OCSP_BASIC}: {ocsp_res_type}"
        raise alerts.BadCertificateStatusResponse(e)
    try:
        ocsp_basic_res = load_der_ocsp_basic_response(
            ocsp_res['responseBytes']['response'].asOctets())
    except ValueError as exc:
        e = "malformed OCSP basic response"
        raise alerts.BadCertificateStatusResponse(e) from exc

    # verify the static informations
    ocsp_req = load_der_ocsp_request(der_ocsp_req)
    try:
        verify_ocsp_basic_response(ocsp_req, ocsp_basic_res, signer_cert)
    except BaselineRequirementsError as exc:
        e = "OCSP verification failed"
        raise alerts.BadCertificateStatusResponse(e) from exc

    # verify the signature
    try:
        verify_signature(ocsp_basic_res, signer_cert, 'tbsResponseData')
    except (SignatureKeyError, SignatureVerifyError) as exc:
        e = "OCSP basic response signature verification failed"
        raise alerts.BadCertificateStatusResponse(e) from exc

    return ocsp_basic_res


def load_verify_cert(*args):
    raise NotImplementedError  # TODO


def load_verify_crl(*args):
    raise NotImplementedError  # TODO
