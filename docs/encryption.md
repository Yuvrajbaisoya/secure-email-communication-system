Email Encryption
1. Introduction
Email encryption protects message contents from unauthorized access.
This project evaluates two commonly used approaches:
- PGP
- S/MIME
Encryption should be combined with authentication, access control, MFA, and secure email gateway controls.
2. PGP
Pretty Good Privacy (PGP) uses public-key cryptography.
The sender encrypts a message using the recipient's public key. The recipient uses the corresponding private key to decrypt it.
Sender
  |
  | Recipient Public Key
  v
Encrypted Message
  |
  v
Recipient
  |
  | Recipient Private Key
  v
Original Message

3. S/MIME
Secure/Multipurpose Internet Mail Extensions (S/MIME) uses digital certificates and public-key cryptography.
It can provide:
- Message encryption
- Digital signatures
- Sender authentication
- Message integrity
4. PGP vs S/MIME
FeaturePGPS/MIME
Public-key encryptionYesYes
Digital signaturesYesYes
Certificate AuthorityNot requiredCommonly used
Enterprise managementMore complexGenerally easier in managed environments
Trust modelKey-basedCertificate-based


5. Security Benefits
Encryption provides:
- Confidentiality
- Protection against unauthorized reading
- Protection for sensitive communications
- Reduced exposure if messages are intercepted
6. Practical Implementation Plan
A controlled lab can be used to:
1. Generate test keys/certificates.
2. Configure an email client.
3. Enable encryption.
4. Send a test message.
5. Decrypt the message.
6. Verify the sender and encryption status.
7. Record observations.
No real confidential information should be used during testing.
7. Practical Status
Implementation should be verified in an authorized controlled environment. Screenshots and results should only be added after the test has actually been performed.
8. Conclusion
PGP and S/MIME can provide strong message confidentiality when keys and certificates are properly managed.
