# Secure Email Communication System

**Defense-in-depth research project · reproducible offline security lab**

[![Offline security lab tests](https://github.com/Yuvrajbaisoya/secure-email-communication-system/actions/workflows/lab-security-tests.yml/badge.svg)](https://github.com/Yuvrajbaisoya/secure-email-communication-system/actions/workflows/lab-security-tests.yml)

**Project context:** First Quadrant Labs research assignment  
**Original submission deadline:** 11 October 2026  
**Validation snapshot:** 20 October 2026

> **What this is:** A secure-email architecture proposal, policy/training package, and working **synthetic offline lab** for OpenPGP, S/MIME, SPF/DKIM/DMARC, TOTP MFA, gateway decisions and DLP.
>
> **What this is not:** A deployed corporate email service or proof of control ownership over a real email domain. Do not deploy this educational code as an SMTP gateway, DNS authenticator, identity provider or antivirus.

## Verified implementation at a glance

| Control | Implemented lab capability | Verified status | Production status |
|---|---|---|---|
| OpenPGP | Disposable keys, sign, encrypt, decrypt, verify | **PASS** — Mac and CI | Not deployed |
| S/MIME | Self-signed lab certs, AES-256 envelope, signing and verification | **PASS** — Mac and CI | Not deployed |
| SHA-256 | Detect synthetic message modifications | **PASS** — local evidence | Not a sender authentication control |
| SPF | Evaluate sample IPv4/IPv6 senders using a strict **subset** of SPF | **PASS** — CI | No published/verified DNS |
| DKIM | Generate genuine RSA-SHA256 signature; detect body/header tampering | **PASS** — CI | No live MTA signing or DNS selector |
| DMARC | Evaluate SPF/DKIM From-domain alignment and none/quarantine/reject policy | **PASS** — CI | No receiver or aggregate reporting |
| MFA | RFC 6238 TOTP, password gate, replay rejection and account lockout | **PASS** — CI | No mailbox/IdP enforcement |
| Secure email gateway | Simulated inbound policy decisions, attachment and phishing markers | **PASS** — CI | No SMTP proxy, AV or reputation feeds |
| DLP | Detect synthetic markers on external outbound messages; flag opaque encrypted mail | **PASS** — CI | No provider or endpoint DLP deployment |
| Policies and training | Proposed controls, governance, quiz and incident workflow | **Written** | Approval and training delivery not verified |

**Test evidence:** [GitHub Actions run — 37/37 unit tests, 9/9 integrated checks, OpenPGP and S/MIME jobs PASS](https://github.com/Yuvrajbaisoya/secure-email-communication-system/actions/runs/39389041933). This result was measured on GitHub's Ubuntu runner, not on production infrastructure. See [evidence register](practical/test-plan.md).

## Architecture

\`\`\`mermaid
flowchart LR
  ext["External email"] --> mx["Owned-domain MX / mail service"]
  mx --> auth["SPF · DKIM · DMARC receiver checks"]
  auth --> seg["Gateway: spam / attachment / malware policies"]
  seg --> mailbox["Protected mailboxes"]
  iam["Identity provider + phishing-resistant MFA"] --> mailbox
  mailbox --> endpoint["Managed email clients"]
  endpoint <-->|"Key verified, E2EE"| crypto["OpenPGP / S/MIME"]
  endpoint --> class["Classification + pre-encryption DLP"]
  class --> outbound["Approved outbound sending"]
  seg --> audit["Redacted audit / alerting"]
  mailbox --> audit
\`\`\`

**Trust boundary:** SPF/DKIM/DMARC defend the domain and transport identity, not the human author. TLS is hop protection, not end-to-end encryption. A gateway generally cannot inspect an OpenPGP/S/MIME-encrypted body; DLP must act at the endpoint or before encryption.

## Run the working labs

Requirements: **Python 3.12+**, **GnuPG 2.x** for OpenPGP, **OpenSSL 3.x** for S/MIME, and only synthetic identities/data. On macOS, install GnuPG and Homebrew OpenSSL via Homebrew. The S/MIME script automatically prefers Homebrew OpenSSL when present.

\`\`\`bash
git clone https://github.com/Yuvrajbaisoya/secure-email-communication-system.git
cd secure-email-communication-system

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

# Authentication, MFA, gateway, DLP: positive + negative cases
python -m unittest discover -s tests -v
python -m practical.run_labs

# Cryptographic end-to-end operations using disposable test keys
bash practical/openpgp_lab.sh
bash practical/smime_lab.sh
\`\`\`

**Expected checks:** 37 successful unit tests, 9/9 true integrated lab assertions, and two shell demos printing PASS. The shell scripts delete generated lab keys on exit. The DKIM fixture uses the Python cryptography library and generates a **new** private key in memory; do not commit private key material.

## Repository guide

| Path | Contents |
|---|---|
| [secure_email_lab/](secure_email_lab/) | Offline SPF/DMARC, RSA DKIM, TOTP MFA, gateway + DLP engine |
| [tests/](tests/) | Unit tests with negative and edge-case assertions |
| [practical/](practical/) | Integration runner, OpenPGP/S/MIME demos, evidence register |
| [docs/final-report.md](docs/final-report.md) | Research report, methodology, test outcomes and limitations |
| [docs/threat-model.md](docs/threat-model.md) | Assets, trust boundaries, threats and residual risks |
| [docs/deployment-checklist.md](docs/deployment-checklist.md) | Steps to progress from offline lab to an authorized pilot |
| [docs/architecture-design.md](docs/architecture-design.md) | Reference architecture and data flow |
| [docs/security-policy-compliance.md](docs/security-policy-compliance.md) | Policy proposals and regulatory considerations |
| [docs/gateway-dlp-guide.md](docs/gateway-dlp-guide.md) | Gateway/DLP controls and lab limitations |
| [training/employee-awareness.md](training/employee-awareness.md) | Employee training module and assessment |
| [references/standards.md](references/standards.md) | IETF, NIST and privacy references |
| [.github/workflows/lab-security-tests.yml](.github/workflows/lab-security-tests.yml) | Automated tests, OpenPGP and S/MIME in CI |

## Threats and defensibility

The research focuses on account takeover, spoofing, phishing, message interception, unauthorized content disclosure and malicious attachments. Its layered design mitigates different parts of the attack chain. **No single control guarantees secure email**: authentication, trusted keys, user behavior, operational monitoring, strong provider policies and recovery procedures must work together.

**Evidence integrity:** The only PASS claims here are synthetic, explicitly executed demonstrations and their saved outputs. Local terminal-derived evidence is distinguished from independent CI results. Production checks remain open. Never upload real mailboxes, customer data, passwords, private keys, MFA seed values or live domain credentials.

## Moving beyond the offline lab

Read [deployment checklist](docs/deployment-checklist.md) before doing anything on a live domain. A real pilot needs an owned domain, authorized provider accounts, DNS and mail flow validation, FIDO2/passkey-based MFA where available, appropriate gateway scanning and endpoint DLP, and redacted operating evidence. Do **not** change an organization's MX/SPF/DKIM/DMARC without its approval.

---

*Educational demonstration and reference design. Not a certified production security product.*
