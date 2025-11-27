import random
import sys


# Enigma-like substitution cipher settings
# Here, we'll use a simple substitution cipher with a randomized mapping
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
plugboard_mapping = dict(zip(alphabet, random.sample(alphabet, len(alphabet))))

def encrypt(message):
    encrypted_message = []
    for char in message.upper():
        if char in plugboard_mapping:
            encrypted_message.append(plugboard_mapping[char])
        else:
            encrypted_message.append(char)  # keep non-alphabet characters unchanged
    return ''.join(encrypted_message)

def decrypt(encrypted_message):
    decrypted_message = []
    reverse_mapping = {v: k for k, v in plugboard_mapping.items()}
    for char in encrypted_message.upper():
        if char in reverse_mapping:
            decrypted_message.append(reverse_mapping[char])
        else:
            decrypted_message.append(char)  # keep non-alphabet characters unchanged
    return ''.join(decrypted_message)

# Example usage
if __name__ == "__main__":
    message = sys.argv[1]
    encrypted_message = encrypt(message)
    decrypted_message = decrypt(encrypted_message)
    
    print(f"Original message: {message}")
    print(f"Encrypted message: {encrypted_message}")
    print(f"Decrypted message: {decrypted_message}")
