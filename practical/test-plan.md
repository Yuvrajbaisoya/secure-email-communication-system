# Practical Test Plan and Evidence Register

All work is performed against accounts, domains and infrastructure owned or explicitly authorized for this project. **Do not claim an implementation is complete until the test is performed.**

| ID | Practical | Expected evidence | Status |
|---|---|---|---|
| T01 | OpenPGP key generation and public-key exchange | Redacted key fingerprints | Pending |
| T02 | OpenPGP encrypted message and decryption | Sender/recipient screenshots with dummy content | Pending |
| T03 | OpenPGP signed message and tamper verification | Valid and invalid signature results | Pending |
| T04 | S/MIME signing and encryption | Test certificates and verification screenshots | Pending |
| T05 | SPF validation | TXT lookup and receiver authentication result | Pending |
| T06 | DKIM signing validation | DKIM-Signature header and validation result | Pending |
| T07 | DMARC alignment | Policy DNS lookup and aggregate/report example | Pending |
| T08 | MFA enforcement | Redacted account security screenshot | Pending |
| T09 | Gateway spam/malware filtering | Safe test fixtures, policy and log | Pending |
| T10 | DLP synthetic data blocking | Dummy sensitive-data sample and blocked-event log | Pending |

## Test record template
- Test ID and date:
- Environment and software versions:
- Preconditions:
- Steps performed:
- Expected outcome:
- Actual outcome:
- Result: PASS / FAIL / BLOCKED
- Evidence path (redacted):
- Remediation / limitations:

## Important technical distinctions
- TLS protects a connection/hop; it is not end-to-end email encryption.
- SPF/DKIM/DMARC authenticate domains and message handling; they do not establish the human sender's identity.
- Digital signatures provide integrity and cryptographic signer verification, subject to key/certificate trust.
- Hashing alone does not authenticate a message; use signatures or a keyed MAC.
- End-to-end encrypted message bodies cannot ordinarily be inspected by a gateway for DLP without endpoint-side controls or decryption.
