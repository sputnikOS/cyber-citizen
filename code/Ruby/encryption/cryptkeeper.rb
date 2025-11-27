require 'openssl'
require 'base64'
require 'optparse'

# Utility module for cryptographic operations
module CryptoUtils
  def self.encrypt(data, cipher_name, key, iv = nil)
    cipher = OpenSSL::Cipher.new(cipher_name)
    cipher.encrypt
    cipher.key = key
    cipher.iv = iv if iv

    encrypted = cipher.update(data) + cipher.final
    Base64.encode64(encrypted)
  end

  def self.decrypt(encrypted_data, cipher_name, key, iv = nil)
    cipher = OpenSSL::Cipher.new(cipher_name)
    cipher.decrypt
    cipher.key = key
    cipher.iv = iv if iv

    decrypted = cipher.update(Base64.decode64(encrypted_data)) + cipher.final
    decrypted
  end

  def self.encrypt_file(input_file, output_file, cipher_name, key, iv = nil)
    File.open(output_file, 'wb') do |outf|
      File.open(input_file, 'rb') do |inf|
        while (data = inf.read(4096))
          encrypted = encrypt(data, cipher_name, key, iv)
          outf.write(Base64.decode64(encrypted))
        end
      end
    end
  end

  def self.decrypt_file(input_file, output_file, cipher_name, key, iv = nil)
    File.open(output_file, 'wb') do |outf|
      File.open(input_file, 'rb') do |inf|
        while (data = inf.read(4096))
          decrypted = decrypt(Base64.encode64(data), cipher_name, key, iv)
          outf.write(decrypted)
        end
      end
    end
  end
end

# Command line interface for the file encryption/decryption program
class FileCryptoCLI
  def initialize
    @options = {}
    parse_options
    validate_options
  end

  def run
    key = Base64.decode64(@options[:key])
    iv = @options[:iv] ? Base64.decode64(@options[:iv]) : nil

    case @options[:action]
    when :encrypt_file
      CryptoUtils.encrypt_file(@options[:input], @options[:output], @options[:cipher], key, iv)
      puts "File encrypted successfully to #{@options[:output]}"
    when :decrypt_file
      CryptoUtils.decrypt_file(@options[:input], @options[:output], @options[:cipher], key, iv)
      puts "File decrypted successfully to #{@options[:output]}"
    when :encrypt_string
      encrypted_data = CryptoUtils.encrypt(@options[:data], @options[:cipher], key, iv)
      puts "Encrypted Data: #{encrypted_data}"
    when :decrypt_string
      decrypted_data = CryptoUtils.decrypt(@options[:data], @options[:cipher], key, iv)
      puts "Decrypted Data: #{decrypted_data}"
    else
      puts "Unknown action #{@options[:action]}"
    end
  rescue ArgumentError => e
    puts "Error: #{e.message}"
  rescue OpenSSL::Cipher::CipherError => e
    puts "Error: Invalid cipher or encryption parameters. Please check the cipher name and key/IV."
  rescue => e
    puts "An unexpected error occurred: #{e.message}"
  end

  private

  def parse_options
    OptionParser.new do |opts|
      opts.banner = "Usage: file_crypto.rb [options]"

      opts.on("-e", "--encrypt-file", "Encrypt the input file") { @options[:action] = :encrypt_file }
      opts.on("-d", "--decrypt-file", "Decrypt the input file") { @options[:action] = :decrypt_file }
      opts.on("-s", "--encrypt-string DATA", "Encrypt the given string") { |data| @options[:data] = data; @options[:action] = :encrypt_string }
      opts.on("-r", "--decrypt-string DATA", "Decrypt the given string") { |data| @options[:data] = data; @options[:action] = :decrypt_string }
      opts.on("-i", "--input FILE", "Input file") { |file| @options[:input] = file }
      opts.on("-o", "--output FILE", "Output file") { |file| @options[:output] = file }
      opts.on("-k", "--key KEY", "Encryption key (base64)") { |key| @options[:key] = key }
      opts.on("-v", "--iv IV", "Initialization vector (base64)") { |iv| @options[:iv] = iv }
      opts.on("-c", "--cipher CIPHER", "Cipher algorithm (aes-256-cbc, des-ede3, rc4, etc.)") { |cipher| @options[:cipher] = cipher }
      opts.on("-h", "--help", "Show this help message") { puts opts; exit }
    end.parse!
  end

  def validate_options
    if @options[:action].nil? || @options[:key].nil? || @options[:cipher].nil?
      puts "Missing required arguments. Use -h for help."
      exit
    end

    if [:encrypt_file, :decrypt_file].include?(@options[:action]) && (@options[:input].nil? || @options[:output].nil?)
      puts "Missing input or output file. Use -h for help."
      exit
    end

    if [:encrypt_string, :decrypt_string].include?(@options[:action]) && @options[:data].nil?
      puts "Missing data to encrypt/decrypt. Use -h for help."
      exit
    end
  end
end

# Run the CLI if this file is executed directly
if __FILE__ == $0
  FileCryptoCLI.new.run
end
