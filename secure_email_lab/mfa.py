"""RFC 6238 TOTP demonstration with replay prevention and basic lockout.

This educational app is not an identity provider, mailbox MFA enforcement,
phishing-resistant passkey system, or production-ready authentication service.
"""
from dataclasses import dataclass
import base64
import hashlib
import hmac
import secrets
import struct


def generate_secret() -> str:
    return base64.b32encode(secrets.token_bytes(20)).decode("ascii").rstrip("=")


def _secret_bytes(secret: str) -> bytes:
    return base64.b32decode(secret.upper() + "=" * ((-len(secret)) % 8), casefold=True)


def hotp(secret: str, counter: int, digits: int = 6) -> str:
    if counter < 0 or digits not in (6, 8):
        raise ValueError("Invalid HOTP parameters")
    mac = hmac.new(_secret_bytes(secret), struct.pack(">Q", counter), hashlib.sha1).digest()
    offset = mac[-1] & 15
    value = struct.unpack(">I", mac[offset:offset + 4])[0] & 0x7fffffff
    return str(value % (10 ** digits)).zfill(digits)


def totp(secret: str, at_time: int, digits: int = 6, period: int = 30) -> str:
    if at_time < 0 or period <= 0:
        raise ValueError("Invalid TOTP time or period")
    return hotp(secret, at_time // period, digits)


@dataclass
class _Account:
    salt: bytes
    password_hash: bytes
    secret: str
    failed: int = 0
    locked_until: int = 0
    last_accepted_step: int = -1


@dataclass(frozen=True)
class LoginResult:
    allowed: bool
    reason: str


class DemoMFA:
    """TOTP second-factor gate with per-account throttling (in memory only)."""

    def __init__(self) -> None:
        self._accounts: dict[str, _Account] = {}

    def enroll(self, username: str, password: str, secret: str | None = None) -> str:
        if username in self._accounts or not username or len(password) < 8:
            raise ValueError("Duplicate account, empty username or short password")
        chosen = secret or generate_secret()
        _secret_bytes(chosen)  # validate before storing
        salt = secrets.token_bytes(16)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
        self._accounts[username] = _Account(salt, digest, chosen)
        return chosen

    def login(self, username: str, password: str, code: str, now: int) -> LoginResult:
        account = self._accounts.get(username)
        if account is None:
            return LoginResult(False, "denied")
        if now < account.locked_until:
            return LoginResult(False, "temporarily_locked")

        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), account.salt, 200_000)
        password_ok = hmac.compare_digest(digest, account.password_hash)
        valid_step = -1
        if isinstance(code, str) and len(code) == 6 and code.isascii() and code.isdigit():
            for step in (now // 30 - 1, now // 30, now // 30 + 1):
                if step >= 0 and step > account.last_accepted_step and hmac.compare_digest(
                    hotp(account.secret, step), code
                ):
                    valid_step = step
                    break
        if password_ok and valid_step >= 0:
            account.failed = 0
            account.last_accepted_step = valid_step
            return LoginResult(True, "mfa_verified")
        account.failed += 1
        if account.failed >= 5:
            account.locked_until = now + 300
            account.failed = 0
            return LoginResult(False, "temporarily_locked")
        return LoginResult(False, "denied")
