# User-Supplied Mac Terminal Evidence — 20 October 2026

**Evidence source:** Four screenshots uploaded by the project owner in ChatGPT on 20 October 2026, showing local terminal executions. This file records the visible results as a faithful transcription; **the original PNG screenshots are not stored in this GitHub repository**.

**Evidence scope:** Local/offline synthetic security demonstrations; not production DNS, live mail transport, hosted identity MFA enforcement, or deployed email gateway.

## Screenshot 01 — Python unit tests (`01_unit_tests.png`)

**Command:** `python -m unittest discover -s tests -v`

Visible end of output:

```text
test_rfc6238_known_sha1_vector (test_mfa.TestTOTP.test_rfc6238_known_sha1_vector) ... ok
test_valid_password_and_totp (test_mfa.TestTOTP.test_valid_password_and_totp) ... ok
test_wrong_password_denied (test_mfa.TestTOTP.test_wrong_password_denied) ... ok
----------------------------------------------------------------------
Ran 37 tests in 1.306s

OK
```

**Observed:** 37 unit tests completed successfully on the user's machine.

## Screenshot 02 — Integrated synthetic labs (`02_integrated_labs.png`)

**Command:** `python -m practical.run_labs`

Visible JSON result:

```json
{
  "passed": 9,
  "production_deployment_verified": false,
  "scope": "isolated_synthetic_offline_lab",
  "tests": {
    "dkim_rsa_signature": true,
    "dkim_tampering_rejected": true,
    "dmarc_alignment": true,
    "gateway_clean_allow": true,
    "gateway_dlp_block": true,
    "mfa_totp_replay_rejected": true,
    "mfa_totp_verified": true,
    "spf_authorized_ip": true,
    "spf_unauthorized_ip": true
  },
  "total": 9
}
```

**Observed:** All 9 integration checks true. Output explicitly states `production_deployment_verified: false`.

## Screenshot 03 — OpenPGP cryptographic lab (`03_openpgp.png`)

**Command:** `bash practical/openpgp_lab.sh`

Visible positive and negative verification results:

```text
==> Encrypting for Bob and signing as Alice
==> Decrypting and verifying
PASS: Bob decrypted the encrypted message; plaintext matched.
PASS: Alice's OpenPGP signature verified.

==> Checking that a modified message fails signature verification
PASS: Tampering was detected; modified message signature rejected.
NOTE: Disposable test keys and ciphertext were deleted on exit.
```

**Observed:** Encryption/decryption, valid signature verification, and deliberate tamper rejection all passed.

## Screenshot 04 — S/MIME cryptographic lab (`04_smime.png`)

**Command:** `bash practical/smime_lab.sh`

Visible OpenSSL version and results:

```text
OpenSSL 3.0.13 30 Jan 2024 (Library: OpenSSL 3.0.13 30 Jan 2024)
==> Creating disposable Alice and Bob certificates
==> Signing message with Alice's private key
==> Verifying Alice's signature with explicit lab trust anchor
Verification successful
==> Encrypting signed S/MIME for Bob
==> Decrypting with Bob's private key
Verification successful
PASS: Alice's S/MIME signature verified against the lab certificate.
PASS: Bob decrypted the AES-256 S/MIME message; content matched.
NOTE: Certificates are self-signed lab fixtures; no public CA or real email transport tested.
NOTE: Disposable private keys were deleted on exit.
```

**Observed:** Successful signing/verification and AES-256 S/MIME encryption/decryption with disposable test identities.

## Evidence provenance and limitations

- These four results are **user-provided screenshots** of local executions, transcribed into this Markdown record. The screenshots have not been independently authenticated or timestamped by the operating system.
- The OpenSSL 3.0.13 version shown in screenshot 04 differs from an earlier Mac execution recorded with OpenSSL 3.5.9. They are **separate executions**; do not combine their software-version claims.
- Local screenshot evidence complements independently executed [GitHub Actions CI run 39389957335](https://github.com/Yuvrajbaisoya/secure-email-communication-system/actions/runs/39389957335), which passed the same lab categories.
- This record does not prove real domain ownership, DNS publication, live mail transport, real mailbox MFA or enterprise gateway deployment.
