from hashlib import sha256
from base32_tiny import encode
from base64 import b64decode, b64encode, urlsafe_b64encode, urlsafe_b64decode, b16decode


def to_base16(b: bytes) -> str:
    # Do not use b16encode, it only for UpperCase letters
    # return hexlify(b).decode("utf-8")
    return b.hex()


def from_base16(s: str) -> bytes:
    inputs = s.upper()
    return b16decode(inputs)


def from_base64(s: str) -> bytes:
    return b64decode(s)


def to_base64(b: bytes) -> str:
    encoded = b64encode(b)
    return encoded.decode("utf-8")


def from_urlsafe_base64(s: str) -> bytes:
    s = s.strip()
    return urlsafe_b64decode(s)


def to_urlsafe_base64(b: bytes) -> str:
    return urlsafe_b64encode(b).decode("utf-8")


# def to_bytes(s: str) -> bytes:
#     s = s.strip()
#     if is_base16(s):
#         return b16decode(s)
#     if is_base64(s):
#         return from_base64(s)
#
#     raise


def base64_to_base16(s: str) -> str:
    b = from_base64(s)
    return to_base16(b)


def to_proof_key(s: str) -> str:
    s_bytes = s.encode("utf-8")
    h = sha256(s_bytes).digest()
    return encode(h, variant="Crockford")


