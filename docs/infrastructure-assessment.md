# Email Infrastructure Assessment (Lab Baseline)

## Scope
This is a proposed **isolated sample lab**, not an assessment of First Quadrant Labs' production infrastructure. No production access or authorization is assumed.

## Assets and data flow
- Two test users and email clients (Thunderbird)
- Test mail service and optional domain with controlled DNS
- Optional secure email gateway and DLP filter
- Dummy messages only; no real personal, financial or customer data

## Baseline assessment checklist
| Control | Evidence to collect | Status |
|---|---|---|
| TLS for SMTP submission and transport | Configuration and negotiated TLS test | Not tested |
| SPF | Published TXT record and DNS query | Not tested |
| DKIM | Signing configuration, public key and header validation | Not tested |
| DMARC | DNS policy, alignment and aggregate reporting | Not tested |
| MFA | Account security settings (redacted) | Not tested |
| OpenPGP | Encrypted send/decrypt and signed-message verification | Not tested |
| S/MIME | Certificate chain, signed/encrypted mail verification | Not tested |
| Gateway | Benign spam/phishing test fixtures and filter logs | Not tested |
| DLP | Synthetic confidential-data detection and policy result | Not tested |
| Audit logging | Retention, access controls and test event | Not tested |

## Risk register (hypotheses, not findings)
| Potential gap | Impact | Recommended mitigation |
|---|---|---|
| Missing DMARC enforcement | Domain impersonation | Stage p=none, analyze reports, then quarantine/reject after validation |
| Weak account authentication | Account takeover | Require phishing-resistant MFA where supported |
| No message-level encryption | Exposure at mail servers | OpenPGP or S/MIME for sensitive communications |
| No outbound DLP | Accidental data disclosure | Classify data, implement scoped detection and exception handling |
| Unfiltered attachments | Malware exposure | Gateway scanning and attachment policies |

## Assessment procedure
1. Document lab topology, ownership, software versions and scope.
2. Inspect mail server/client settings and DNS under your control.
3. Execute authorized, non-destructive validation tests.
4. Record command, date, expected result, observed result and redacted screenshot.
5. Convert hypotheses into confirmed findings only after evidence exists.

## Reporting
Record each finding with: ID, affected asset, evidence, likelihood, impact, severity, remediation, owner, and retest outcome. Never include credentials, private keys, real user data or API tokens in the repository.
