import importlib

from .cipher_suites import TLSCipherSuite
from .key_exchanges import TLSKeyExchange
from .signature_schemes import SignatureKeyError, SignatureVerifyError, TLSSignatureScheme


def install(provider):
    importlib.import_module('.' + provider, 'siotls.crypto.providers')
