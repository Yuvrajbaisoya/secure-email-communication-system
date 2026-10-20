# Research Report: Implementing a Secure Email Communication System

**Organization:** First Quadrant Labs — project context only; its infrastructure was not accessed  
**Research subject:** Defense-in-depth email security design, isolated implementation and test evidence  
**Report status:** Implemented offline lab; not a deployed organizational email service  
**Report date:** 20 October 2026  
**Original assignment deadline:** 11 October 2026

## Executive summary

Modern organizational email must withstand account compromise, sender-domain spoofing, phishing, malicious attachments, message interception and accidental disclosure. This research project develops a layered reference architecture and demonstrates selected controls in a reproducible offline laboratory. Controls span OpenPGP and S/MIME cryptography, SHA-256, SPF/DKIM/DMARC, TOTP-based multifactor access checks, secure-email-gateway policy decisions and Data Loss Prevention (DLP) logic.

Implementation code, synthetic fixtures, negative security tests and governance deliverables are versioned in GitHub. The independently recorded [GitHub Actions run](https://github.com/Yuvrajbaisoya/secure-email-communication-system/actions/runs/39389957335) completed **37/37 unit tests**, **9/9 integrated offline checks**, and both OpenPGP and S/MIME shell labs. Earlier successful Mac terminal demonstrations for OpenPGP and S/MIME are separately documented. **These results do not constitute a production rollout or live domain/mailbox verification.**

## 1. Background and objectives

Email security is more than message encryption. Mail transit crosses multiple trust boundaries; sending domains may be spoofed; human credentials are phishable; attachments and links can be weaponized; and staff can inadvertently transmit confidential content. The project's goals were to design practical defenses, demonstrate their behavior using test-only assets, document limitations, and establish the steps required for authorized future deployment.

Key security requirements are confidentiality, integrity, authentication, access control, availability, and accountability. Implementations are grouped into cryptography, sender-domain verification, identity controls, filtering, data protection, monitoring, and human processes.

## 2. Assessment method and system boundaries

The supplied project describes a hypothetical consulting organization but did not provide live Microsoft 365/Google Workspace tenants, domain/DNS ownership, functioning SMTP gateway or security telemetry. Accordingly, no production scans or configuration changes were attempted. The [infrastructure assessment](infrastructure-assessment.md) is a **baseline plan and risk hypotheses**, not a certified assessment of a real business.

The laboratory uses synthetic addresses at `example.test`, documentation IP ranges (`192.0.2.0/24`, `198.51.100.0/24` and `2001:db8::/32`), disposable GnuPG keyrings, self-signed S/MIME certificates and a newly generated ephemeral DKIM RSA key. No real user mail is transmitted.

## 3. Proposed layered architecture

See the [architecture design](architecture-design.md) and [threat model](threat-model.md). Inbound mail should pass through a managed MX/service and authenticated checks, a gateway with current security intelligence and policy enforcement, and restricted mailboxes. End users authenticate through an organizational identity provider with phishing-resistant MFA where available. End-to-end encryption and digital signatures are applied and verified on managed endpoints; sensitive outbound content is classified and inspected **before** encryption. Restricted logs support response and audit.

E2EE and centralized gateway DLP create a visibility trade-off. The proposed resolution is endpoint/pre-encryption DLP, not unauthorized decryption of users' private communication.

## 4. Implementation and verification

### 4.1 OpenPGP

`practical/openpgp_lab.sh` creates temporary Alice and Bob keys, signs a synthetic message, encrypts it for Bob, decrypts it, compares plaintext and checks GnuPG signature markers. A macOS GPG agent socket-path problem was corrected, and the user reported an exit-code-0 successful run. The shell test passed in GitHub Actions; an additional later CI execution also verified a detached-signature tampering attempt returned GnuPG `BADSIG`. See [T-PGP-01](../practical/evidence/T-PGP-01/EVIDENCE.md).

### 4.2 S/MIME

`practical/smime_lab.sh` uses disposable self-signed certificates for Alice and Bob, a signed message and an AES-256-encrypted S/MIME envelope. Verification is performed both before and after recipient decryption. An initial CRLF canonicalization mismatch was repaired; later Mac and CI executions passed. Certificate validity is established only against the explicitly installed test trust anchor, not a publicly recognized certification authority. See [T-SMIME-01](../practical/evidence/T-SMIME-01/EVIDENCE.md).

### 4.3 Hashing and signed-message integrity

`practical/integrity_demo.py` and its recorded synthetic fixtures demonstrate how changed content produces a different SHA-256 digest. Hashing is a detection primitive and **cannot on its own prove who sent an email**; user-level signatures add signer-key verification, and DKIM supplies different domain-level authentication.

### 4.4 SPF / DKIM / DMARC

`secure_email_lab/authentication.py` implements a **deliberately restricted offline SPF evaluator** for `ip4`, `ip6` and `all` and a DMARC alignment/policy decision model with an explicitly supplied organizational domain. It covers authorized/unauthorized senders, alignment alternatives, strict vs relaxed matching and staged dispositions. Unsupported SPF mechanisms raise explicit errors.

`secure_email_lab/dkim_lab.py` uses genuine RSA-SHA256 signing and verification. Selected headers and the body undergo a bounded relaxed canonicalization scheme; changing signed headers or the message body invalidates the signature. This educational fixture is **not a full RFC 6376 parser**, nor does it publish selectors or verify DNS in live mail. See [T-AUTH-01](../practical/evidence/T-AUTH-01/EVIDENCE.md).

### 4.5 MFA

`secure_email_lab/mfa.py` demonstrates RFC 6238 TOTP with PBKDF2 password checking, per-account lockout after repeated failures, replay prevention and explicit negative tests (wrong password, expired code, reused code). Successful test logins are local simulation results, **not an assertion that any real mailbox requires MFA**. Production rollout should favor phishing-resistant passkeys or FIDO2 authenticators wherever possible. See [T-MFA-01](../practical/evidence/T-MFA-01/EVIDENCE.md).

### 4.6 Gateway and DLP

`secure_email_lab/gateway.py` parses small synthetic MIME messages and applies policy to risky attachment filename extensions, a specific synthetic phishing marker, independently supplied DMARC disposition, and synthetic outbound secret markers. Suspected data leakage to an external destination is blocked; opaque encrypted outbound MIME causes a review action rather than a false claim of inspection. The audit output includes only a message SHA-256 fingerprint, action and policy reasons, not the sensitive body.

**Limitations:** The emulator cannot recognize arbitrary malware or real phishing, scan PDFs, evaluate URL reputation, prevent MIME evasions in production, or deliver/quarantine actual SMTP traffic. See [T-SEG-DLP-01](../practical/evidence/T-SEG-DLP-01/EVIDENCE.md).

## 5. Test results

| Verification | Execution evidence | Result |
|---|---|---|
| Security unit tests | GitHub Actions run 39389957335 | **37/37 PASS** |
| Synthetic integrated checks | Same CI run | **9/9 PASS** |
| OpenPGP isolated sign/encrypt/decrypt | Mac terminal + CI | **PASS** |
| S/MIME isolated sign/encrypt/decrypt | Mac terminal + CI | **PASS** |
| Real domain SPF/DKIM/DMARC | No owned-domain access verified | **Not tested** |
| Real mailbox MFA enforcement | No provider tenant configured | **Not tested** |
| Real SMTP gateway / AV / DLP deployment | No server or integrated provider | **Not tested** |
| End-to-end client-to-client mail transfer | No controlled mailboxes supplied | **Not tested** |

Unit tests check both accepted and rejected cases. Detailed expected outcomes, links and limitations are in the [evidence register](../practical/test-plan.md). No penetration test of external systems was conducted.

## 6. Security policies, awareness and compliance

Proposed policies cover classification, MFA and least privilege, message-level and transit encryption, sender-domain authentication, endpoint DLP, safe attachments, retention, incident reporting, recovery and periodic review. See [email security policies](security-policy-compliance.md) and the [employee awareness program](../training/employee-awareness.md).

The design references GDPR and HIPAA **only to the extent applicable**. Encryption and a successful synthetic test suite are not evidence of legal compliance, data protection impact assessment completion, or organizational certification.

## 7. Risk assessment and residual gaps

The major unresolved risks are deployment-related: legitimate third-party senders omitted from SPF, misaligned DKIM, business interruption from premature DMARC rejection, phishing-resistant MFA not enforced, lost keys/certificates, gateway false positives, malicious content missed by toy policy rules, leakage through E2EE content, and incomplete operational monitoring. The [threat model](threat-model.md) records assumptions; the [deployment checklist](deployment-checklist.md) specifies staged operational validation and rollback.

There are also limits to what lab verification proves. Self-generated signatures verify mathematics and algorithm interoperability, not human identity without independent key trust. The DKIM model does not implement every standards requirement. The TOTP demo deliberately omits production account recovery, secure enrollment, distributed state and identity lifecycle management.

## 8. Conclusion and recommendations

The project delivers a documented reference architecture, runnable offline implementation and reproducible evidence for major email security mechanisms. GitHub CI demonstrates that the expected positive and negative fixtures behave as specified. These are meaningful engineering results, but a real secure-email communication system requires authorized configuration and evidence from an operational mail environment.

Next steps are to: (1) obtain scope and domain ownership approval; (2) inventory all authorized sending services; (3) pilot provider-managed SPF/DKIM/DMARC in monitor mode; (4) enforce FIDO2/passkeys through the actual identity platform; (5) deploy and validate a managed gateway and pre-encryption/endpoint DLP; and (6) conduct real delivery, negative, recovery and incident tabletop testing with redacted audit evidence.

## References

See [IETF, NIST and regulatory references](../references/standards.md). The project does not assert that any part of this report has been accepted, certified, submitted or deployed by an external organization.
