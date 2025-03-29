import abc
from collections import defaultdict
from typing import ClassVar

from siotls import TLSError
from siotls.iana import SignatureScheme
from siotls.utils import RegistryMeta
from siotls.x509 import (
    EllipticCurveOID,
    HashOID,
    PublicKeyAlgorithmOID,
    SignatureAlgorithmOID,
    load_algorithm,
    oid_from_pyasn1,
)


class SignatureKeyError(TLSError):
    pass


class SignatureVerifyError(TLSError):
    pass


class ISign(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, *, public_key=None, private_key=None):
        raise NotImplementedError

    @abc.abstractmethod
    def sign(self, message):
        raise NotImplementedError

    @abc.abstractmethod
    def verify(self, signature, message):
        raise NotImplementedError


class TLSSignatureScheme(ISign, metaclass=RegistryMeta):
    _registry_key = '_signature_iana_registry'
    _signature_iana_registry: ClassVar = {}
    _signature_sign_oid_registry: ClassVar = defaultdict(list)
    _signature_pubkey_oid_registry: ClassVar = defaultdict(list)

    iana_id: SignatureScheme
    sign_oid: SignatureAlgorithmOID
    pubkey_id: PublicKeyAlgorithmOID

    def __init_subclass__(cls, *, register=True, **kwargs):
        super().__init_subclass__(**kwargs)
        if register and TLSSignatureScheme in cls.__bases__:
            other_cls = cls._signature_iana_registry.setdefault(cls.iana_id, cls)
            if cls is not other_cls:
                e =(f"cannot install {cls} as {other_cls} is installed "
                    f"for {cls.iana_id!r} already")
                raise KeyError(e)
            cls._signature_sign_oid_registry[cls.sign_oid].append(cls)
            cls._signature_pubkey_oid_registry[cls.pubkey_oid].append(cls)

    @classmethod
    def for_signature_algo(cls, asn1_signature_algo):
        # asn1_certificate['signatureAlgorithm']
        sign_oid, params = load_algorithm(SignatureAlgorithmOID, asn1_signature_algo)
        Suites = cls._signature_sign_oid_registry[sign_oid]
        if sign_oid == SignatureAlgorithmOID.RSASSA_PSS:
            hash_oid = oid_from_pyasn1(params['hashAlgorithm'])
            Suites = [Suite for Suite in Suites if Suite.hash_oid == hash_oid]
        if len(Suites) == 1:
            return Suites[0]
        if not Suites:
            e = f"no tls suite installed for {sign_oid!r}"
            raise KeyError(e)
        e = f"too many tls suite installed for {sign_oid!r}: {Suites}"
        raise KeyError(e)

    @classmethod
    def for_key_algo(cls, asn1_key_algo):
        # asn1_certificate['tbsCertificate']['subjectPublicKeyInfo']['algorithm']
        pubkey_oid, params = load_algorithm(PublicKeyAlgorithmOID, asn1_key_algo)
        Suites = cls._signature_pubkey_oid_registry[pubkey_oid]
        if pubkey_oid == PublicKeyAlgorithmOID.EC_PUBLIC_KEY:
            curve_oid = oid_from_pyasn1(EllipticCurveOID, params['namedCurve'])
            Suites = [Suite for Suite in Suites if Suite.curve_oid == curve_oid]
        return Suites


class RsaPkcs1Sha256Mixin:
    iana_id = SignatureScheme.rsa_pkcs1_sha256
    sign_oid = SignatureAlgorithmOID.RSA_WITH_SHA256
    pubkey_oid = PublicKeyAlgorithmOID.RSAES_PKCS1_v1_5

class RsaPkcs1Sha384Mixin:
    iana_id = SignatureScheme.rsa_pkcs1_sha384
    sign_oid = SignatureAlgorithmOID.RSA_WITH_SHA384
    pubkey_oid = PublicKeyAlgorithmOID.RSAES_PKCS1_v1_5

class RsaPkcs1Sha512Mixin:
    iana_id = SignatureScheme.rsa_pkcs1_sha512
    sign_oid = SignatureAlgorithmOID.RSA_WITH_SHA512
    pubkey_oid = PublicKeyAlgorithmOID.RSAES_PKCS1_v1_5

class RsaPssRsaeSha256Mixin:
    iana_id = SignatureScheme.rsa_pss_rsae_sha256
    sign_oid = SignatureAlgorithmOID.RSASSA_PSS
    pubkey_oid = PublicKeyAlgorithmOID.RSAES_PKCS1_v1_5

class RsaPssRsaeSha384Mixin:
    iana_id = SignatureScheme.rsa_pss_rsae_sha384
    sign_oid = SignatureAlgorithmOID.RSASSA_PSS
    pubkey_oid = PublicKeyAlgorithmOID.RSAES_PKCS1_v1_5

class RsaPssRsaeSha512Mixin:
    iana_id = SignatureScheme.rsa_pss_rsae_sha512
    sign_oid = SignatureAlgorithmOID.RSASSA_PSS
    pubkey_oid = PublicKeyAlgorithmOID.RSAES_PKCS1_v1_5

class RsaPssPssSha256Mixin:
    iana_id = SignatureScheme.rsa_pss_pss_sha256
    sign_oid = SignatureAlgorithmOID.RSASSA_PSS
    pubkey_oid = PublicKeyAlgorithmOID.RSASSA_PSS
    hash_oid = HashOID.sha256

class RsaPssPssSha384Mixin:
    iana_id = SignatureScheme.rsa_pss_pss_sha384
    sign_oid = SignatureAlgorithmOID.RSASSA_PSS
    pubkey_oid = PublicKeyAlgorithmOID.RSASSA_PSS
    hash_oid = HashOID.sha384

class RsaPssPssSha512Mixin:
    iana_id = SignatureScheme.rsa_pss_pss_sha512
    sign_oid = SignatureAlgorithmOID.RSASSA_PSS
    pubkey_oid = PublicKeyAlgorithmOID.RSASSA_PSS
    hash_oid = HashOID.sha512


class EcdsaSecp256r1Sha256Mixin:
    iana_id = SignatureScheme.ecdsa_secp256r1_sha256
    sign_oid = SignatureAlgorithmOID.ECDSA_WITH_SHA256
    pubkey_oid = PublicKeyAlgorithmOID.EC_PUBLIC_KEY
    curve_oid = EllipticCurveOID.secp256r1

class EcdsaSecp384r1Sha384Mixin:
    iana_id = SignatureScheme.ecdsa_secp384r1_sha384
    sign_oid = SignatureAlgorithmOID.ECDSA_WITH_SHA384
    pubkey_oid = PublicKeyAlgorithmOID.EC_PUBLIC_KEY
    curve_oid = EllipticCurveOID.secp384r1

class EcdsaSecp521r1Sha512Mixin:
    iana_id = SignatureScheme.ecdsa_secp521r1_sha512
    sign_oid = SignatureAlgorithmOID.ECDSA_WITH_SHA512
    pubkey_oid = PublicKeyAlgorithmOID.EC_PUBLIC_KEY
    curve_oid = EllipticCurveOID.secp521r1


class Ed25519Mixin:
    iana_id = SignatureScheme.ed25519
    sign_oid = SignatureAlgorithmOID.ED25519
    pubkey_oid = PublicKeyAlgorithmOID.ED25519

class Ed448Mixin:
    iana_id = SignatureScheme.ed448
    sign_oid = SignatureAlgorithmOID.ED448
    pubkey_oid = PublicKeyAlgorithmOID.ED448
