import base64
import re
from enum import IntEnum

KNOWN_PEM_LABELS = (
    'CERTIFICATE', 'X509 CRL', 'CERTIFICATE REQUEST', 'PKCS7', 'CMS',
    'PRIVATE KEY', 'ENCRYPTED PRIVATE KEY', 'ATTRIBUTE CERTIFICATE',
    'PUBLIC KEY',
)
PEM_LABEL_RE = re.compile(r'[!-,.-~]+(?:[\s-][!-,.-~]+)')

# Headers found in the cryptography-vectors PEM files
# Ones known to rfc7468:
"""\
108 -----BEGIN CERTIFICATE-----
 27 -----BEGIN PRIVATE KEY-----
 21 -----BEGIN X509 CRL-----
 18 -----BEGIN ENCRYPTED PRIVATE KEY-----
 16 -----BEGIN CERTIFICATE REQUEST-----
 15 -----BEGIN PUBLIC KEY-----
  2 -----BEGIN PKCS7-----
"""
# Ones unknown to rfc7468:
"""\
  7 -----BEGIN RSA PRIVATE KEY-----
  5 -----BEGIN EC PRIVATE KEY-----
  5 -----BEGIN DSA PRIVATE KEY-----
  3 -----BEGIN RSA PUBLIC KEY-----
  2 -----BEGIN X509 CERTIFICATE-----
  1 -----BEGIN X9.42 DH PARAMETERS-----
  1 -----BEGIN NEW CERTIFICATE REQUEST-----
  1 -----BEGIN DSA PUBLIC KEY-----
  1 -----BEGIN DSA PARAMETERS-----
  1 -----BEGIN DH PARAMETERS-----
"""

def is_valid_pem_label(label):
    """ Is :param:`label` a valid label according to RFC 7468 """
    if label == '':
        return True
    if label in KNOWN_PEM_LABELS:
        return True
    return re.fullmatch(PEM_LABEL_RE, label)


def pem_encode(der_data: bytes, label: str, linesep='\n'):
    if label not in KNOWN_PEM_LABELS:
        e = f"unknown label: {label}"
        raise ValueError(e)
    if linesep not in ('\n', '\r', '\r\n'):
        e = fr"linesep is neither \n, \r, or \r\n: {linesep}"
        raise ValueError(e)

    preeb = f'-----BEGIN {label}-----{linesep}'.encode()
    posteb = f'-----END {label}-----{linesep}'.encode()
    b64 = base64.b64encode(der_data)

    linesep_cnt = len(b64) // 64 + bool(len(der_data) % 48)
    length = len(preeb) + len(posteb) + len(b64) + linesep_cnt * len(linesep)

    pem_data = bytearray(length)
    pem_data[:len(preeb)] = preeb
    j = len(preeb)
    for i in range(0, len(b64), 64):
        pem_data[j : j + 64] = b64[i : i + 64]
        pem_data[j + 64 : j + 64 + len(linesep)] = linesep.encode()
        j += 64 + len(linesep)
    pem_data[j:length] = posteb

    assert len(pem_data) == length, (len(pem_data), length)  # noqa: S101
    return pem_data


class _PemState(IntEnum):
    WAIT_BEGIN = 1
    WAIT_END = 2


def pem_decode(substrate: str, expect_label='', *, multi=False):  # noqa: C901, PLR0912
    multi_der_data = []
    state = _PemState.WAIT_BEGIN
    for lineno, line in enumerate(substrate.splitlines()):
        match state:
            case _PemState.WAIT_BEGIN:
                if line.startswith('-----BEGIN ') and line.endswith('-----'):
                    label = line[11:-5]
                    if expect_label:
                        if label != expect_label:
                            continue
                    elif not is_valid_pem_label(label):
                        e = f"invalid label at line {lineno}: {label!r}"
                        raise ValueError(e)
                    der_data = bytearray()
                    state = _PemState.WAIT_END

            case _PemState.WAIT_END:
                if line == f'-----END {label}-----':
                    if not multi:
                        return bytes(der_data)
                    multi_der_data.append(bytes(der_data))
                    state = _PemState.WAIT_BEGIN
                elif line.startswith('-----'):
                    e = f"invalid boundary at line {lineno}"
                    raise ValueError(e)
                else:
                    try:
                        der_data += base64.b64decode(line.rstrip())
                    except ValueError as exc:
                        e = f'{exc.args[0]} at line {lineno}'
                        raise ValueError(e) from None

    if state == _PemState.WAIT_END:
        e = f"end boundary {f'-----END {label}-----'!r} not found"
        raise ValueError(e)
    elif not multi:
        boundary = f'-----BEGIN {expect_label or "[label]"}----'
        e = f"begin boundary {boundary!r} not found"
        raise ValueError(e)

    return multi_der_data
