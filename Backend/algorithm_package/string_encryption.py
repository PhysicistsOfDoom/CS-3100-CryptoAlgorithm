# Backend/algorithm_package/string_encryption.py
# Author: Vip Monty (Group 2, CS3100)
# Purpose: Encrypt and decrypt strings using Fernet symmetric encryption.

from cryptography.fernet import Fernet

def encrypt_string(plain_text: str) -> tuple[str, str]:
    """
    Encrypts a plain text string with a generated Fernet key.

    Args:
        plain_text (str): The input string to encrypt.

    Returns:
        tuple[str, str]: (encryption_key, encrypted_text)
    """
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encrypted_text = fernet.encrypt(plain_text.encode())
    return key.decode(), encrypted_text.decode()

def decrypt_string(key: str, encrypted_text: str) -> str:
    """
    Decrypts an encrypted string using the provided Fernet key.
    """
    fernet = Fernet(key.encode())
    decrypted_text = fernet.decrypt(encrypted_text.encode())
    return decrypted_text.decode()
