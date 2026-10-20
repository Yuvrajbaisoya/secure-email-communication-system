# Encryption and Authentication Plan

## OpenPGP lab (Thunderbird)
1. Create two **test-only** mail accounts controlled by the researcher.
2. Install an up-to-date Thunderbird version. For each account open Account Settings > End-To-End Encryption > Add Key > Create a new OpenPGP Key.
3. Exchange **public** keys through a trusted channel. Independently compare full fingerprints before accepting identities.
4. Send a dummy encrypted message A -> B; confirm B decrypts it and a third party without the private key cannot.
5. Send a signed message; verify signature status and record the displayed fingerprint.
6. Revoke a test key and document how the client responds. Never upload private keys, passphrases or sensitive emails.

## S/MIME lab
1. Obtain **test-only** certificates for each test mailbox, with appropriate email identity and key usage. Self-signed certificates are suitable only for an explicitly documented isolated lab; they are not publicly trusted.
2. Import each certificate and private key locally in the client; exchange recipients' public certificates.
3. Sign a dummy email and verify certificate trust and sender identity.
4. Encrypt a dummy email to a recipient whose certificate is available; verify decryption and behavior with an untrusted certificate.
5. Capture redacted screenshots and describe trust limitations.

## Transport protection
Use authenticated SMTP submission over TLS (typically port 587 with STARTTLS or 465 implicit TLS), IMAP over TLS where applicable, and validated server certificates. Do not describe TLS as E2EE.

## SPF example (illustrative only)
```dns
example.test. IN TXT "v=spf1 ip4:192.0.2.10 -all"
```
The reserved example domain/IP are placeholders and **must not** be deployed unchanged. Enumerate actual authorized senders; avoid multiple SPF TXT records.

## DKIM example (illustrative only)
```dns
selector1._domainkey.example.test. IN TXT "v=DKIM1; k=rsa; p=REPLACE_WITH_PUBLIC_KEY"
```
Generate keys using the chosen mail service, keep the private signing key secret, configure selector rotation and validate signing headers.

## DMARC staged rollout
```dns
_dmarc.example.test. IN TXT "v=DMARC1; p=none; rua=mailto:dmarc-reports@example.test"
```
Use a real, authorized reporting mailbox for production. Review aggregate reports and SPF/DKIM alignment; advance to `p=quarantine` and then `p=reject` only when legitimate flows pass.

## Verification
```bash
dig TXT example.test
dig TXT selector1._domainkey.example.test
dig TXT _dmarc.example.test
```
Inspect authentication results in messages received through an authorized test mailbox. DNS presence alone does not prove DKIM signing or DMARC alignment.

## MFA
Enforce MFA for every mailbox and administrator, prefer FIDO2/passkeys where supported, disable legacy authentication, secure recovery methods and test enrollment/recovery with a test user.

## Evidence
Record software versions, domain ownership, redacted DNS outputs, signed/encrypted message outcomes, and failure cases in `practical/test-plan.md`.
