require 'securerandom'
require 'digest'
require 'colorize'

# Class representing a Crypto Token
class CryptoToken
  attr_accessor :name, :symbol, :total_supply

  def initialize(name, symbol, total_supply)
    @name = name
    @symbol = symbol
    @total_supply = total_supply
  end

  def to_s
    "#{@name} (#{@symbol}) - Total Supply: #{@total_supply}"
  end
end

# Class representing a Wallet
class Wallet
  attr_accessor :address, :balance

  def initialize
    # Generate a random wallet address (UUID for simplicity)
    @address = SecureRandom.hex(16)
    @balance = 0
  end

  def deposit(amount)
    @balance += amount
  end

  def withdraw(amount)
    if @balance >= amount
      @balance -= amount
    else
      puts "Insufficient funds"
    end
  end

  def to_s
    "Wallet Address: #{@address}, Balance: #{@balance}"
  end
end

# Class representing the Blockchain
class Blockchain
  attr_accessor :chain, :tokens, :wallets

  def initialize
    @chain = []
    @tokens = []
    @wallets = []
    create_genesis_block
  end

  # Create the first block in the blockchain (genesis block)
  def create_genesis_block
    genesis_block = Block.new(0, "Genesis Block", "0")
    @chain << genesis_block
  end

  # Add a block to the blockchain
  def add_block(data)
    previous_hash = @chain.last.hash
    new_block = Block.new(@chain.length, data, previous_hash)
    @chain << new_block
  end

  # Add a crypto token to the blockchain
  def add_token(token)
    @tokens << token
  end

  # Add a wallet to the blockchain
  def create_wallet
    wallet = Wallet.new
    @wallets << wallet
    wallet
  end

  # Display blockchain
  def display_chain
    @chain.each { |block| puts block }
  end

  # Verify blockchain integrity
  def valid_chain?
    @chain.each_with_index do |block, index|
      next if index == 0
      previous_block = @chain[index - 1]
      return false if block.previous_hash != previous_block.hash
      return false if block.hash != block.calculate_hash
    end
    true
  end
end

# Class representing a Block in the blockchain
class Block
  attr_accessor :index, :data, :timestamp, :previous_hash, :hash

  def initialize(index, data, previous_hash)
    @index = index
    @data = data
    @timestamp = Time.now.to_i
    @previous_hash = previous_hash
    @hash = calculate_hash
  end

  # Calculate the hash of the block
  def calculate_hash
    content = "#{@index}#{@data}#{@timestamp}#{@previous_hash}"
    Digest::SHA256.hexdigest(content)
  end

  def to_s
    "Block #{@index}: #{@data}, Timestamp: #{@timestamp}, Hash: #{@hash}, Previous Hash: #{@previous_hash}"
  end
end

# Example usage

# Initialize blockchain
blockchain = Blockchain.new

# Add a crypto token
oss = CryptoToken.new("Sputnik", "OSS", 100)
blockchain.add_token(oss)
puts "Added Token: #{oss}"



# Display blockchain
puts "\nBlockchain:".colorize(:green)
blockchain.display_chain

# Verify blockchain integrity
puts "\nIs the blockchain valid? #{blockchain.valid_chain?}"
