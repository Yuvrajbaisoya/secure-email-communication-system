Digital Signatures
1. Introduction
Digital signatures help verify the authenticity and integrity of an email.
A digital signature can provide evidence that:
- The message originated from the expected sender.
- The message was not modified after signing.
- The sender controls the signing private key.
2. Basic Process
Email Message
     |
     v
Hash Function
     |
     v
Message Digest
     |
     v
Private Key
     |
     v
Digital Signature

The recipient uses the sender's public key to verify the signature.
3. Integrity
If the message is modified after signing, the calculated digest will no longer match the signed digest.
This helps detect tampering.
4. Authentication
Digital signatures provide cryptographic authentication of the signing key, but the trustworthiness of the identity depends on the key or certificate management system.
5. Recommended Algorithms
Modern cryptographic standards should be used according to current organizational security requirements.
Examples include:
- SHA-256 or stronger approved hash algorithms
- RSA with appropriate key sizes
- ECC algorithms where supported
Deprecated or weak algorithms should not be used for new deployments.
6. Practical Verification
A controlled test should:
1. Create a test signing identity.
2. Sign a test email.
3. Send the signed message.
4. Verify the signature.
5. Modify a copy of the message.
6. Verify that the modification is detected.
7. Security Benefits
Digital signatures help provide:
- Integrity
- Authentication
- Non-repudiation support
- Tamper detection
8. Conclusion
Digital signatures are an important component of secure email communication and should be combined with encryption and authentication controls.
