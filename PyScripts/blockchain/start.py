import hashlib
import time
import argparse
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

class Wallet:
    def __init__(self):
        self.balance = 0
        self.tokens = 0
        self.private_key = hashlib.sha256(str(time.time()).encode()).hexdigest()
        self.public_key = hashlib.sha256(self.private_key.encode()).hexdigest()

class Token:
    def __init__(self, name, symbol, total_supply):
        self.name = name
        self.symbol = symbol
        self.total_supply = total_supply
        self.balance = {}

    def mint(self, account, amount):
        if account in self.balance:
            self.balance[account] += amount
        else:
            self.balance[account] = amount

    def transfer(self, sender, receiver, amount):
        if sender in self.balance and self.balance[sender] >= amount:
            self.balance[sender] -= amount
            if receiver in self.balance:
                self.balance[receiver] += amount
            else:
                self.balance[receiver] = amount
            return True
        return False

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

@app.route('/')
def index():
    return render_template('index.html', blockchain=blockchain)

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    return jsonify({'blockchain': blockchain})

@app.route('/transaction', methods=['POST'])
def add_transaction():
    data = request.get_json()
    sender = data['sender']
    recipient = data['recipient']
    amount = data['amount']

    # Create a new transaction and add it to the pending transactions list
    new_transaction = Transaction(sender, recipient, amount, "your_token_instance")
    pending_transactions.append(new_transaction.__dict__)

    response = {'message': f'Transaction added to pending transactions.'}
    return jsonify(response), 201
# Example endpoint to mine a new block
@app.route('/mine', methods=['GET'])
def mine_block():
    previous_block = blockchain[-1]
    transactions = pending_transactions  # Include pending transactions in the new block
    new_block = create_new_block(previous_block, transactions)

    # Clear pending transactions after mining a block
    pending_transactions.clear()

    response = {
        'message': 'New block mined successfully.',
        'block': new_block.__dict__
    }
    return render_template('mine.html', message=response['message'], block=response['block'])



if __name__ == '__main__':
    blockchain = [create_genesis_block()]
    app.run(host='0.0.0.0', port=5000)