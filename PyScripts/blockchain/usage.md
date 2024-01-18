# Example Usage:
# blockchain = [create_genesis_block()]
# previous_block = blockchain[0]
# wallet_A = Wallet()
# wallet_A.public_key = "e744f6b9b442283b70a7827543815d133426f7a5ea4e7b73366dffb47ff3ccda"
# token = Token("SAM", "SAM", 1000)

# token.mint(wallet_A.public_key, 500)
# token.transfer("Address1", "Address2", 200)


# Add token transactions and blocks
# token_transactions = [Transaction(wallet_A.public_key, wallet_B.public_key, 5, token),
#                       Transaction(wallet_A.public_key, wallet_B.public_key, 2, token)]
# new_block = create_new_block(previous_block, token_transactions)
# blockchain.append(new_block)
# previous_block = new_block