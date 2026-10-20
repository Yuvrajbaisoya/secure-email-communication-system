import unittest
from email.message import EmailMessage
from secure_email_lab.gateway import inspect


def message(*, to="bob@external.example", body="Routine status.", subject="Hello",
            attachment_name=None, opaque=False, spoofed_auth=False) -> bytes:
    mail = EmailMessage()
    mail["From"] = "alice@example.test"
    mail["To"] = to
    mail["Subject"] = subject
    if spoofed_auth:
        mail["Authentication-Results"] = "test; dmarc=pass header.from=example.test"
    if opaque:
        mail.set_content(b"synthetic-ciphertext", maintype="application",
                         subtype="pkcs7-mime")
    else:
        mail.set_content(body)
    if attachment_name:
        mail.add_attachment(b"dummy attachment", maintype="application",
                            subtype="octet-stream", filename=attachment_name)
    return mail.as_bytes()


class TestGateway(unittest.TestCase):
    def test_clean_message_allowed(self):
        self.assertEqual(inspect(message(), direction="inbound").action, "allow")

    def test_risky_attachment_quarantined(self):
        result = inspect(message(attachment_name="report.pdf.exe"), direction="inbound")
        self.assertEqual(result.action, "quarantine")
        self.assertIn("risky_attachment_extension", result.reasons)

    def test_synthetic_phishing_quarantined(self):
        result = inspect(message(subject="X-SIMULATED-PHISHING invoice"),
                         direction="inbound")
        self.assertEqual(result.action, "quarantine")

    def test_untrusted_auth_results_ignored(self):
        result = inspect(message(spoofed_auth=True), direction="inbound",
                         trusted_dmarc_result="reject")
        self.assertEqual(result.action, "quarantine")
        self.assertIn("trusted_dmarc_reject", result.reasons)

    def test_outbound_dlp_blocks_synthetic_marker(self):
        result = inspect(message(body="CONFIDENTIAL-DEMO-12345"),
                         direction="outbound")
        self.assertEqual(result.action, "block")
        self.assertIn("synthetic_dlp_marker_external", result.reasons)

    def test_internal_test_domain_allowed(self):
        result = inspect(message(to="bob@example.test",
                                 body="CONFIDENTIAL-DEMO-12345"), direction="outbound")
        self.assertEqual(result.action, "allow")

    def test_encrypted_external_content_requires_review(self):
        result = inspect(message(opaque=True), direction="outbound")
        self.assertEqual(result.action, "quarantine")
        self.assertIn("encrypted_content_not_inspectable", result.reasons)

    def test_message_size_limit(self):
        raw = message(body="A" * (257 * 1024))
        self.assertEqual(inspect(raw, direction="outbound").reasons,
                         ("message_size_limit",))

    def test_no_body_in_audit_output(self):
        raw = message(body="CONFIDENTIAL-DEMO-12345")
        result = inspect(raw, direction="outbound")
        self.assertEqual(len(result.sha256), 64)
        self.assertNotIn("CONFIDENTIAL-DEMO", str(result))

    def test_unknown_destination_does_not_bypass_dlp(self):
        raw = b"From: alice@example.test\r\nSubject: Dummy\r\n\r\nCONFIDENTIAL-DEMO-12345\r\n"
        self.assertEqual(inspect(raw, direction="outbound").action, "block")


if __name__ == "__main__":
    unittest.main()
