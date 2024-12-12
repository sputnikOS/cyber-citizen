require 'digest'
require 'time'

class Block
  attr_reader :index, :timestamp, :transactions, :prev_hash, :nonce, :hash

  def initialize(index, transactions, prev_hash)
    @index = index
    @timestamp = Time.now
    @transactions = transactions
    @prev_hash = prev_hash
    @nonce, @hash = mine_block
  end

  def mine_block(difficulty = '00')
    nonce = 0
    loop do
      hash = calc_hash_with_nonce(nonce)
      if hash.start_with?(difficulty)
        return [nonce, hash]
      else
        nonce += 1
      end
    end
  end

  def calc_hash_with_nonce(nonce)
    sha = Digest::SHA256.new
    sha.update(@index.to_s + @timestamp.to_s + @transactions.to_s + @prev_hash + nonce.to_s)
    sha.hexdigest
  end
end

class Blockchain
  attr_reader :chain

  def initialize
    @chain = [create_genesis_block]
  end

  def add_block(transactions)
    prev_block = @chain[-1]
    new_block = Block.new(@chain.length, transactions, prev_block.hash)
    @chain << new_block
  end

  private

  def create_genesis_block
    Block.new(0, "Genesis Block", "0")
  end
end

# Example Usage
blockchain = Blockchain.new
blockchain.add_block("Transaction 1: Alice sends 1 coin to Bob")
blockchain.add_block("Transaction 2: Bob sends 2 coins to Charlie")

blockchain.chain.each do |block|
  puts "Block #{block.index}:"
  puts "Nonce: #{block.nonce}"
  puts "Hash: #{block.hash}"
  puts "Previous Hash: #{block.prev_hash}"
  puts "Transactions: #{block.transactions}"
  puts "-" * 20
end
