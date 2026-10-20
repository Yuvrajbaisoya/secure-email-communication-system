# Authorized Deployment Checklist

This is a future deployment playbook, **not a record of changes already made**. Obtain written permission for every domain, mail tenant, VM and account. Make changes only in a pilot or designated maintenance window with an explicit rollback owner.

## Phase 0 — Scope and baseline

- [ ] Confirm account/domain ownership, approved test users, operational sponsor and permitted testing scope.
- [ ] Inventory inbound/outbound providers, SaaS senders, third-party bulk senders, forwarding services and MX routes.
- [ ] Capture redacted DNS, mail headers, TLS and MFA settings with timestamps and software versions.
- [ ] Decide classifications, retention requirements, emergency contacts and service-level needs.
- [ ] Pilot synthetic messages before any real customer or personal data.

## Phase 1 — Sender-domain authentication

- [ ] Query existing SPF: \`dig +short TXT owned-domain.example\`.
- [ ] Publish **one** correctly sized SPF TXT policy for all authorized senders; validate DNS lookup limits and include chains.
- [ ] Configure DKIM signing **inside the authorized email provider/MTA**; store signing keys in managed secrets, not GitHub.
- [ ] Publish selector TXT and confirm a real received message has valid \`DKIM-Signature\` plus trusted authentication results.
- [ ] Publish DMARC \`p=none\` initially and receive aggregate reports in an approved mailbox.
- [ ] Evaluate every legitimate sender and required relaxed/strict SPF or DKIM alignment to the Header From domain.
- [ ] Only after monitoring, pilot \`p=quarantine\` then \`p=reject\` with safe rollback.

Illustrative placeholders (do **not** deploy literally):

\`\`\`dns
example.test.                      TXT "v=spf1 ip4:192.0.2.10 -all"
lab._domainkey.example.test.       TXT "v=DKIM1; k=rsa; p=REPLACE_WITH_PROVIDER_PUBLIC_KEY"
_dmarc.example.test.               TXT "v=DMARC1; p=none; rua=mailto:dmarc-reports@example.test"
\`\`\`

The toy authentication evaluator in this repo cannot stand in for full SPF/DKIM/DMARC verification.

## Phase 2 — Account identity and key trust

- [ ] Enforce supported phishing-resistant FIDO2/passkeys for privileged and end-user access, with secure recovery.
- [ ] Disable legacy/basic authentication, apply least privilege and review stale sessions.
- [ ] Test lost device, session revocation, phishing challenge and password-reset recovery with test-only accounts.
- [ ] Provision end-user OpenPGP keys or organizational S/MIME certificates; verify fingerprints/identity and revocation paths.
- [ ] Test client-to-client encrypted/signed messages without exposing private keys or user correspondence.

## Phase 3 — Gateway, malware and DLP

- [ ] Select provider-managed SEG with updated AV, URL intelligence, attachment sandboxing and quarantine release workflows.
- [ ] Apply inbound restrictions, fail-safe relay behavior, TLS, monitoring, alerts, least privilege and safe logging.
- [ ] Begin DLP in **audit-only mode** with synthetic unique markers; tune false positives and exception approval.
- [ ] Protect pre-encryption plaintext with managed endpoint classification/DLP; define policy for opaque E2EE content.
- [ ] Verify that clean mail is delivered, harmless synthetic marker is blocked, and quarantine decisions are recoverable.
- [ ] Monitor performance, delivery impacts and incident response with an approved on-call owner.

## Phase 4 — Evidence, training and rollback

- [ ] Capture redacted DNS query output and actual received Authentication-Results headers.
- [ ] Capture redacted provider MFA enrollment/enforcement evidence and recovery outcomes.
- [ ] Capture sanitized gateway quarantine / DLP decisions with rule version, actor and timestamp.
- [ ] Record deliverability and false-positive metrics across legitimate senders; simulate safe rollback.
- [ ] Train users on phishing, recipient verification, encryption and incident reporting.
- [ ] Obtain formal operator and security sign-off before declaring production controls complete.

## Rollback rules

Avoid abrupt DMARC \`p=reject\` changes without monitoring. Restore documented MX and authentication/DLP policies only under authorized change management. Do not log entire message bodies or publish secrets merely to prove that a test ran.
