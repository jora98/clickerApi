import unittest
from common.utils import Utils

class TestUtils(unittest.TestCase):
    def test_email_valid(self):
        self.assertTrue(Utils.email_is_valid("example@example.com"))
        self.assertFalse(Utils.email_is_valid("invalid_email"))

    def test_hash_password(self):
        password = "password123"
        hashed_password = Utils.hash_password(password)
        self.assertTrue(Utils.check_hashed_password(password, hashed_password))
        self.assertFalse(Utils.check_hashed_password("wrong_password", hashed_password))

if __name__ == '__main__':
    unittest.main()