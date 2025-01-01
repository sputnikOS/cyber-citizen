import argparse


def caesar_decrypt(ciphertext, shift):
    plaintext = ""

    for char in ciphertext:
        if char.isalpha():
            is_upper = char.isupper()
            char = char.lower()
            decrypted_char = chr(((ord(char) - ord('a') - shift) % 26) + ord('a'))
            if is_upper:
                decrypted_char = decrypted_char.upper()
            plaintext += decrypted_char
        else:
            plaintext += char

    return plaintext

def main():
    parser = argparse.ArgumentParser(description="Decrypt text using the Caesar cipher.")
    parser.add_argument("ciphertext", type=str, help="The text to decrypt")
    parser.add_argument("shift", type=int, help="The decryption shift value")

    args = parser.parse_args()

    decrypted_text = caesar_decrypt(args.ciphertext, args.shift)
    print("Decrypted Text:", decrypted_text)

if __name__ == "__main__":
    main()
