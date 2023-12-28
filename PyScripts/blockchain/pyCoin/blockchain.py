from pycoin.blockchain.Block import Block
from pycoin.blockchain.Chain import Chain

# Initialize an empty chain
chain = Chain()

# Create genesis block
genesis_block = Block(0, b"Genesis Block", previous_id=None)
chain.add_block(genesis_block)

# Add more blocks to the chain
block1 = Block(1, b"Data for Block 1", previous_id=genesis_block.id())
block2 = Block(2, b"Data for Block 2", previous_id=block1.id())
block3 = Block(3, b"Data for Block 3", previous_id=block2.id())

chain.add_block(block1)
chain.add_block(block2)
chain.add_block(block3)

# Print the blockchain
print("Blockchain:")
for block in chain.blocks:
    print(f"Block {block.block_id}: {block.data}")
