from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

import sys
import argparse
import colorama
from colorama import Fore, Style
import humanize

def banner():
    
    print(Fore.MAGENTA + """

======================================================================

██████╗░░█████╗░░██████╗██████╗░██╗░░░██╗████████╗███╗░░██╗██╗██╗░░██╗
██╔══██╗██╔══██╗██╔════╝██╔══██╗██║░░░██║╚══██╔══╝████╗░██║██║██║░██╔╝
██████╔╝███████║╚█████╗░██████╔╝██║░░░██║░░░██║░░░██╔██╗██║██║█████═╝░
██╔══██╗██╔══██║░╚═══██╗██╔═══╝░██║░░░██║░░░██║░░░██║╚████║██║██╔═██╗░
██║░░██║██║░░██║██████╔╝██║░░░░░╚██████╔╝░░░██║░░░██║░╚███║██║██║░╚██╗
╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝░░░░░░╚═════╝░░░░╚═╝░░░╚═╝░░╚══╝╚═╝╚═╝░░╚═╝
======================================================================
                    pyCrypt v0.1.0
"Usage: python pyCrypt.py <encrypt|decrypt> <message|file> <output_file>"
=======================================================================

""" + Style.RESET_ALL)
    

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_key, pem_public_key

def encrypt_message(public_key, message):
    encrypted_message = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_message

def decrypt_message(private_key, encrypted_message):
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_message

if __name__ == "__main__":
    banner()
    if len(sys.argv) < 3:
        print("Usage: python crypt.py <encrypt|decrypt|generate> <message|file> <output_file>")
        sys.exit(1)

    command = sys.argv[1]
    input_arg = sys.argv[2]
    output_file_arg = sys.argv[3]



    if command == "encrypt":
        message_bytes = input_arg.encode('utf-8')
        private_key, pem_public_key = generate_key_pair()
        encrypted_message = encrypt_message(private_key.public_key(), message_bytes)

        with open(output_file_arg + "_public_key.pem", 'wb') as public_key_file:
            public_key_file.write(pem_public_key)

        with open(output_file_arg + "_encrypted_message.bin", 'wb') as encrypted_message_file:
            encrypted_message_file.write(encrypted_message)

        print(f"Key pair and encrypted message saved to {output_file_arg}_public_key.pem and {output_file_arg}_encrypted_message.bin")

    elif command == "decrypt":
        with open(output_file_arg + "_private_key.pem", 'rb') as private_key_file:
            private_key = serialization.load_pem_private_key(
                private_key_file.read(),
                password=None,
                backend=default_backend()
            )

        with open(input_arg, 'rb') as encrypted_message_file:
            encrypted_message = encrypted_message_file.read()

        decrypted_message = decrypt_message(private_key, encrypted_message)
        print(f"Decrypted message: {decrypted_message.decode('utf-8')}")

    else:
        print("Invalid command. Use 'encrypt' or 'decrypt'.")
        sys.exit(1)
