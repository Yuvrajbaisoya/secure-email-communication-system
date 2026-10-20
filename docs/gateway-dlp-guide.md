# Secure Email Gateway and Data Loss Prevention Guide

## What this repository actually implements

The [gateway policy emulator](../secure_email_lab/gateway.py) runs entirely offline: it parses synthetic email bytes and returns \`allow\`, \`quarantine\` or \`block\` with coded policy reasons and a SHA-256 fingerprint. No email is delivered and the code is **not** an SMTP gateway, antivirus, sandbox, phishing classifier, reputation engine or enterprise DLP product.

### Policy matrix used by the lab

| Signal | Direction | Test action | Reason |
|---|---|---|---|
| Normal sample message | Inbound | Allow | No flagged lab indicator |
| \`X-SIMULATED-PHISHING\` in subject | Inbound | Quarantine | Synthetic phishing marker |
| \`.exe\`, \`.js\`, \`.scr\` and similar attachment filename | Inbound | Quarantine | Risky filename extension |
| Trusted independently supplied DMARC rejection | Inbound | Quarantine | Receiver authentication policy |
| \`CONFIDENTIAL-DEMO-12345\` to outside \`example.test\` | Outbound | Block | Synthetic external DLP marker |
| The same synthetic marker to internal test recipient | Outbound | Allow | Deliberately scoped external-disclosure rule |
| Opaque S/MIME/PGP MIME content to outside domain | Outbound | Quarantine | Body cannot be inspected |
| Oversized sample (>256 KiB) | Either | Quarantine | Offline parser size limit |

**Careful:** Extension checks and subject markers are **toy policies**, not malware/phishing detection. Real gateways require updated threat feeds, content-type/magic-byte analysis, decoding and evasions defense, sender reputation, quarantine workflows and continuous monitoring.

### Reproduce

\`\`\`bash
python -m unittest tests.test_gateway -v
python -m practical.run_labs
\`\`\`

Observed result: [CI PASS, security suite](https://github.com/Yuvrajbaisoya/secure-email-communication-system/actions/runs/39389041933); see [gateway/DLP evidence](../practical/evidence/T-SEG-DLP-01/EVIDENCE.md).

## Production evaluation design (not deployed)

1. Choose an authorized mail tenant or isolated lab MTA with outbound relay restrictions.
2. Enable vendor anti-spam, attachment/malware protection, URL inspection, SPF/DKIM/DMARC validation, and operator alerts.
3. Start quarantine policy monitoring with deliberately harmless synthetic messages, measure false positives, and restrict who may release mail.
4. Set DLP classifications, destination scopes and exception workflows before enabling blocks.
5. Inspect outgoing plaintext **before E2EE** on approved endpoints; otherwise treat encrypted content as opaque.
6. Limit event logs to justified metadata, redacted snippets where lawful, reason codes, and retention periods.
7. Test safe rollback, reporting, suspicious-message triage and recovery with signed-off owners.

## Out of scope / risks

The lab does not unpack archives, scan embedded links for reputation, check real confidential data, read encrypted message bodies, evaluate anti-malware signatures, implement active SMTP quarantine or enforce organizational policy. Never use it to filter real mail. See [deployment checklist](deployment-checklist.md) for verification tasks.
