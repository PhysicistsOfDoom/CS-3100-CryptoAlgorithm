import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # go up 1 level

from string_encryption import encrypt_string, decrypt_string

# Encrypt
key, cipher = encrypt_string("secret message")

# Decrypt
plain = decrypt_string(key, cipher)
print("Decrypted:", plain)