# utils/encryption.py

from cryptography.fernet import Fernet
import base64
import os

class Encryption:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def encrypt(self, password):
        """Encrypt a password."""
        cipher_text = self.cipher_suite.encrypt(password.encode())
        return cipher_text.decode()

    def decrypt(self, cipher_text):
        """Decrypt a cipher text."""
        plain_text = self.cipher_suite.decrypt(cipher_text.encode())
        return plain_text.decode()

    def generate_key(self):
        """Generate a new encryption key."""
        return Fernet.generate_key()

    def set_key(self, key):
        """Set a custom encryption key."""
        self.key = key
        self.cipher_suite = Fernet(self.key)

# Example usage:
if __name__ == "__main__":
    encryption = Encryption()
    password = "mysecretpassword"
    encrypted_password = encryption.encrypt(password)
    print(f"Encrypted password: {encrypted_password}")

    decrypted_password = encryption.decrypt(encrypted_password)
    print(f"Decrypted password: {decrypted_password}")