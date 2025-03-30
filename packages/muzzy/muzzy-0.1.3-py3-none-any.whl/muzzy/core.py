from base32_tiny import encode, decode
from base32_tiny.encode import Variant, Options


def base32_encode(s: bytes, variants: Variant, option:  Options = None) -> str:
    return encode(s, variant=variants, options=option)


def base32_decode(s: str, variants: Variant) -> bytes:
    return decode(s, variant=variants)




