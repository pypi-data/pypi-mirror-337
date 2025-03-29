# noqa: A005

import typing

from pyasn1_modules.rfc5280 import (
    AlgorithmIdentifier as Asn1AlgorithmIdentifier,
    AuthorityInfoAccessSyntax as Asn1AuthorityInfoAccessSyntax,
    Certificate as Asn1Certificate,
    CertificateList as Asn1CertificateList,
    CRLDistributionPoints as Asn1CRLDistributionPoints,
    SubjectPublicKeyInfo as Asn1SubjectPublicKeyInfo,
)
from pyasn1_modules.rfc5958 import PrivateKeyInfo as Asn1PrivateKeyInfo
from pyasn1_modules.rfc6960 import (
    BasicOCSPResponse as Asn1BasicOCSPResponse,
    OCSPRequest as Asn1OCSPRequest,
    OCSPResponse as Asn1OCSPResponse,
)

__all__ = (
    'Asn1AlgorithmIdentifier',
    'Asn1AuthorityInfoAccessSyntax',
    'Asn1BasicOCSPResponse',
    'Asn1CRLDistributionPoints',
    'Asn1Certificate',
    'Asn1CertificateList',
    'Asn1OCSPRequest',
    'Asn1OCSPResponse',
    'Asn1PrivateKeyInfo',
    'Asn1SubjectPublicKeyInfo',
    'DerCRL',
    'DerCertificate',
    'DerOCSPBasicResponse',
    'DerOCSPRequest',
    'DerOCSPResponse',
    'DerPrivateKey',
    'DerPublicKey',
    'PemCRL',
    'PemCertificate',
    'PemCertificates',
    'PemPrivateKey',
    'PemPublicKey',
)

DerCertificate = typing.NewType('DerCertificate', bytes)  #:
PemCertificate = typing.NewType('PemCertificate', bytes)  #:
PemCertificates = typing.NewType('PemCertificates', bytes)  #:
DerCRL = typing.NewType('DerCRL', bytes)  #:
PemCRL = typing.NewType('PemCRL', bytes)  #:
DerOCSPRequest = typing.NewType('DerOCSPRequest', bytes)  #:
DerOCSPResponse = typing.NewType('DerOCSPResponse', bytes)  #:
DerOCSPBasicResponse = typing.NewType('DerOCSPBasicResponse', bytes)  #:
DerPrivateKey = typing.NewType('DerPrivateKey', bytes)  #:
PemPrivateKey = typing.NewType('PemPrivateKey', bytes)  #:
DerPublicKey = typing.NewType('DerPublicKey', bytes)  #:
PemPublicKey = typing.NewType('PemPublicKey', bytes)  #:
