require 'openssl'
require 'base64'
require 'optparse'
require 'artii'
require 'colorize'

# Display help information
def display_help
  a = Artii::Base.new
  header = a.asciify('Cryptkeeper')

  puts header.colorize(:blue)
  puts ""
  puts "Usage: cryptkeeper.rb [options]"
  puts ""
  puts "Encrypt or decrypt data using various ciphers."
  puts ""
  puts "Options:"
  puts "  -e, --encrypt DATA        Encrypt the given DATA"
  puts "  -d, --decrypt DATA        Decrypt the given DATA"
  puts "  -k, --key KEY             Encryption key (base64 encoded)"
  puts "  -i, --iv IV               Initialization vector (base64 encoded)"
  puts "  -c, --cipher CIPHER       Cipher algorithm (e.g., aes-256-cbc, des-ede3, rc4)"
  puts "  -h, --help                Show this help message"
  puts ""
  puts "Example usage:"
  puts "  Encrypting data: ruby cryptkeeper.rb -e 'Hello, World!' -k <base64_key> -c 'aes-256-cbc' -i <base64_iv>"
  puts "  Decrypting data: ruby cryptkeeper.rb -d <base64_encrypted_data> -k <base64_key> -c 'aes-256-cbc' -i <base64_iv>"
  puts "  Encrypt with RC4: ruby cryptkeeper.rb -e 'Hello, World!' -k <base64_key> -c 'rc4'"
end

# Function to encrypt data using a specific cipher
def encrypt(data, cipher, key, iv = nil)
  cipher_obj = OpenSSL::Cipher.new(cipher)
  cipher_obj.encrypt
  cipher_obj.key = key
  cipher_obj.iv = iv if iv

  encrypted = cipher_obj.update(data) + cipher_obj.final
  Base64.encode64(encrypted)
end

# Function to decrypt data using a specific cipher
def decrypt(encrypted_data, cipher, key, iv = nil)
  cipher_obj = OpenSSL::Cipher.new(cipher)
  cipher_obj.decrypt
  cipher_obj.key = key
  cipher_obj.iv = iv if iv

  decrypted = cipher_obj.update(Base64.decode64(encrypted_data)) + cipher_obj.final
  decrypted
end

# Function to list available ciphers
def list_ciphers
  puts "Available ciphers:"
  OpenSSL::Cipher.ciphers.each do |cipher|
    puts "- #{cipher}"
  end
end

# Command-line options parsing
options = {}
OptionParser.new do |opts|
  opts.banner = "Usage: cryptkeeper.rb [options]"

  opts.on("-e", "--encrypt DATA", "Encrypt the data") do |data|
    options[:data] = data
    options[:action] = :encrypt
  end

  opts.on("-d", "--decrypt DATA", "Decrypt the data") do |data|
    options[:data] = data
    options[:action] = :decrypt
  end

  opts.on("-k", "--key KEY", "Encryption key (base64)") do |key|
    options[:key] = key
  end

  opts.on("-i", "--iv IV", "Initialization vector (base64)") do |iv|
    options[:iv] = iv
  end

  opts.on("-c", "--cipher CIPHER", "Cipher algorithm (aes-256-cbc, des-ede3, rc4, etc.)") do |cipher|
    options[:cipher] = cipher
  end

  opts.on("-h", "--help", "Show help message") do
    display_help
    exit
  end

  opts.on("-l", "--list-ciphers", "List available ciphers") do
    options[:list_ciphers] = true
  end
end.parse!

# Display available ciphers if the list-ciphers flag is set
if options[:list_ciphers]
  list_ciphers
  exit
end

# Check if necessary arguments are provided
if options[:action].nil? || options[:data].nil? || options[:key].nil? || options[:cipher].nil?
  puts "Missing required arguments. Use -e for encryption or -d for decryption."
  display_help
  exit
end

# Decode base64 for key and IV if they are provided
begin
  key = Base64.decode64(options[:key])
  iv = options[:iv] ? Base64.decode64(options[:iv]) : nil
rescue ArgumentError => e
  puts "Error: Invalid base64 encoding for key or IV. Please provide a valid base64 encoded string."
  exit
end

# Perform the requested action
begin
  if options[:action] == :encrypt
    encrypted_data = encrypt(options[:data], options[:cipher], key, iv)
    puts "Encrypted Data: #{encrypted_data}"
  elsif options[:action] == :decrypt
    decrypted_data = decrypt(options[:data], options[:cipher], key, iv)
    puts "Decrypted Data: #{decrypted_data}"
  end
rescue OpenSSL::Cipher::CipherError => e
  puts "Error: Invalid cipher or encryption parameters. Please check the cipher name and key/IV."
rescue => e
  puts "An unexpected error occurred: #{e.message}"
end
