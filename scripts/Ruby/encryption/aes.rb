require 'openssl'
require 'base64'

# Method to encrypt a string using AES encryption
def encrypt(data, key, iv)
  cipher = OpenSSL::Cipher::AES.new(256, :CBC)
  cipher.encrypt
  cipher.key = key
  cipher.iv = iv

  encrypted = cipher.update(data) + cipher.final
  Base64.strict_encode64(encrypted)
end

# Method to decrypt an encrypted string
def decrypt(encrypted_data, key, iv)
  cipher = OpenSSL::Cipher::AES.new(256, :CBC)
  cipher.decrypt
  cipher.key = key
  cipher.iv = iv

  decrypted = cipher.update(Base64.strict_decode64(encrypted_data)) + cipher.final
  decrypted
end

# Generate random key and IV
key = OpenSSL::Cipher::AES.new(256, :CBC).random_key
iv = OpenSSL::Cipher::AES.new(256, :CBC).random_iv

# User input
print "Enter a message to encrypt: "
user_input = gets.chomp

# Encrypt user input
encrypted_message = encrypt(user_input, key, iv)
puts "Encrypted Message: #{encrypted_message}"

# Decrypt the encrypted message (for demonstration)
decrypted_message = decrypt(encrypted_message, key, iv)
puts "Decrypted Message: #{decrypted_message}"
