# Evidence Register and Test Plan

**Snapshot:** 20 October 2026  
**Independent CI evidence:** [Offline email security labs — 37/37 tests, 9/9 integrated checks, two crypto demos PASS](https://github.com/Yuvrajbaisoya/secure-email-communication-system/actions/runs/39389041933)  
**Scope:** Synthetic, offline and authorized GitHub CI execution only.

| ID | Control / expected behavior | Evidence | Lab result | Live deployment |
|---|---|---|---|---|
| T-HASH-01 | Modified sample message produces different SHA-256 | [Hash fixture report](evidence/T-HASH-01/EVIDENCE.md) | PASS (synthetic file test) | N/A |
| T01 | Disposable OpenPGP signing/encryption key generation | [T-PGP-01](evidence/T-PGP-01/EVIDENCE.md) | PASS | Not deployed |
| T02 | OpenPGP encrypted message roundtrip | [T-PGP-01](evidence/T-PGP-01/EVIDENCE.md) | PASS | Not deployed |
| T03 | OpenPGP signature verifies | [T-PGP-01](evidence/T-PGP-01/EVIDENCE.md) | PASS for valid signature; deliberate tamper/revocation test remains open | Not deployed |
| T04 | S/MIME signing, encrypting, verifying and decrypting | [T-SMIME-01](evidence/T-SMIME-01/EVIDENCE.md) | PASS | Not deployed |
| T05 | SPF permitted/denied test-sender IP | [T-AUTH-01](evidence/T-AUTH-01/EVIDENCE.md) | PASS in bounded offline evaluator | No actual DNS |
| T06 | DKIM RSA signature checks; tampered header/body rejected | [T-AUTH-01](evidence/T-AUTH-01/EVIDENCE.md) | PASS in fixed-format lab | No actual DNS/MTA |
| T07 | DMARC alignment and staged reject/quarantine/none outcomes | [T-AUTH-01](evidence/T-AUTH-01/EVIDENCE.md) | PASS in offline evaluator | No actual DMARC reports |
| T08 | Password plus TOTP, wrong/replayed/expired OTP and lockout | [T-MFA-01](evidence/T-MFA-01/EVIDENCE.md) | PASS in in-memory demo | No provider enforcement |
| T09 | Synthetic suspicious mail and risky filename quarantined | [T-SEG-DLP-01](evidence/T-SEG-DLP-01/EVIDENCE.md) | PASS in policy emulator | No deployed SEG or malware scanner |
| T10 | Synthetic marker on external mail blocked; encrypted mail reviewed | [T-SEG-DLP-01](evidence/T-SEG-DLP-01/EVIDENCE.md) | PASS in policy emulator | No deployed DLP |

## Result conventions

- **PASS — lab:** Test was actually executed in a synthetic fixture or CI runner and assertions passed.
- **BLOCKED / not deployed:** Needs owned domain, production-like identity/mail platform, consent, or infrastructure that was not supplied.
- **PASS — production:** Requires separate implementation evidence; **none is claimed here**.
- **NOT TESTED:** Work not demonstrated (e.g., real email deliveries, live TLS, monitoring operations, and OpenPGP key revocation).

## Reproduction

\`\`\`bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m practical.run_labs
bash practical/openpgp_lab.sh
bash practical/smime_lab.sh
\`\`\`

## Evidence quality rules

For each later real-world pilot test, record date/time, owner, domain authorization, software versions, setup, commands, observed pass/fail, sanitized screenshots or logs, remediation, rollback and residual risk. Never upload real account credentials, certificate private keys, MFA secrets, client content, or unmanaged samples.

See [deployment checklist](../docs/deployment-checklist.md) for all controls not yet validated on actual services.
