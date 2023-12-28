import ecdsa
import hashlib
import base58

def generate_wallet():
    # Generate a private key
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

    # Get the corresponding public key
    public_key = private_key.get_verifying_key()

    # Get the uncompressed and compressed forms of the public key
    uncompressed_pub_key = public_key.to_string('uncompressed').hex()
    compressed_pub_key = public_key.to_string('compressed').hex()

    # Create the address from the public key
    public_key_bytes = bytes.fromhex(compressed_pub_key)
    sha256_hash = hashlib.sha256(public_key_bytes).digest()
    ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()

    # Add version byte (0x00 for Bitcoin mainnet)
    version_ripemd160_hash = b'\x00' + ripemd160_hash

    # Get checksum
    checksum = hashlib.sha256(hashlib.sha256(version_ripemd160_hash).digest()).digest()[:4]

    # Add checksum to the version + ripemd160 hash
    binary_address = version_ripemd160_hash + checksum

    # Encode the binary address to Base58
    wallet_address = base58.b58encode(binary_address).decode('utf-8')

    return {
        "private_key": private_key.to_string().hex(),
        "public_key_uncompressed": uncompressed_pub_key,
        "public_key_compressed": compressed_pub_key,
        "wallet_address": wallet_address
    }

# Generate a wallet
wallet = generate_wallet()
print("Generated Wallet:")
print(wallet)
