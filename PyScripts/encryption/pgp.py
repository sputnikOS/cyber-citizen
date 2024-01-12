from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


import argparse

banner = """

======================================================================
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
pgp key generator
version 0.0.1
License: GPLv3
Usage: python pgp.py "secret message" "file_output"
=======================================================================

"""

import sys
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

def generate_key_pair():
    # Generate a private/public key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # Serialize the public key to PEM format
    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_key, pem_public_key

def encrypt_message(public_key, message):
    # Encrypt the message using the public key
    encrypted_message = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted_message

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python script.py <message> <output_file>")
        sys.exit(1)

    # Extract command line arguments
    message_arg = sys.argv[1]
    output_file_arg = sys.argv[2]

    # Convert message to bytes
    message_bytes = message_arg.encode('utf-8')

    # Generate key pair
    private_key, pem_public_key = generate_key_pair()

    # Encrypt the message
    encrypted_message = encrypt_message(private_key.public_key(), message_bytes)

    # Save public key and encrypted message to files
    with open(output_file_arg + "_public_key.pem", 'wb') as public_key_file:
        public_key_file.write(pem_public_key)

    with open(output_file_arg + "_encrypted_message.bin", 'wb') as encrypted_message_file:
        encrypted_message_file.write(encrypted_message)

    print(f"Key pair and encrypted message saved to {output_file_arg}_public_key.pem and {output_file_arg}_encrypted_message.bin")
