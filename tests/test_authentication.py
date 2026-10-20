import unittest
from secure_email_lab.authentication import evaluate_spf, evaluate_dmarc
from secure_email_lab.dkim_lab import generate_lab_key, public_dns_txt, sign, verify


MESSAGE = (
    b"From: Alice <alice@example.test>\r\n"
    b"To: Bob <bob@example.test>\r\n"
    b"Subject: Synthetic project update\r\n\r\nHello team.\r\n"
)


class TestSPF(unittest.TestCase):
    def test_authorized_ipv4(self):
        self.assertEqual(evaluate_spf("192.0.2.10", "v=spf1 ip4:192.0.2.0/24 -all"), "pass")

    def test_unauthorized_ipv4(self):
        self.assertEqual(evaluate_spf("198.51.100.7", "v=spf1 ip4:192.0.2.0/24 -all"), "fail")

    def test_ipv6(self):
        self.assertEqual(evaluate_spf("2001:db8::2", "v=spf1 ip6:2001:db8::/32 -all"), "pass")

    def test_softfail(self):
        self.assertEqual(evaluate_spf("198.51.100.1", "v=spf1 ip4:192.0.2.1 ~all"), "softfail")

    def test_unsupported_mechanism_fails_closed(self):
        with self.assertRaises(ValueError):
            evaluate_spf("192.0.2.1", "v=spf1 include:other.test -all")

    def test_invalid_syntax(self):
        with self.assertRaises(ValueError):
            evaluate_spf("192.0.2.1", "ip4:192.0.2.1 -all")


class TestDKIM(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.key = generate_lab_key()
        cls.signed = sign(MESSAGE, cls.key)

    def test_real_rsa_dkim_signature(self):
        self.assertTrue(verify(self.signed, self.key.public_key()))

    def test_body_tampering_rejected(self):
        self.assertFalse(verify(self.signed.replace(b"Hello team.", b"Hello attacker."),
                                self.key.public_key()))

    def test_subject_tampering_rejected(self):
        self.assertFalse(verify(self.signed.replace(b"Synthetic project update", b"Changed"),
                                self.key.public_key()))

    def test_wrong_public_key_rejected(self):
        self.assertFalse(verify(self.signed, generate_lab_key().public_key()))

    def test_wrong_selector_rejected(self):
        self.assertFalse(verify(self.signed, self.key.public_key(), expected_selector="other"))

    def test_publishes_only_public_key_material(self):
        record = public_dns_txt(self.key.public_key())
        self.assertTrue(record.startswith("v=DKIM1; k=rsa; p="))
        self.assertNotIn("PRIVATE", record)


class TestDMARC(unittest.TestCase):
    def evaluate(self, **changes):
        settings = dict(
            from_domain="example.test", envelope_domain="bounce.example.test",
            spf_result="pass", dkim_domain="example.test", dkim_result="pass",
            dmarc_record="v=DMARC1; p=reject; aspf=r; adkim=s",
            organizational_domain="example.test"
        )
        settings.update(changes)
        return evaluate_dmarc(**settings)

    def test_aligned_spf_passes(self):
        self.assertEqual(self.evaluate(dkim_result="fail").result, "pass")

    def test_aligned_dkim_passes(self):
        result = self.evaluate(spf_result="fail")
        self.assertTrue(result.aligned_dkim)
        self.assertEqual(result.action, "accept")

    def test_unaligned_both_rejected(self):
        result = self.evaluate(envelope_domain="evil.example.net",
                               dkim_domain="evil.example.net")
        self.assertEqual((result.result, result.action), ("fail", "reject"))

    def test_relaxed_is_not_suffix_confusion(self):
        result = self.evaluate(envelope_domain="notexample.test",
                               dkim_result="fail")
        self.assertEqual(result.result, "fail")

    def test_strict_spf_rejects_subdomain(self):
        result = self.evaluate(dmarc_record="v=DMARC1; p=quarantine; aspf=s",
                               dkim_result="fail")
        self.assertEqual(result.action, "quarantine")

    def test_monitoring_policy_does_not_reject(self):
        result = self.evaluate(dmarc_record="v=DMARC1; p=none",
                               spf_result="fail", dkim_result="fail")
        self.assertEqual((result.result, result.action), ("fail", "accept"))

    def test_invalid_dmarc_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate(dmarc_record="v=DMARC1; p=permit_everything")


if __name__ == "__main__":
    unittest.main()
