import hashlib
import time
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Globals
blockchain = []
pending_transactions = []

# Classes
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
            self.balance[receiver] = self.balance.get(receiver, 0) + amount
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


# Blockchain Functions
def calculate_hash(index, previous_hash, timestamp, transactions):
    value = str(index) + str(previous_hash) + str(timestamp) + str(sorted(transactions, key=lambda x: str(x)))
    return hashlib.sha256(value.encode()).hexdigest()


def create_genesis_block():
    return Block(0, "0", time.time(), [], calculate_hash(0, "0", time.time(), []))


def create_new_block(previous_block, transactions):
    index = previous_block.index + 1
    timestamp = time.time()
    hash = calculate_hash(index, previous_block.hash, timestamp, transactions)
    return Block(index, previous_block.hash, timestamp, transactions, hash)


# Routes
@app.route('/')
def index():
    return render_template('index.html', blockchain=blockchain)


@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    return jsonify({'blockchain': [block.__dict__ for block in blockchain]})


@app.route('/transaction', methods=['POST'])
def add_transaction():
    data = request.get_json()
    sender = data.get('sender')
    recipient = data.get('recipient')
    amount = data.get('amount')

    if not sender or not recipient or not amount:
        return jsonify({'error': 'Invalid transaction data.'}), 400

    # Check token balance
    if token.transfer(sender, recipient, amount):
        new_transaction = Transaction(sender, recipient, amount, token.symbol)
        pending_transactions.append(new_transaction.__dict__)
        return jsonify({'message': 'Transaction added to pending transactions.'}), 201
    else:
        return jsonify({'error': 'Insufficient balance or invalid sender.'}), 400


@app.route('/mine', methods=['GET'])
def mine_block():
    if not pending_transactions:
        return jsonify({'error': 'No transactions to mine.'}), 400

    previous_block = blockchain[-1]
    transactions = pending_transactions.copy()  # Include pending transactions
    new_block = create_new_block(previous_block, transactions)

    # Clear pending transactions and add the block to the blockchain
    pending_transactions.clear()
    blockchain.append(new_block)

    return render_template('mine.html', message='New block mined successfully.', block=new_block.__dict__)


if __name__ == '__main__':
    blockchain.append(create_genesis_block())
    token = Token("OpenSputnik", "OS", 100)
    wallet = Wallet()
    token.mint(wallet.public_key, 500)

    app.run(host='0.0.0.0', port=5001)
