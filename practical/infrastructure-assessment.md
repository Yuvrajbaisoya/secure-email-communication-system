Infrastructure Assessment
1. Purpose
This assessment evaluates a sample email infrastructure and identifies security controls that should be implemented.
2. Assessment Scope
The sample environment includes:
- Email clients
- Email server
- DNS
- Internet mail flow
- Secure email gateway
- User authentication
3. Assessment Checklist
AreaAssessment
MFARequired
SPFRequired
DKIMRequired
DMARCRequired
EncryptionRecommended
Digital signaturesRecommended
Secure gatewayRequired
DLPRecommended
LoggingRequired
User trainingRequired


4. Threat Assessment
ThreatRiskRecommended Control
PhishingHighGateway + training + MFA
SpoofingHighSPF + DKIM + DMARC
MalwareHighGateway scanning
Data leakageHighDLP + encryption
Account compromiseHighMFA
Message tamperingMediumDigital signatures


5. Findings
The sample environment should use multiple security layers rather than depending on a single technology.
6. Recommendations
Priority recommendations:
1. Deploy MFA.
2. Configure SPF, DKIM, and DMARC.
3. Deploy secure email gateway controls.
4. Implement malware and phishing filtering.
5. Establish DLP rules.
6. Provide user awareness training.
7. Establish logging and incident response procedures.
7. Assessment Status
This is a design-level assessment of a sample environment. It does not represent an assessment of a real third-party organization.
