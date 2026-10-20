"""Offline secure-email-gateway + DLP policy emulator using synthetic signals.

Not an SMTP service, antivirus engine, reputation feed, or production DLP
product. Never claim malware detection or enterprise deployment from these tests.
"""
from dataclasses import dataclass
from email import policy
from email.parser import BytesParser
from hashlib import sha256
from pathlib import PurePath

MAX_MESSAGE_BYTES = 256 * 1024
DLP_MARKERS = ("CONFIDENTIAL-DEMO-12345", "DEMO-SECRET-2026")
BLOCKED_EXTENSIONS = (".exe", ".scr", ".js", ".vbs", ".bat", ".cmd", ".ps1")


@dataclass(frozen=True)
class GatewayDecision:
    action: str
    reasons: tuple[str, ...]
    sha256: str  # audit fingerprint, not message content


def _external(recipients: list[str], internal_domain: str) -> bool:
    from email.utils import getaddresses
    addresses = getaddresses(recipients)
    # Unknown or missing recipients should not bypass outbound DLP.
    if not addresses:
        return True
    return any(not addr.lower().endswith("@" + internal_domain.lower())
               for _, addr in addresses)


def inspect(
    raw_message: bytes, *, direction: str, internal_domain: str = "example.test",
    trusted_dmarc_result: str | None = None,
) -> GatewayDecision:
    """Evaluate sanitized policy actions without network access or email delivery.

    trusted_dmarc_result MUST come from an independent verifier, never from
    untrusted incoming Authentication-Results headers.
    """
    if direction not in {"inbound", "outbound"}:
        raise ValueError("direction must be inbound or outbound")
    digest = sha256(raw_message).hexdigest()
    if len(raw_message) > MAX_MESSAGE_BYTES:
        return GatewayDecision("quarantine", ("message_size_limit",), digest)
    try:
        message = BytesParser(policy=policy.default).parsebytes(raw_message)
    except Exception:
        return GatewayDecision("quarantine", ("malformed_message",), digest)

    reasons: list[str] = []
    if direction == "inbound" and trusted_dmarc_result == "reject":
        reasons.append("trusted_dmarc_reject")
    if direction == "inbound" and "X-SIMULATED-PHISHING" in str(message.get("Subject", "")):
        reasons.append("synthetic_phishing_indicator")

    content_parts: list[str] = []
    has_opaque_content = False
    for part in message.walk():
        if part.is_multipart():
            continue
        filename = part.get_filename()
        if filename:
            clean_name = PurePath(filename.replace("\\", "/")).name.lower()
            if clean_name.endswith(BLOCKED_EXTENSIONS):
                reasons.append("risky_attachment_extension")
        media_type = part.get_content_type()
        if media_type in {"application/pkcs7-mime", "application/pgp-encrypted"}:
            has_opaque_content = True
        if media_type == "text/plain" and not filename:
            try:
                payload = part.get_content()
                content_parts.append(payload if isinstance(payload, str) else payload.decode("utf-8", "replace"))
            except Exception:
                reasons.append("unreadable_text")
    text = "\n".join(content_parts)
    outbound_external = direction == "outbound" and _external(
        message.get_all("To", []) + message.get_all("Cc", []) + message.get_all("Bcc", []),
        internal_domain,
    )
    if outbound_external and any(marker in text for marker in DLP_MARKERS):
        reasons.append("synthetic_dlp_marker_external")
    if outbound_external and has_opaque_content:
        reasons.append("encrypted_content_not_inspectable")

    unique = tuple(sorted(set(reasons)))
    if any(reason in unique for reason in ("synthetic_dlp_marker_external",)):
        action = "block"
    elif unique:
        action = "quarantine"
    else:
        action = "allow"
    return GatewayDecision(action, unique, digest)
