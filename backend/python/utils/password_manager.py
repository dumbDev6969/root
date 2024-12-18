from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash

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

        Raises:
            ValueError: If the password is empty or None
            TypeError: If the password is not a string
        """
        if not password:
            raise ValueError("Password cannot be empty")
        if not isinstance(password, str):
            raise TypeError("Password must be a string")
            
        try:
            return self.ph.hash(password)
        except Exception as e:
            raise RuntimeError(f"Error hashing password: {str(e)}")

    def verify_password(self, hashed_password: str, provided_password: str) -> bool:
        """
        Verify a password against its hash using Argon2.

        Args:
            hashed_password (str): The hashed password.
            provided_password (str): The password to verify.

        Returns:
            bool: True if the provided password matches the hash, False otherwise.

        Raises:
            InvalidHash: If the hash is malformed or corrupted
        """
        try:
            self.ph.verify(hashed_password, provided_password)
            return True
        except VerifyMismatchError:
            return False
        except InvalidHash as e:
            raise InvalidHash(f"Invalid hash format: {str(e)}")

# Example usage
if __name__ == "__main__":
    password_manager = PasswordManager()

    # password = "mysecretpassword"
    # hashed_password = password_manager.hash_password(password)
    # print(f"Hashed password: {hashed_password}")

    # provided_password = "mysecretpassword"
    # is_valid = password_manager.verify_password(hashed_password, provided_password)
    # print(f"Is password valid? {is_valid}")

    # provided_password = "wrongpassword"
    # is_valid = password_manager.verify_password(hashed_password, provided_password)
    # print(f"Is password valid? {is_valid}")

    a= password_manager.hash_password("Abcd.123")
    print(a)
