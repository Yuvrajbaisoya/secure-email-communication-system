# T-SMIME-01 — S/MIME Signing, Encryption and Verification

**Status:** PASS — user-executed local lab (terminal transcript supplied by user)  
**Platform:** macOS (Apple Silicon), Homebrew OpenSSL 3.5.9  
**Script:** [practical/smime_lab.sh](../../smime_lab.sh)  
**Tested revision:** `213c85f`  
**Identities:** Alice <alice@example.test> and Bob <bob@example.test> (synthetic lab certificates)

## Test method

The script generates disposable self-signed certificates and private keys for Alice and Bob; signs a synthetic RFC 5322-style message with Alice's key; verifies the signature against the explicit Alice lab certificate trust anchor; encrypts the signed S/MIME envelope for Bob using AES-256; decrypts it with Bob's private key; and verifies both the signature and byte-for-byte content again. The script removes temporary private keys and artifacts when it exits.

## User-provided successful terminal output

```text
From https://github.com/Yuvrajbaisoya/secure-email-communication-system
   8367734..213c85f  main -> origin/main
Updating 8367734..213c85f
Fast-forward
 practical/smime_lab.sh | 12 ++++++------
 1 file changed, 6 insertions(+), 6 deletions(-)
OpenSSL 3.5.9 29 Sep 2026 (Library: OpenSSL 3.5.9 29 Sep 2026)
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
Exit code: 0
```

## Findings

- **PASS:** Signature verification succeeded before and after encryption/decryption.
- **PASS:** Byte comparison confirmed the recovered content matched the original synthetic message.
- **PASS:** Script completed with exit code 0.
- **Scope:** All cryptographic keys were generated for an offline, synthetic lab. This does not establish CA identity assurance, real mail-server integration, external delivery, recipient key isolation on separate machines, or enterprise policy compliance.
- **Provenance:** This report transcribes the user's Mac Terminal output; it is not an independently witnessed remote run.

## Earlier failure and remediation

The initial test at revision `8367734` returned `Verification successful` but failed a raw byte comparison due to S/MIME canonicalization differences (`message.eml verified.eml differ: char 25, line 1`). Revision `213c85f` changed the synthetic input to CRLF and enabled binary preservation in OpenSSL S/MIME commands. The subsequent user-reported run passed.

## Reproduce

```bash
git pull origin main
bash practical/smime_lab.sh
echo "Exit code: $?"
```
