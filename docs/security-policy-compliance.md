# Email Security Policy and Compliance Mapping

**Status:** Proposed policy for a hypothetical consulting organization; legal and compliance review required before adoption.

## Policy
1. **Access:** Unique accounts, least privilege, MFA for all users and administrators, periodic access review and prompt offboarding.
2. **Classification:** Public / Internal / Confidential / Restricted; classify sensitive messages before sending.
3. **Encryption:** Use approved OpenPGP or S/MIME for sensitive content; verify recipient keys and identities. Require TLS for transport.
4. **Authentication:** Maintain authorized SPF, DKIM and staged DMARC enforcement for owned domains.
5. **Acceptable use:** Do not share passwords, private keys, confidential client data or regulated records through unapproved channels.
6. **Attachments:** Scan and restrict risky file types; use approved secure file sharing for large or highly sensitive documents.
7. **DLP:** Monitor or block unauthorized disclosures with documented exception approval and proportionate logging.
8. **Incident response:** Report suspected phishing, account compromise, misdelivery or malware immediately; preserve evidence, revoke sessions, rotate credentials, investigate, contain and notify affected stakeholders as required.
9. **Retention:** Define documented retention/deletion schedules, backup security and legal holds.
10. **Training:** Onboarding plus periodic refreshers and safe phishing simulations; measure improvement without shaming staff.
11. **Review:** Security owner reviews policies at least annually and after major incidents or platform changes.

## Regulatory considerations
- **GDPR (EU):** Assess lawful basis, purpose limitation, data minimization, security of processing (Article 32), processor contracts, international transfers and applicable breach notification obligations. Email encryption alone does not establish GDPR compliance.
- **HIPAA (US, where applicable):** Determine whether the organization is a covered entity or business associate handling PHI; perform a risk analysis and apply relevant Security Rule safeguards and business associate agreements. HIPAA is not automatically applicable to every consulting firm.
- Confirm applicable local laws, sector rules and contractual requirements with qualified counsel.

## Incident playbook (summary)
Detect -> Triage -> Contain -> Preserve evidence -> Eradicate -> Recover -> Notify where required -> Lessons learned. Maintain incident timestamps and assigned owners; avoid exposing personal information in GitHub.
