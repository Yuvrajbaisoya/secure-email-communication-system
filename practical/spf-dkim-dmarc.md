SPF, DKIM and DMARC Practical
1. Objective
Demonstrate how SPF, DKIM, and DMARC improve email authentication.
2. Test Domain
Use a domain or DNS environment that you own or are explicitly authorized to administer.
Do not modify third-party DNS records.
3. SPF
Create an SPF TXT record identifying authorized sending infrastructure.
Example documentation format:
v=spf1 ip4:203.0.113.10 -all

Use the actual authorized sending service/IP only in an authorized lab.
4. DKIM
Configure the mail system to sign outgoing messages.
Publish the corresponding public key in DNS.
5. DMARC
Start with a monitoring policy in a controlled environment.
Example:
v=DMARC1; p=none; rua=mailto:dmarc@example.com

The domain and reporting address must be replaced with authorized values.
6. Verification
Verify:
- SPF result
- DKIM result
- DMARC result
- Domain alignment
- Authentication headers
7. Expected Result
Legitimate test messages should pass the configured authentication checks.
8. Status
Pending authorized DNS/lab verification.
