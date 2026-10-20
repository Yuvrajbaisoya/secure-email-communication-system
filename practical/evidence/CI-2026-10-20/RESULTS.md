# Verified GitHub Actions Results — 20 October 2026

**CI run:** [Offline email security labs — run 39389957335](https://github.com/Yuvrajbaisoya/secure-email-communication-system/actions/runs/39389957335)  
**Code commit:** `c641f4489b4b0f502304c8d5cf31cb6daed257eb`  
**Job:** `offline-labs` — GitHub-hosted Ubuntu, Python 3.12  
**GitHub Actions conclusion:** `success` (checked via run status and successful job steps)

## Captured observations

```text
Ran 37 tests in 1.275s
OK
"passed": 9
"total": 9
"production_deployment_verified": false
PASS: Bob decrypted the encrypted message; plaintext matched.
PASS: Alice's OpenPGP signature verified.
PASS: Tampering was detected; modified message signature rejected.
Verification successful
Verification successful
PASS: Alice's S/MIME signature verified against the lab certificate.
PASS: Bob decrypted the AES-256 S/MIME message; content matched.
```

The four separate stages — unit tests, integrated Python demo, GnuPG OpenPGP and OpenSSL S/MIME — completed successfully in the same job. The source of this result is **actual GitHub Actions job logs**, not a generated prediction. Details by control:

- [SPF/DKIM/DMARC](../T-AUTH-01/EVIDENCE.md)
- [TOTP MFA](../T-MFA-01/EVIDENCE.md)
- [Gateway and synthetic DLP](../T-SEG-DLP-01/EVIDENCE.md)
- [OpenPGP Mac lab](../T-PGP-01/EVIDENCE.md)
- [S/MIME Mac lab](../T-SMIME-01/EVIDENCE.md)

No production domain, tenant or gateway was verified in this run. All signing keys and messages were synthetic test fixtures.

Earlier successful CI baseline: [run 39389041933](https://github.com/Yuvrajbaisoya/secure-email-communication-system/actions/runs/39389041933). The later green run additionally checked bad OpenPGP signatures.
