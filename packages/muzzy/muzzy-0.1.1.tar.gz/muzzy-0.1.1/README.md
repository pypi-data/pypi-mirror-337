# Muzzy
A python function library.

## Installation
use pip
```shell
pip install muzzy
```
use poetry
```
poetry add muzzy
```
> Please confirm that you have properly set up the Python interpreter and can correctly recognize the packages installed by Poetry.

## Usage
```python
from muzzy import is_base16, is_base64, is_url, to_base64, base32_encode, base32_decode

message = base32_encode(b"f", "Crockford")
print(base32_decode(message, "Crockford").decode("utf-8"))
```

## API Reference
### def base32_encode(s: bytes, variants: Variant, option:  Options = None) -> str
### def base32_decode(s: str, variants: Variant) -> bytes
### def to_base16(b: bytes) -> str
### def to_base64(b: bytes) -> str
### def to_urlsafe_base64(b: bytes) -> str
### def from_base16(s: str) -> bytes
### def from_base64(s: str) -> bytes
### def from_urlsafe_base64(s: str) -> bytes
### def base64_to_base16(s: str) -> str
### def is_base64(s: str) -> bool
### def is_base16(s: str) -> bool
### def is_url(s: str) -> bool
