# Reproducible Practical Labs

## Tested implementations

The project includes **two independent kinds of evidence**:

1. **Mac user terminal logs** for OpenPGP ([T-PGP-01](evidence/T-PGP-01/EVIDENCE.md)) and S/MIME ([T-SMIME-01](evidence/T-SMIME-01/EVIDENCE.md)).
2. **GitHub Actions runner logs** ([successful run](https://github.com/Yuvrajbaisoya/secure-email-communication-system/actions/runs/39389957335)) for 37 unit tests, 9 integrated offline checks and the two cryptographic shell labs. Authentication, MFA and gateway/DLP evidence links below point to this CI execution.

These are not third-party mail service tests and do not prove production enforcement.

## Requirements

- Python 3.12+ and `python -m pip install -r requirements.txt`
- GnuPG 2.x (`gpg`, `gpgconf`) for OpenPGP
- OpenSSL 3.x for S/MIME
- All fixtures use reserved domains, reserved IP blocks and disposable synthetic data.

## Run

From repository root:

```bash
python -m unittest discover -s tests -v
python -m practical.run_labs
bash practical/openpgp_lab.sh
bash practical/smime_lab.sh
```

OpenPGP uses a short isolated temporary GnuPG home because GPG agent socket paths can be too long on macOS. S/MIME chooses Homebrew OpenSSL 3 if installed. Both shell scripts delete disposable credentials when they exit.

## Evidence register

- [T-HASH-01 — SHA-256 fixture](evidence/T-HASH-01/EVIDENCE.md)
- [T-PGP-01 — GnuPG sign/encrypt/decrypt](evidence/T-PGP-01/EVIDENCE.md)
- [T-SMIME-01 — OpenSSL sign/encrypt/decrypt](evidence/T-SMIME-01/EVIDENCE.md)
- [T-AUTH-01 — offline SPF, DKIM and DMARC](evidence/T-AUTH-01/EVIDENCE.md)
- [T-MFA-01 — offline TOTP MFA](evidence/T-MFA-01/EVIDENCE.md)
- [T-SEG-DLP-01 — offline gateway/DLP](evidence/T-SEG-DLP-01/EVIDENCE.md)
- [Status by test ID](test-plan.md)

## Important limitations

- SPF is a **bounded** IPv4/IPv6 and `all` mechanism evaluator; it does not make DNS lookups or implement `include`, `redirect`, HELO checks or RFC lookup limits.
- The DKIM fixture generates real RSA-SHA256 signatures for fixed-format, single-signer ASCII test messages; **it is not a full DKIM receiver** and doesn't query selector DNS.
- DMARC uses an **explicit organizational-domain value** to avoid pretending to implement public suffix discovery; it does not process aggregate reports or ARC.
- MFA is an in-memory TOTP demo, **not deployed MFA** on an email account. Passkeys/security keys should be preferred in actual providers.
- Gateway is a **policy emulator**, not an SMTP listener, antivirus or URL-reputation service. DLP only recognizes synthetic markers in readable plaintext. For encrypted messages it flags lack of visibility instead of claiming to inspect content.
- Tests must not be used as an excuse to touch any domain, account or infrastructure without ownership/permission.
