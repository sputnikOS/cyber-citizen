# ciphers/pgp.py
import gnupg

def generate_pgp_key():
    # Initialize the GPG instance
    gpg = gnupg.GPG()

    # Define the key parameters
    input_data = gpg.gen_key_input(
        name_email='your-email@example.com',  # Replace with your email
        passphrase='your-strong-passphrase',  # Replace with your passphrase
    )

    # Generate the key
    key = gpg.gen_key(input_data)

    # Display key information
    print("PGP Key generated successfully.")
    print("Key ID:", key.fingerprint)

    return key
