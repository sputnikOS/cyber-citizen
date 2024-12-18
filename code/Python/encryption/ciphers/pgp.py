# ciphers/pgp.py
import os
import subprocess
import requests
import sys

# URL for the GPG4Win installer
url = "https://files.gpg4win.org/gpg4win-4.1.1.exe"  # Adjust the version if necessary

# Path to save the installer
installer_path = "gpg4win_installer.exe"

# Function to download GPG4Win installer
def download_installer():
    print("Downloading GPG4Win installer...")
    try:
        response = requests.get(url)
        with open(installer_path, 'wb') as f:
            f.write(response.content)
        print("Download complete.")
    except Exception as e:
        print(f"Error downloading installer: {e}")
        sys.exit(1)

# Function to run the installer
def run_installer():
    print("Running GPG4Win installer...")
    try:
        # Running the installer with silent install option (if supported)
        subprocess.run([installer_path, "/silent", "/norestart"], check=True)
        print("Installation complete.")
    except subprocess.CalledProcessError as e:
        print(f"Error during installation: {e}")
        sys.exit(1)

# Function to verify GPG installation
def verify_installation():
    print("Verifying GPG installation...")
    try:
        result = subprocess.run(["gpg", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("GPG installation verified successfully.")
            print(result.stdout)
        else:
            print("GPG is not installed properly.")
            sys.exit(1)
    except FileNotFoundError:
        print("GPG command not found. Ensure GPG is in your PATH.")
        sys.exit(1)

# Main function to manage the whole process
def main():
    download_installer()
    run_installer()
    verify_installation()

if __name__ == "__main__":
    main()
