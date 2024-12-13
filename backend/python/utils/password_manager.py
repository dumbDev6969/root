from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

class PasswordManager:
    def __init__(self):
        self.ph = PasswordHasher()

    def hash_password(self, password: str) -> str:
        """
        Hash a password using Argon2.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password.
        """
        return self.ph.hash(password)

    def verify_password(self, hashed_password: str, provided_password: str) -> bool:
        """
        Verify a password against its hash using Argon2.

        Args:
            hashed_password (str): The hashed password.
            provided_password (str): The password to verify.

        Returns:
            bool: True if the provided password matches the hash, False otherwise.
        """
        try:
            self.ph.verify(hashed_password, provided_password)
            return True
        except VerifyMismatchError:
            return False

# Example usage
if __name__ == "__main__":
    password_manager = PasswordManager()

    password = "mysecretpassword"
    hashed_password = password_manager.hash_password(password)
    print(f"Hashed password: {hashed_password}")

    provided_password = "mysecretpassword"
    is_valid = password_manager.verify_password(hashed_password, provided_password)
    print(f"Is password valid? {is_valid}")

    provided_password = "wrongpassword"
    is_valid = password_manager.verify_password(hashed_password, provided_password)
    print(f"Is password valid? {is_valid}")
