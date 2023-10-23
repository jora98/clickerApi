"""
Utility methods for validation, password hashing, and verification.
"""

import re
from passlib.hash import pbkdf2_sha512

class Utils():
    """Utility methods."""

    @staticmethod
    def email_is_valid(email):
        """Check if the provided email has a valid format."""
        email_address_matcher = re.compile(r"^[\w-]+@([\w-]+\.)+[\w]+$")
        return bool(email_address_matcher.match(email))

    @staticmethod
    def hash_password(password):
        """Return a pbkf2_sha512 encrypted password."""
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """Verify if the hashed password matches the provided password."""
        return pbkdf2_sha512.verify(password, hashed_password)
