import subprocess
import sys

def install_package(package_name):
    """Install a Python package using pip."""
    try:
        print(f"Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"{package_name} installed successfully!\n")
    except subprocess.CalledProcessError as e:
        print(f"Error installing {package_name}: {e}\n")

def main():
    packages = [
        "pycryptodome",   # Comprehensive cryptography library
        "cryptography",   # Modern cryptography library
        "python-gnupg",   # PGP/GPG encryption
        "hashlib", # Advanced hashing (if needed separately)
        "colorama",
        "argparse",
        "gnupg"
    ]

    print("Starting installation of required packages...\n")
    for package in packages:
        install_package(package)
    print("All packages installed successfully!")

if __name__ == "__main__":
    main()
