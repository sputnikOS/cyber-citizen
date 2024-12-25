import argparse
import sys, os
from colorama import Fore, Style

# Function to print banner with color
def banner():
    print(Fore.LIGHTWHITE_EX + """


          
          

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                                                                                                                           

                                ██████╗░░█████╗░░██████╗██████╗░██╗░░░██╗████████╗███╗░░██╗██╗██╗░░██╗
                                ██╔══██╗██╔══██╗██╔════╝██╔══██╗██║░░░██║╚══██╔══╝████╗░██║██║██║░██╔╝
                                ██████╔╝███████║╚█████╗░██████╔╝██║░░░██║░░░██║░░░██╔██╗██║██║█████═╝░
                                ██╔══██╗██╔══██║░╚═══██╗██╔═══╝░██║░░░██║░░░██║░░░██║╚████║██║██╔═██╗░
                                ██║░░██║██║░░██║██████╔╝██║░░░░░╚██████╔╝░░░██║░░░██║░╚███║██║██║░╚██╗
                                ╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝░░░░░░╚═════╝░░░░╚═╝░░░╚═╝░░╚══╝╚═╝╚═╝░░╚        
                                       
                                                        
                                                        .sS$$$$$$$$$$$$$$Ss.
                                                    .$$$$$$$$$$$$$$$$$$$$$$s.
                                                    $$$$$$$$$$$$$$$$$$$$$$$$S.
                                                    $$$$$$$$$$$$$$$$$$$$$$$$$$s.
                                                    S$$$$'        `$$$$$$$$$$$$$
                                                    `$$'            `$$$$$$$$$$$.
                                                    :               `$$$$$$$$$$$
                                                    :                 `$$$$$$$$$$
                                                .====.  ,=====.       $$$$$$$$$$
                                                .'      ~'       ".    s$$$$$$$$$$
                                                :       :         :=_  $$$$$$$$$$$
                                                `.  ()  :   ()    ' ~=$$$$$$$$$$$'
                                                ~====~`.      .'    $$$$$$$$$$$
                                                .'     ~====~     sS$$$$$$$$$'
                                                :      .         $$$$$' $$$$
                                                .sS$$$$$$$$Ss.     `$$'   $$$'
                                                $$$$$$$$$$$$$$$s         s$$$$
                                                $SSSSSSSSSSSSSSS$        $$$$$
                                                    :                   $$$$'
                                                    `.                 $$$'
                                                        `.               :
                                                        :               :
                                                        :              .'`.
                                                        .'.           .'   :
                                                    : .$s.       .'    .'
                                                    :.S$$$S.   .'    .'
                                                    : $$$$$$`.'    .'
                                                        $$$$   `. .'
                                                                `
          
        
                                                                                                                                    
==============================================================================================================================================
""" + Style.RESET_ALL)

def clearScr():
    os.system('clear')

# Function to display available ciphers
def list_ciphers():
    print(Fore.LIGHTCYAN_EX + """
        Available Ciphers:
        -------------------
        1. PGP (Pretty Good Privacy)
        2. Fernet (Symmetric Encryption)
        3. Caesar Cipher (Shift Cipher)
        4. AES256 (Advanced Encryption Standard)
        5. Enigma (Historical Cipher)

        Choose a cipher for encryption/decryption.
    """ + Style.RESET_ALL)

# Function to display help information
def help_menu():
    print(Fore.YELLOW + """
        Usage: python start.py <command> <cipher> <input_type> <output_file>

        Commands:
        ----------
        encrypt   : Encrypt a message or file
        decrypt   : Decrypt a message or file
        generate  : Generate necessary keys (e.g., for Fernet)
        help      : Help
        list      : List ciphers

        Ciphers:
        --------
        - pgp      : PGP encryption
        - fernet   : Symmetric encryption with Fernet
        - caesar   : Caesar shift cipher
        - aes256   : AES256 encryption
        - enigma   : Enigma machine encryption (historical)

        Input Types:
        -------------
        message   : Encrypt or decrypt a string message
        file      : Encrypt or decrypt a file

        Example:
        python start.py encrypt fernet message "Hello World" output.txt
        python start.py decrypt fernet file input.txt output.txt

    """ + Style.RESET_ALL)

# Main function to parse and execute arguments
def main():
    parser = argparse.ArgumentParser(description="pyCrypt Encryption/Decryption Utility")
    subparsers = parser.add_subparsers(dest="command")

    # Subparser for 'help'
    parser_help = subparsers.add_parser('help', help="Display help information")
    parser_help.set_defaults(func=help_menu)

    # Subparser for 'list_ciphers'
    parser_ciphers = subparsers.add_parser('list', help="List available ciphers")
    parser_ciphers.set_defaults(func=list_ciphers)

    # Subparser for 'encrypt'
    parser_encrypt = subparsers.add_parser('encrypt', help="Encrypt a message or file")
    parser_encrypt.add_argument('cipher', choices=['pgp', 'fernet', 'caesar', 'aes256', 'enigma'], help="Cipher to use for encryption")
    parser_encrypt.add_argument('input_type', choices=['message', 'file'], help="Type of input: message or file")
    parser_encrypt.add_argument('input', help="Input message or file path")
    parser_encrypt.add_argument('output', help="Output file path to save encrypted data")
    parser_encrypt.set_defaults(func=encrypt)

    # Subparser for 'decrypt'
    parser_decrypt = subparsers.add_parser('decrypt', help="Decrypt a message or file")
    parser_decrypt.add_argument('cipher', choices=['pgp', 'fernet', 'caesar', 'aes256', 'enigma'], help="Cipher to use for decryption")
    parser_decrypt.add_argument('input_type', choices=['message', 'file'], help="Type of input: message or file")
    parser_decrypt.add_argument('input', help="Input message or file path")
    parser_decrypt.add_argument('output', help="Output file path to save decrypted data")
    parser_decrypt.set_defaults(func=decrypt)

    # Subparser for 'generate'
    parser_generate = subparsers.add_parser('generate', help="Generate necessary encryption keys")
    parser_generate.set_defaults(func=generate)

    # Parse the arguments
    args = parser.parse_args()

    # Execute the function associated with the chosen command
    if args.command:
        args.func()

# Placeholder for actual cipher encryption/decryption logic
def encrypt():
    print("Encrypting...")
    # Implement actual encryption logic based on cipher and input type

def decrypt():
    print("Decrypting...")
    # Implement actual decryption logic based on cipher and input type

def generate():
    print ("Generate")

if __name__ == "__main__":
    clearScr()
    banner()
    help_menu()
    list_ciphers()
    main()
