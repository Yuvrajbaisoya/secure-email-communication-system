# Secure Email Gateway and DLP Configuration Guide

## Deployment model
Choose provider-native protection for managed production mail, or a separate authorized test gateway (e.g. Proxmox Mail Gateway) for lab evaluation. Never change a third-party MX record or intercept others' email.

## Lab prerequisites
- Isolated VM/network and two test mailboxes
- Mail relay with outbound restrictions to avoid accidental external delivery
- Admin access to lab DNS/MTA, TLS certificates and logging
- Current security patches and resource limits

## Configuration procedure
1. Document topology and baseline SMTP flow with dummy mail.
2. Route test inbound SMTP through the gateway; restrict accepted recipients and relaying.
3. Enable anti-spam scoring, URL reputation checks, attachment policies and antivirus scanning with updated signatures.
4. Configure quarantine and release permissions; monitor false positives.
5. Set inbound rate limits and logging with minimal retention of message content.
6. Test using benign spam patterns and the standard harmless EICAR antivirus test file **only in an authorized isolated environment**.
7. Integrate with a DLP engine or provider-native DLP; define a rule for a synthetic marker such as `CONFIDENTIAL-DEMO-12345`.
8. Send dummy outbound mail with and without the marker. Verify that policy blocks/quarantines the marked message and permits the clean message.
9. Record gateway version, configuration screenshots, redacted logs, false positives and rollback plan.

## Example policy matrix
| Signal | Action | Escalation |
|---|---|---|
| Known malware attachment | Reject/quarantine | Alert security |
| High-confidence phishing | Quarantine | Security review |
| Spam score above threshold | Junk/quarantine | User release workflow |
| Synthetic DLP marker | Block and log | Notify test administrator |
| Encrypted outbound content | Require endpoint classification | Review exceptions |

## DLP and E2EE limitation
A gateway cannot reliably inspect end-to-end encrypted message bodies. Apply DLP before encryption in managed clients/endpoints or use approved metadata policies. Do not silently decrypt private communications.

## Acceptance tests
Log test ID, policy, synthetic message, expected action, actual action, timestamp and screenshot. Keep all results **Pending** until performed.
