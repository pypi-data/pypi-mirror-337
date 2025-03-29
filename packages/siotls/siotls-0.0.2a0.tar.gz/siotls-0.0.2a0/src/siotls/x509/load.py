import pyasn1_modules.rfc4055  # RSA algorithms
import pyasn1_modules.rfc5480  # ECDSA algorithms # noqa: F401
from pyasn1.codec.der.decoder import decode as der_decode
from pyasn1.codec.native.decoder import decode as py_decode
from pyasn1_modules.rfc5280 import algorithmIdentifierMap

from .oid import PublicKeyAlgorithmOID, SignatureAlgorithmOID, oid_from_pyasn1
from .pem import pem_decode
from .types import (
    Asn1AlgorithmIdentifier,
    Asn1BasicOCSPResponse,
    Asn1Certificate,
    Asn1CertificateList,
    Asn1OCSPRequest,
    Asn1OCSPResponse,
    Asn1PrivateKeyInfo,
    Asn1SubjectPublicKeyInfo,
    DerCertificate,
    DerCRL,
    DerOCSPBasicResponse,
    DerOCSPRequest,
    DerOCSPResponse,
    DerPrivateKey,
    DerPublicKey,
    PemCertificate,
    PemCertificates,
    PemCRL,
    PemPrivateKey,
    PemPublicKey,
)

__all__ = (
    'decode_pem_certificate',
    'decode_pem_certificates',
    'decode_pem_crl',
    'decode_pem_private_key',
    'decode_pem_public_key',
    'load_algorithm',
    'load_der_certificate',
    'load_der_certificates',
    'load_der_crl',
    'load_der_ocsp_basic_response',
    'load_der_ocsp_request',
    'load_der_ocsp_response',
    'load_der_private_key',
    'load_der_public_key',
    'load_pem_certificate',
    'load_pem_certificates',
    'load_pem_crl',
    'load_pem_private_key',
    'load_pem_public_key',
)


def load_der(data, asn_object):
    """
    :meta private:
    """
    cert, rest = der_decode(data, asn_object)
    if rest:
        e =(f"only {len(data) - len(rest)} bytes out of {len(data)} "
            "could be decoded")
        raise ValueError(e)
    return cert


# Single certificate
def load_der_certificate(data: DerCertificate) -> Asn1Certificate:
    return load_der(data, Asn1Certificate())

def decode_pem_certificate(data: PemCertificate) -> DerCertificate:
    return pem_decode(data.decode(), 'CERTIFICATE')

def load_pem_certificate(data: PemCertificate) -> Asn1Certificate:
    return load_der_certificate(decode_pem_certificate(data))


# Multiple certificates
def load_der_certificates(data_list: list[DerCertificate]) -> list[Asn1Certificate]:
    return [load_der(data, Asn1Certificate()) for data in data_list]

def decode_pem_certificates(data: PemCertificates) -> list[DerCertificate]:
    return list(pem_decode(data.decode(), 'CERTIFICATE', multi=True))

def load_pem_certificates(data: PemCertificates) -> list[Asn1Certificate]:
    return load_der_certificates(decode_pem_certificates(data))


# Certificate Revocation List (CRL)
def load_der_crl(data: DerCRL) -> Asn1CertificateList:
    return load_der(data, Asn1CertificateList())

def decode_pem_crl(data: PemCRL) -> DerCRL:
    return pem_decode(data.decode(), 'X509 CRL')

def load_pem_crl(data: PemCRL) -> Asn1CertificateList:
    return load_der_crl(decode_pem_crl(data))


# OCSP
def load_der_ocsp_request(data: DerOCSPRequest) -> Asn1OCSPRequest:
    return load_der(data, Asn1OCSPRequest())

def load_der_ocsp_response(data: DerOCSPResponse) -> Asn1OCSPResponse:
    return load_der(data, Asn1OCSPResponse())

def load_der_ocsp_basic_response(data: DerOCSPBasicResponse) -> Asn1BasicOCSPResponse:
    return load_der(data, Asn1BasicOCSPResponse())


# Private Key
def load_der_private_key(data: DerPrivateKey) -> Asn1PrivateKeyInfo:
    return load_der(data, Asn1PrivateKeyInfo())

def decode_pem_private_key(data: PemPrivateKey) -> DerPrivateKey:
    return pem_decode(data.decode(), 'PRIVATE KEY')

def load_pem_private_key(data: PemPrivateKey) -> Asn1PrivateKeyInfo:
    return load_der(decode_pem_private_key(data), Asn1PrivateKeyInfo())


# Public Key
def load_der_public_key(data: DerPublicKey) -> Asn1SubjectPublicKeyInfo:
    return load_der(data, Asn1SubjectPublicKeyInfo())

def decode_pem_public_key(data: PemPublicKey) -> DerPublicKey:
    return pem_decode(data.decode(), 'PUBLIC KEY')

def load_pem_public_key(data: PemPublicKey) -> Asn1SubjectPublicKeyInfo:
    return load_der(decode_pem_public_key(data), Asn1SubjectPublicKeyInfo())


# Key algorithm
def load_algorithm(
    AlgoOID: PublicKeyAlgorithmOID | SignatureAlgorithmOID,  # noqa: N803
    algo: Asn1AlgorithmIdentifier,
):
    algo_oid = oid_from_pyasn1(AlgoOID, algo['algorithm'])
    try:
        spec = algorithmIdentifierMap[algo['algorithm']]
    except KeyError:
        return algo_oid, None  # no parameters
    if not algo['parameters'].hasValue():
        return algo_oid, py_decode({}, spec)  # missing parameters
    return algo_oid, load_der(algo['parameters'], spec)
