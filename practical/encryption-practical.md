Encryption Practical
1. Objective
Demonstrate email encryption in an authorized controlled lab environment.
2. Environment
The test environment should contain:
- Test email accounts
- Test email client
- PGP or S/MIME support
- Test keys/certificates
No confidential production data should be used.
3. Test Procedure
1. Create test identities.
2. Generate or obtain test cryptographic keys/certificates.
3. Configure the email client.
4. Enable encryption.
5. Send a test message.
6. Verify that the recipient can decrypt it.
7. Record the result.
4. Expected Result
The message should be readable by the intended recipient after successful decryption.
Unauthorized users without the required private key should not be able to decrypt the protected content.
5. Evidence
Add screenshots only after completing the authorized lab test.
Recommended evidence:
- Key/certificate configuration
- Email encryption status
- Encrypted message indication
- Successful decryption
6. Status
Pending controlled lab verification.
