require 'securerandom'
require 'digest'
require 'optparse'
require 'artii'
require 'colorize'

# This method clears the terminal screen
def clear_terminal
  if Gem.win_platform?
    system('cls') # Windows command to clear terminal
  else
    system('clear') # Unix/Linux/Mac command to clear terminal
  end
end

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
    new_block.mine_block
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

  # Display a specific block
  def display_block(index)
    if index >= 0 && index < @chain.length
      puts @chain[index]
    else
      puts "Block not found"
    end
  end

  # Display a specific wallet by address
  def display_wallet(address)
    wallet = @wallets.find { |w| w.address == address }
    if wallet
      puts wallet
    else
      puts "Wallet not found"
    end
  end

  # List all wallets
  def list_wallets
    if @wallets.empty?
      puts "No wallets found"
    else
      @wallets.each { |wallet| puts wallet }
    end
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
  attr_accessor :index, :data, :timestamp, :previous_hash, :hash, :nonce

  def initialize(index, data, previous_hash)
    @index = index
    @data = data
    @timestamp = Time.now.to_i
    @previous_hash = previous_hash
    @nonce = 0
    @hash = calculate_hash
  end

  # Calculate the hash of the block
  def calculate_hash
    content = "#{@index}#{@data}#{@timestamp}#{@previous_hash}#{@nonce}"
    Digest::SHA256.hexdigest(content)
  end

  # Mine the block using a simple proof-of-work algorithm
  def mine_block(difficulty = 2)
    target = '0' * difficulty
    until @hash.start_with?(target)
      @nonce += 1
      @hash = calculate_hash
    end
    puts "Block mined: #{@hash}"
  end

  def to_s
    "Block #{@index}: #{@data}, Timestamp: #{@timestamp}, Hash: #{@hash}, Previous Hash: #{@previous_hash}, Nonce: #{@nonce}"
  end
end

# Command line argument parsing
options = {}
OptionParser.new do |opts|
  opts.banner = "Usage: blockchain.rb [options]"

  opts.on("-d", "--display-block INDEX", "Display block at INDEX") do |index|
    options[:display_block] = index.to_i
  end

  opts.on("-m", "--mine-block DATA", "Mine and add a block with DATA") do |data|
    options[:mine_block] = data
  end

  opts.on("-w", "--display-wallet ADDRESS", "Display wallet with ADDRESS") do |address|
    options[:display_wallet] = address
  end

  opts.on("-n", "--new-wallet", "Generate a new wallet") do
    options[:new_wallet] = true
  end

  opts.on("-l", "--list-wallets", "List all wallets") do
    options[:list_wallets] = true
  end
end.parse!

# Example usage
clear_terminal
a = Artii::Base.new :font => 'computer'
header = a.asciify('SputnikOS')
puts header.colorize(:green)

# Initialize blockchain
blockchain = Blockchain.new

# Add a genesis crypto token
genesis_token = CryptoToken.new("GenesisToken", "GEN", 1000000)
blockchain.add_token(genesis_token)
puts "Added Genesis Token: #{genesis_token}"

# Process command line options
if options[:display_block]
  blockchain.display_block(options[:display_block])
elsif options[:mine_block]
  blockchain.add_block(options[:mine_block])
  puts "Block mined and added to blockchain."
elsif options[:display_wallet]
  blockchain.display_wallet(options[:display_wallet])
elsif options[:new_wallet]
  wallet = blockchain.create_wallet
  puts "New wallet created: #{wallet}"
elsif options[:list_wallets]
  blockchain.list_wallets
else
  # Default action, display blockchain
  puts "\nBlockchain:".colorize(:green)
  blockchain.display_chain
end

# Verify blockchain integrity
puts "\nIs the blockchain valid? #{blockchain.valid_chain?}"
