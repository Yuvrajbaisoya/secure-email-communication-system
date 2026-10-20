# Email Integrity and Tamper-Resistance Strategy

## Goals
Detect unauthorized changes to message content and provide verifiable evidence of signing key ownership. No email system can guarantee absolute tamper-proofing.

## Controls
- OpenPGP and S/MIME digital signatures cryptographically bind message content to a signing key.
- SHA-256 can fingerprint files for comparison, but an attacker can replace an unsigned hash; pair hashes with trusted signatures.
- DKIM protects selected headers and message body across SMTP transit, subject to canonicalization and forwarding effects; it is not an end-user signature.
- Store logs with controlled access, retention and audit trails.

## Reproducible local hash demonstration
```bash
printf 'Approved dummy message\n' > original.txt
shasum -a 256 original.txt
cp original.txt modified.txt
printf 'Changed\n' >> modified.txt
shasum -a 256 modified.txt
```
Expected: different SHA-256 digests. This alone does **not** authenticate the sender.

## Signed email test
1. Create an OpenPGP key for a test mailbox.
2. Send a signed dummy message and verify the public key fingerprint out of band.
3. Confirm the recipient sees a valid signature.
4. Alter a copy of signed content in an isolated test fixture and confirm signature verification fails.
5. Record actual observed results; do not label this PASS before executing.

## Key lifecycle
Generate strong keys using maintained software, protect private keys with local device security, restrict backups, document revocation and certificate expiration, and rotate keys when compromised.
