from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
from typing import Optional

class Encryption:
    def __init__(self, key_file: str = "encryption_key.key"):
        self.key_file = key_file
        self.key = self._load_or_generate_key()
        self.cipher_suite = Fernet(self.key)

    def _load_or_generate_key(self) -> bytes:
        """Load the encryption key from file or generate a new one if it doesn't exist."""
        try:
            with open(self.key_file, "rb") as key_file:
                return key_file.read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as key_file:
                key_file.write(key)
            return key

    def encrypt(self, data: str) -> Optional[str]:
        """Encrypt data."""
        try:
            cipher_text = self.cipher_suite.encrypt(data.encode())
            return base64.urlsafe_b64encode(cipher_text).decode()
        except Exception as e:
            print(f"Encryption error: {e}")
            return None

    def decrypt(self, cipher_text: str) -> Optional[str]:
        """Decrypt cipher text."""
        try:
            cipher_bytes = base64.urlsafe_b64decode(cipher_text.encode())
            plain_text = self.cipher_suite.decrypt(cipher_bytes)
            return plain_text.decode()
        except InvalidToken:
            print("Invalid token: Decryption failed")
            return None
        except Exception as e:
            print(f"Decryption error: {e}")
            return None

    def generate_key_from_password(self, password: str, salt: Optional[bytes] = None) -> bytes:
        """Generate a key from a password and salt using PBKDF2."""
        if salt is None:
            salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def set_key(self, key: bytes):
        """Set a custom encryption key."""
        self.key = key
        self.cipher_suite = Fernet(self.key)
        with open(self.key_file, "wb") as key_file:
            key_file.write(key)

# Example usage:
if __name__ == "__main__":
    encryption = Encryption()
    
    # Example with direct encryption
    data = "mysecretdata"
    encrypted_data = encryption.encrypt(data)
    print(f"Encrypted data: {encrypted_data}")

    decrypted_data = encryption.decrypt(encrypted_data)
    print(f"Decrypted data: {decrypted_data}")

    # Example with password-based key
    password = "mypassword"
    salt = os.urandom(16)
    key = encryption.generate_key_from_password(password, salt)
    encryption.set_key(key)

    encrypted_data = encryption.encrypt(data)
    print(f"Encrypted data with password-based key: {encrypted_data}")

    decrypted_data = encryption.decrypt(encrypted_data)
    print(f"Decrypted data with password-based key: {decrypted_data}")
