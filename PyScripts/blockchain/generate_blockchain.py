import hashlib
import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(
            str(self.index).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.data).encode('utf-8') +
            str(self.previous_hash).encode('utf-8')
        ).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # Create the first block (genesis block)
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        # Return the latest block in the chain
        return self.chain[-1]

    def add_block(self, new_block):
        # Add a new block to the chain
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

# Create a blockchain instance
my_blockchain = Blockchain()

# Add blocks to the blockchain
my_blockchain.add_block(Block(1, time.time(), "Transaction Data", ""))
my_blockchain.add_block(Block(2, time.time(), "More Transactions", ""))
