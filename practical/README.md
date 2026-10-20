# Practical Lab Execution Guide

These are **reproducible instructions**, not fabricated evidence of a completed deployment.

## Lab scope
Use two test mailboxes, current Thunderbird, optional owned test domain and isolated gateway VM. Never publish secrets or private keys.

## Execution order
1. Follow [encryption and authentication plan](../docs/encryption-authentication-plan.md) for OpenPGP, S/MIME, DNS and MFA.
2. Follow [integrity strategy](../docs/integrity-strategy.md) for signed email and SHA-256 demonstration.
3. Follow [gateway/DLP guide](../docs/gateway-dlp-guide.md) for isolated gateway tests.
4. Update [test plan](test-plan.md) with PASS / FAIL / BLOCKED and redacted evidence.

## Suggested evidence naming
`evidence/T01-openpgp-key-fingerprint-redacted.png`, `evidence/T02-encrypted-mail-redacted.png`, etc. Use synthetic message content and do not include secret material.

## Acceptance criteria
Every claimed completed control must have reproducible configuration, actual observed results and a limitation statement. If no domain or mail infrastructure is available, mark the relevant tests BLOCKED rather than claiming they passed.
