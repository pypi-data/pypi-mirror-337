from collections.abc import Sequence

from pyasn1_modules.rfc5280 import Certificate


class BaselineRequirementsError(Exception):
    pass


def verify_certificate_fullchain(other_side, fullchain: Sequence[Certificate]):
    raise NotImplementedError  # TODO

def verify_ocsp_basic_response():
    raise NotImplementedError  # TODO
