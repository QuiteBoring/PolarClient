import os
import re
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# Function to read a file's content
def read_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to encrypt content with a password
def encrypt_string_with_password(plain_text, password):
    # Convert password to bytes
    password_bytes = password.encode()
    
    # Generate a random salt
    salt = os.urandom(16)
    
    # Derive a key from the password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password_bytes)
    
    # Generate a random IV
    iv = os.urandom(16)
    
    # Initialize the cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Pad the plaintext to be compatible with block size
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plain_text.encode()) + padder.finalize()
    
    # Encrypt the data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    # Combine the salt, IV, and encrypted data for storage/transmission
    encrypted_message = salt + iv + encrypted_data
    
    # Encode the encrypted message with base64
    encoded_message = base64.b64encode(encrypted_message)
    
    return encoded_message.decode()

# Main function to process the loader.js file
def process_loader_js(loader_file_path, password):
    big_string = ""
    import_pattern = re.compile(r"import\s+'(.+?)'")

    # Read the loader.js file content
    loader_content = read_file_content(loader_file_path)

    # Find all imported file paths
    imported_files = import_pattern.findall(loader_content)

    for file_path in imported_files:
        # Normalize the file path (assuming all paths are relative to the directory containing loader.js)
        full_path = os.path.join(os.path.dirname(loader_file_path), file_path + ".js")

        # Read the file content
        file_content = read_file_content(full_path)

        # Encrypt the file content
        encrypted_content = encrypt_string_with_password(file_content, password)

        # Append the encrypted content to the big string
        big_string += encrypted_content + "§§§"

    # Print the final big string
    print(big_string.removesuffix("§§§"))

# Specify the path to the loader.js file and the password for encryption
loader_file_path = 'src/loader.js'
password = 'D3rb*oeANorKiuvaa_8waxoyAXwt2@jndno!fVf*hh_kL.4*-9gRoWRJPDKPAQUo'

# Process the loader.js file
process_loader_js(loader_file_path, password)

