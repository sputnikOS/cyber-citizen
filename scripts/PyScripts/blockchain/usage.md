# Example Usage:
# blockchain = [create_genesis_block()]
# token = Token("Laika", "SAM", 1000)
# previous_block = blockchain[0]
# wallet_A = Wallet()
# wallet_B = Wallet()

# token.mint(wallet_A.public_key, 500)
# token.transfer(wallet_A.public_key, wallet_B.public_key, 200, token)


# # Add token transactions and blocks
# token_transactions = [Transaction(wallet_A.public_key, wallet_B.public_key, 5, token),
#                       Transaction(wallet_A.public_key, wallet_B.public_key, 2, token)]
# new_block = create_new_block(previous_block, token_transactions)
# blockchain.append(new_block)
# previous_block = new_block

# # Print wallet balances and token amounts
# print(f"\033[91m\tWallet A Balance: {wallet_A.balance}, Token Amount: {wallet_A.tokens}, Address: {wallet_A.public_key}")
# print(f"\033[91m\tWallet B Balance: {wallet_B.balance}, Token Amount: {wallet_B.tokens}, Address: {wallet_B.public_key}")

# print(f"\033[91m\tToken Supply: {token.total_supply}")