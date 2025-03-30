import validators
from re import fullmatch


def is_base16(s: str) -> bool:
    s = s.strip()
    return fullmatch(r'[A-Fa-f0-9]+', s) and len(s) % 2 == 0


def is_base64(s: str) -> bool:
    s = s.strip()
    return fullmatch(r'[A-Za-z0-9+/]*={0,2}', s) and len(s) % 4 == 0


# def is_base16(s: str):
#     return validators.base16(s)


# def is_base64(s: str):
#     return validators.base64(s)


def is_url(s: str):
    return validators.url(s)


