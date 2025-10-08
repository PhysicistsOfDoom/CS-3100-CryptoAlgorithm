# CS3100 CryptoAlgorithm – String Encryption

This project provides a simple Python package (`algorithm_package`) with functions to **encrypt** and **decrypt strings** using the `cryptography` library (Fernet symmetric encryption).

---

## Installation

1. Clone the Repository

git clone https://github.com/PhysicistsOfDoom/CS-3100-CryptoAlgorithm.git
cd CS-3100-CryptoAlgorithm


=====================================================================

2. Create and Activate Virtual Environment

On Windows (Git Bash):

python -m venv venv
source venv/Scripts/activate


On Mac/Linux:

python3 -m venv venv
source venv/bin/activate


===========================================================================

3. Install Dependencies

Dependencies are listed in requirements.txt. Install them with:

pip install -r requirements.txt


Alternatively, install the package in editable mode:

pip install -e .

========================================================================

Usage

Run the demo script to test encryption/decryption:

python string_encryption.py

Example Output
Original Text:   hello team
Generated Key:   UC6x4P5eA0fnbj5_w6dbY9Yz...
Encrypted Text:  gAAAAABn2-0dktm3klv8XY6H...
Decrypted Text:  hello team

==========================================================================


In Your Own Code

You can import and use the functions directly:

from algorithm_package import algorithm
from string_encryption import encrypt_string, decrypt_string

# Encrypt
key, cipher = encrypt_string("secret message")

# Decrypt
plain = decrypt_string(key, cipher)
print("Decrypted:", plain)