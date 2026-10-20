# Threat Model — Secure Email Communication System

**System:** Hypothetical consulting organization; reference design and isolated lab only.  
**Threat modeling scope:** Mail identities, domain authentication, encrypted content, user access, gateway enforcement, outbound disclosures and observability.

## Assets and trust boundaries

- **Assets:** Mailboxes, message content, signing/encryption keys, IdP accounts, organizational domain/DNS, gateway configuration, audits, private reports.
- **Adversaries:** External spoofers/phishers, compromised mail users, unauthorized insiders, malicious attachment senders and accidental recipients.
- **Boundaries:** Internet → authorized mail gateway; email provider → identity platform; mail server → managed client; client plaintext → encrypted message; internal sender → external recipient; policy decisions → audit store.

## STRIDE-oriented threats and controls

| Category | Scenario | Proposed safeguards | Lab demonstration | Residual limitation |
|---|---|---|---|---|
| Spoofing | Attacker forges apparent organizational sender | SPF/DKIM/DMARC alignment, phishing training | Offline SPF/DKIM/DMARC tests | Must configure owned DNS and MTA |
| Tampering | Sender/body text altered en route | S/MIME/OpenPGP signatures, DKIM, hashes | Signed-message verification and DKIM tamper tests | Requires reliable sender key/cert trust |
| Repudiation | User denies sending a message | Signed mail, audit policy | Signature proof of **test key** only | Keys may be stolen/shared; no legal non-repudiation claim |
| Information disclosure | Confidential file sent outside company | Client classification, endpoint DLP, encryption | Synthetic marker block and opaque message flag | Toy DLP misses real sensitive data |
| Denial of service | Attachment flood or oversized email | Provider quotas, gateway limits, rate limiting | Simple size-limit policy test | No live SMTP capacity testing |
| Elevation of privilege | Stolen password allows mailbox takeover | IdP MFA/passkeys, least privilege, recovery policy | TOTP/replay/lockout demo | No real IdP enforcement or device binding |
| Phishing/malware | Manipulated links and unsafe files | Managed SEG, reputation, AV and training | Synthetic phishing marker, risky extension policy | No AV or reputation engine |
| Supply-chain / operational | Outdated library or leaked private key | Automated tests, dependency updates, secret handling, code review | Ephemeral keys and CI | Continuous patching/monitoring outside lab |

## Abuse cases

- **Spoofed Authentication-Results header:** The gateway model ignores untrusted received header text and uses an explicit independently supplied DMARC result.
- **MFA replay:** Previously accepted TOTP step cannot be reused.
- **Forged DKIM signature or modified body:** Genuine RSA signature verification fails if signed material differs.
- **DLP evasion through encryption:** Simulated opaque outbound content is held for review instead of labeled clean.
- **DMARC bypass via lookalike domain:** Relaxed domain alignment uses an explicit organization root and label boundary checks.

## Assurance boundaries

Threat mitigations demonstrated by these tests are **narrowly scoped to the laboratory**. They do not validate TLS configuration, DNS routing, credential recovery, rate limits across multiple servers, actual antivirus detections, third-party providers or incident response staffing. Document additional risks and exceptions before operating with real data.
