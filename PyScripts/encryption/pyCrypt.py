from cryptography.fernet import Fernet
import sys

banner = """

=======================================================================

██████╗░██████╗░░█████╗░░░░░░██╗███████╗██╗░░██╗████████╗
██╔══██╗██╔══██╗██╔══██╗░░░░░██║██╔════╝██║░██╔╝╚══██╔══╝
██████╔╝██████╔╝██║░░██║░░░░░██║█████╗░░█████═╝░░░░██║░░░
██╔═══╝░██╔══██╗██║░░██║██╗░░██║██╔══╝░░██╔═██╗░░░░██║░░░
██║░░░░░██║░░██║╚█████╔╝╚█████╔╝███████╗██║░╚██╗░░░██║░░░
╚═╝░░░░░╚═╝░░╚═╝░╚════╝░░╚════╝░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░

██████╗░░█████╗░░██████╗██████╗░██╗░░░██╗████████╗███╗░░██╗██╗██╗░░██╗
██╔══██╗██╔══██╗██╔════╝██╔══██╗██║░░░██║╚══██╔══╝████╗░██║██║██║░██╔╝
██████╔╝███████║╚█████╗░██████╔╝██║░░░██║░░░██║░░░██╔██╗██║██║█████═╝░
██╔══██╗██╔══██║░╚═══██╗██╔═══╝░██║░░░██║░░░██║░░░██║╚████║██║██╔═██╗░
██║░░██║██║░░██║██████╔╝██║░░░░░╚██████╔╝░░░██║░░░██║░╚███║██║██║░╚██╗
╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝░░░░░░╚═════╝░░░░╚═╝░░░╚═╝░░╚══╝╚═╝╚═╝░░╚═╝
======================================================================
Projekt Rasputnik
pyCrypt
version 0.0.1
Usage: python pyCrypt.py [your_string]
Algorythm: Fernet
License: GPLv3
=======================================================================

"""
def encrypt_string(key, plaintext):

    cipher_suite = Fernet(key)
    encrypted_text = cipher_suite.encrypt(plaintext.encode())
    return encrypted_text.decode()

# Example usage:
if __name__ == "__main__":
    # Generate a random encryption key (should be kept secret)
    encryption_key = Fernet.generate_key()
    input = sys.argv[1]
  
    # Text to encrypt
    text_to_encrypt = input

    # Encrypt the text
    encrypted_text = encrypt_string(encryption_key, text_to_encrypt)
    # print(banner)
    print('\033[91m' + '\033[92m', banner)
    # print("Encrypted Text:", encrypted_text)
    print('\033[91m'+'encrypted_text: ' + '\033[92m', encrypted_text)
    

