Secure Email Gateway
1. Introduction
A Secure Email Gateway (SEG) is positioned between an organization's email infrastructure and external email systems.
Its purpose is to inspect and protect email traffic before messages reach users or leave the organization.
2. Main Security Functions
A secure gateway may provide:
- Spam filtering
- Phishing detection
- Malware scanning
- Attachment inspection
- URL analysis
- Sender reputation checking
- SPF/DKIM/DMARC validation
- Data Loss Prevention
- Quarantine
- Security logging
3. Architecture
Internet
   |
   v
Secure Email Gateway
   |
   +--> Spam Filtering
   +--> Phishing Detection
   +--> Malware Scanning
   +--> DLP
   +--> Authentication Checks
   |
   v
Email Server
   |
   v
Users

4. Incoming Email
Incoming messages should be inspected before delivery.
Recommended sequence:
1. Connection and sender checks
2. SPF/DKIM/DMARC validation
3. Reputation analysis
4. Malware scanning
5. URL and attachment inspection
6. DLP/security policy checks
7. Delivery or quarantine
5. Outgoing Email
Outgoing messages should also be inspected.
Controls can include:
- DLP
- Malware scanning
- Policy enforcement
- DKIM signing
- Logging
- Encryption requirements
6. Quarantine
Suspicious messages can be placed in quarantine rather than delivered directly to users.
Administrators should establish procedures for reviewing false positives.
7. Logging
The gateway should record appropriate security events such as:
- Message filtering decisions
- Authentication failures
- Malware detections
- Policy violations
- Quarantine events
Logs should be protected against unauthorized modification.
8. Conclusion
A secure email gateway provides a central defensive layer against common email threats.
