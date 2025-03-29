import argparse
import re

from . import load
from .oid import (
    OCSPResponseType,
    PublicKeyAlgorithmOID,
    SignatureAlgorithmOID,
    oid_from_pyasn1,
    parse_oid,
)
from .types import Asn1Certificate, Asn1OCSPResponse


def prettyoid(obj):
    return re.sub(r'\b(?:\d+\.)+\d+\b', lambda m: repr(parse_oid(m[0])), str(obj))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--format', choices=('der', 'pem'))
    parser.add_argument('-c', '--class', dest='asn1class', default='cert', choices=(
        'cert', 'certchain', 'crl', 'ocsp-res', 'ocsp-req', 'pub-key', 'priv-key'))
    parser.add_argument('file')
    options = parser.parse_args()

    if not options.format:
        with open(options.file, 'rb') as file:
            options.format = 'pem' if file.read(11) == b'-----BEGIN ' else 'der'

    x509_load = {
        ('pem', 'cert'): load.load_pem_certificate,
        ('pem', 'certchain'): load.load_pem_certificates,
        ('der', 'cert'): load.load_der_certificate,
        ('pem', 'crl'): load.load_pem_crl,
        ('der', 'crl'): load.load_der_crl,
        ('der', 'ocsp-req'): load.load_der_ocsp_request,
        ('der', 'ocsp-res'): load.load_der_ocsp_response,
        ('pem', 'priv-key'): load.load_pem_private_key,
        ('der', 'priv-key'): load.load_der_private_key,
        ('pem', 'pub-key'): load.load_pem_public_key,
        ('der', 'pub-key'): load.load_der_public_key,
    }[options.format, options.asn1class]

    with open(options.file, 'rb') as file:
        data = file.read()
        obj = x509_load(data)

    return data, obj


if __name__ == '__main__':
    data, obj = main()
    print(prettyoid(obj))
    if (
        isinstance(obj, Asn1OCSPResponse)
        and obj['responseStatus'] == 0  # successful
        and oid_from_pyasn1(
            OCSPResponseType,
            obj['responseBytes']['responseType']
        ) == OCSPResponseType.OCSP_BASIC
    ):
        ocsp = load.load_der_ocsp_basic_response(obj['responseBytes']['response'].asOctets())
        print(prettyoid(ocsp))

    if isinstance(obj, Asn1Certificate):
        pubkey_oid, pubkey_params = load.load_algorithm(
            PublicKeyAlgorithmOID,
            obj['tbsCertificate']['subjectPublicKeyInfo']['algorithm'])
        print(repr(pubkey_oid))
        print(prettyoid(pubkey_params))

        sign_oid, sign_params = load.load_algorithm(
            SignatureAlgorithmOID, obj['signatureAlgorithm'])
        print(repr(sign_oid))
        print(prettyoid(sign_params))
