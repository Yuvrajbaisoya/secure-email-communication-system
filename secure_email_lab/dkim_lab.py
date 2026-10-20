"""Real RSA-SHA256 signing in a *bounded* DKIM relaxed/relaxed test fixture.

Not a full RFC 6376 implementation. Supports ASCII RFC 5322 lab messages,
a single DKIM-Signature and an explicit trusted public key. No DNS discovery,
internationalization, multi-signature policies or robust MIME canonicalization.
"""
import base64
import hashlib
import re

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def _normalize(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n").replace(b"\n", b"\r\n")


def _parse(data: bytes) -> tuple[list[tuple[str, bytes]], bytes]:
    normalized = _normalize(data)
    head, separator, body = normalized.partition(b"\r\n\r\n")
    if not separator:
        raise ValueError("Missing RFC 5322 header/body separator")
    headers: list[tuple[str, bytes]] = []
    for line in head.split(b"\r\n"):
        if line.startswith((b" ", b"\t")):
            if not headers:
                raise ValueError("Orphan header continuation")
            name, value = headers[-1]
            headers[-1] = name, value + b"\r\n" + line
        else:
            name, colon, value = line.partition(b":")
            if not colon or not re.fullmatch(rb"[A-Za-z0-9-]+", name):
                raise ValueError("Malformed ASCII test header")
            headers.append((name.decode("ascii").lower(), value))
    return headers, body


def _relaxed_header(name: str, value: bytes) -> bytes:
    unfolded = re.sub(rb"\r\n[ \t]+", b" ", value)
    compact = re.sub(rb"[ \t]+", b" ", unfolded).strip(b" \t")
    return name.lower().encode("ascii") + b":" + compact + b"\r\n"


def _relaxed_body(body: bytes) -> bytes:
    lines = [re.sub(rb"[ \t]+", b" ", line.rstrip(b" \t"))
             for line in body.split(b"\r\n")]
    while lines and lines[-1] == b"":
        lines.pop()
    return b"\r\n".join(lines) + b"\r\n"


def _chosen(headers: list[tuple[str, bytes]], selected: tuple[str, ...]) -> bytes:
    # DKIM chooses each occurrence from the BOTTOM of the header block.
    taken: set[int] = set()
    result = bytearray()
    for name in selected:
        for index in range(len(headers) - 1, -1, -1):
            if index not in taken and headers[index][0] == name:
                taken.add(index)
                result.extend(_relaxed_header(name, headers[index][1]))
                break
        else:
            raise ValueError("Missing signed header: " + name)
    return bytes(result)


def generate_lab_key() -> rsa.RSAPrivateKey:
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def public_dns_txt(key: rsa.RSAPublicKey) -> str:
    """Synthetic selector._domainkey TXT record; publishing is NOT performed."""
    encoded = base64.b64encode(key.public_bytes(
        serialization.Encoding.DER, serialization.PublicFormat.PKCS1
    )).decode("ascii")
    return "v=DKIM1; k=rsa; p=" + encoded


def sign(raw: bytes, key: rsa.RSAPrivateKey, *, domain: str = "example.test",
         selector: str = "lab") -> bytes:
    if not re.fullmatch(r"[a-zA-Z0-9.-]+", domain) or not re.fullmatch(r"[a-zA-Z0-9-]+", selector):
        raise ValueError("Invalid lab signing domain or selector")
    headers, body = _parse(raw)
    names = ("from", "to", "subject")
    signed = _chosen(headers, names)
    body_hash = base64.b64encode(hashlib.sha256(_relaxed_body(body)).digest())
    unsigned = (b"v=1; a=rsa-sha256; c=relaxed/relaxed; d=" + domain.encode()
                + b"; s=" + selector.encode()
                + b"; h=from:to:subject; bh=" + body_hash + b"; b=")
    digest_input = signed + _relaxed_header("dkim-signature", b" " + unsigned)
    signature = key.sign(digest_input, padding.PKCS1v15(), hashes.SHA256())
    return b"DKIM-Signature: " + unsigned + base64.b64encode(signature) + b"\r\n" + _normalize(raw)


def verify(raw: bytes, key: rsa.RSAPublicKey, *, expected_domain: str = "example.test",
           expected_selector: str = "lab") -> bool:
    """Verify a fixed-format lab signature using an explicitly trusted key."""
    try:
        headers, body = _parse(raw)
        signatures = [value for name, value in headers if name == "dkim-signature"]
        if len(signatures) != 1:
            return False
        value = signatures[0].strip()
        tags = {}
        for chunk in value.split(b";"):
            name, sep, val = chunk.strip().partition(b"=")
            if not sep or name in tags:
                return False
            tags[name] = val
        required = {b"v", b"a", b"c", b"d", b"s", b"h", b"bh", b"b"}
        if set(tags) != required or tags[b"v"] != b"1" or tags[b"a"] != b"rsa-sha256":
            return False
        if tags[b"c"] != b"relaxed/relaxed" or tags[b"h"] != b"from:to:subject":
            return False
        if tags[b"d"] != expected_domain.encode() or tags[b"s"] != expected_selector.encode():
            return False
        calculated_hash = base64.b64encode(hashlib.sha256(_relaxed_body(body)).digest())
        if not __import__("hmac").compare_digest(calculated_hash, tags[b"bh"]):
            return False
        # Verify only our documented, single-line, fixed-order educational
        # serialization. Do not treat this as generic incoming DKIM verification.
        prefix = (b"v=1; a=rsa-sha256; c=relaxed/relaxed; d=" + tags[b"d"]
                  + b"; s=" + tags[b"s"] + b"; h=from:to:subject; bh="
                  + tags[b"bh"] + b"; b=")
        if value != prefix + tags[b"b"]:
            return False
        signed_headers = _chosen(headers, ("from", "to", "subject"))
        digest_input = signed_headers + _relaxed_header("dkim-signature", b" " + prefix)
        key.verify(base64.b64decode(tags[b"b"], validate=True), digest_input,
                   padding.PKCS1v15(), hashes.SHA256())
        return True
    except (ValueError, InvalidSignature, TypeError, KeyError, IndexError):
        return False
