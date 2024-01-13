import hashlib
import time

class Wallet:
    def __init__(self):
        self.balance = 0
        self.tokens = 0
        self.private_key = hashlib.sha256(str(time.time()).encode()).hexdigest()
        self.public_key = hashlib.sha256(self.private_key.encode()).hexdigest()

class Token:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

class Transaction:
    def __init__(self, sender, recipient, amount, token):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.token = token

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, transactions):
    value = str(index) + str(previous_hash) + str(timestamp) + str(transactions)
    return hashlib.sha256(value.encode()).hexdigest()

def create_genesis_block():
    return Block(0, "0", time.time(), [], calculate_hash(0, "0", time.time(), []))

def create_new_block(previous_block, transactions):
    index = previous_block.index + 1
    timestamp = time.time()
    hash = calculate_hash(index, previous_block.hash, timestamp, transactions)
    return Block(index, previous_block.hash, timestamp, transactions, hash)

# Example Usage:
blockchain = [create_genesis_block()]
previous_block = blockchain[0]
wallet_A = Wallet()
wallet_B = Wallet()
my_token = Token("OSS", "OSS")

# Add token transactions and blocks
token_transactions = [Transaction(wallet_A.public_key, wallet_B.public_key, 5, my_token),
                      Transaction(wallet_A.public_key, wallet_B.public_key, 2, my_token)]
new_block = create_new_block(previous_block, token_transactions)
blockchain.append(new_block)
previous_block = new_block

# Print wallet balances and token amounts
print(f"Wallet A Balance: {wallet_A.balance}, Token Amount: {wallet_A.tokens}")
print(f"Wallet B Balance: {wallet_B.balance}, Token Amount: {wallet_B.tokens}")
