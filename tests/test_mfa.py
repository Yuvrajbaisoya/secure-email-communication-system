import base64
import unittest
from secure_email_lab.mfa import DemoMFA, totp


class TestTOTP(unittest.TestCase):
    def test_rfc6238_known_sha1_vector(self):
        secret = base64.b32encode(b"12345678901234567890").decode("ascii")
        self.assertEqual(totp(secret, 59, digits=8), "94287082")

    def setUp(self):
        self.svc = DemoMFA()
        self.secret = self.svc.enroll("alice", "CorrectHorseBattery", "JBSWY3DPEHPK3PXP")

    def test_valid_password_and_totp(self):
        self.assertTrue(self.svc.login("alice", "CorrectHorseBattery",
                                       totp(self.secret, 1000), 1000).allowed)

    def test_password_alone_is_not_enough(self):
        self.assertFalse(self.svc.login("alice", "CorrectHorseBattery", "", 1000).allowed)

    def test_wrong_password_denied(self):
        self.assertFalse(self.svc.login("alice", "WrongPassword",
                                        totp(self.secret, 1000), 1000).allowed)

    def test_replay_denied(self):
        code = totp(self.secret, 1000)
        self.assertTrue(self.svc.login("alice", "CorrectHorseBattery", code, 1000).allowed)
        self.assertFalse(self.svc.login("alice", "CorrectHorseBattery", code, 1000).allowed)

    def test_expired_code_denied(self):
        self.assertFalse(self.svc.login("alice", "CorrectHorseBattery",
                                        totp(self.secret, 800), 1000).allowed)

    def test_brute_force_lockout(self):
        for _ in range(5):
            result = self.svc.login("alice", "WrongPassword", "000000", 1000)
        self.assertEqual(result.reason, "temporarily_locked")
        self.assertFalse(self.svc.login("alice", "CorrectHorseBattery",
                                        totp(self.secret, 1001), 1001).allowed)
        self.assertTrue(self.svc.login("alice", "CorrectHorseBattery",
                                       totp(self.secret, 1330), 1330).allowed)

    def test_duplicate_account_rejected(self):
        with self.assertRaises(ValueError):
            self.svc.enroll("alice", "CorrectHorseBattery")


if __name__ == "__main__":
    unittest.main()
