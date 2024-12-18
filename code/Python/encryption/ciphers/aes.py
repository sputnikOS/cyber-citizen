from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

# AES Encryption example
def aes_encrypt(key, data):
    cipher = AES.new(key, AES.MODE_CBC)  # Using CBC mode for AES encryption
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))  # Padding the data to be a multiple of block_size
    iv = base64.b64encode(cipher.iv).decode('utf-8')  # Get the IV and encode it in base64
    ct = base64.b64encode(ct_bytes).decode('utf-8')  # Encode the ciphertext in base64
    return iv, ct

def aes_decrypt(key, iv, ct):
    iv = base64.b64decode(iv)  # Decode the base64 encoded IV
    ct = base64.b64decode(ct)  # Decode the base64 encoded ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)  # Create the AES cipher object
    pt = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')  # Decrypt and unpad the data
    return pt

# Example of generating a random AES key (256-bit key for AES-256)
key = get_random_bytes(32)  # AES-256 key is 32 bytes (256 bits)
print("Generated AES Key:", base64.b64encode(key).decode('utf-8'))

# Encrypt data
iv, encrypted_data = aes_encrypt(key, "Hello, World!")
print("Encrypted Data:", encrypted_data)

# Decrypt data
decrypted_data = aes_decrypt(key, iv, encrypted_data)
print("Decrypted Data:", decrypted_data)
