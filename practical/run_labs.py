#!/usr/bin/env python3
"""Generate a JSON result summary using live, disposable offline lab operations."""
import json
from email.message import EmailMessage

from secure_email_lab.authentication import evaluate_dmarc, evaluate_spf
from secure_email_lab.dkim_lab import generate_lab_key, sign, verify
from secure_email_lab.gateway import inspect
from secure_email_lab.mfa import DemoMFA, totp


def main() -> None:
    checks = {}
    spf = evaluate_spf("192.0.2.10", "v=spf1 ip4:192.0.2.10 -all")
    checks["spf_authorized_ip"] = spf == "pass"
    checks["spf_unauthorized_ip"] = (
        evaluate_spf("198.51.100.10", "v=spf1 ip4:192.0.2.10 -all") == "fail"
    )
    unsigned = (b"From: alice@example.test\r\nTo: bob@example.test\r\n"
                b"Subject: Synthetic DKIM\r\n\r\nLab message.\r\n")
    key = generate_lab_key()
    signed = sign(unsigned, key)
    checks["dkim_rsa_signature"] = verify(signed, key.public_key())
    checks["dkim_tampering_rejected"] = not verify(
        signed.replace(b"Lab message.", b"Altered message."), key.public_key()
    )
    dmarc = evaluate_dmarc(
        from_domain="example.test", envelope_domain="mail.example.test",
        spf_result=spf, dkim_domain="example.test", dkim_result="pass",
        dmarc_record="v=DMARC1; p=reject", organizational_domain="example.test"
    )
    checks["dmarc_alignment"] = dmarc.result == "pass"
    mfa = DemoMFA()
    secret = mfa.enroll("alice", "DummyPassword123")
    code = totp(secret, 1200)
    checks["mfa_totp_verified"] = mfa.login("alice", "DummyPassword123", code, 1200).allowed
    checks["mfa_totp_replay_rejected"] = not mfa.login(
        "alice", "DummyPassword123", code, 1200
    ).allowed
    outbound = EmailMessage()
    outbound["From"] = "alice@example.test"
    outbound["To"] = "bob@external.example"
    outbound["Subject"] = "Synthetic DLP"
    outbound.set_content("CONFIDENTIAL-DEMO-12345")
    checks["gateway_dlp_block"] = inspect(outbound.as_bytes(), direction="outbound").action == "block"
    checks["gateway_clean_allow"] = inspect(
        unsigned, direction="inbound"
    ).action == "allow"
    output = {
        "scope": "isolated_synthetic_offline_lab",
        "production_deployment_verified": False,
        "tests": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
