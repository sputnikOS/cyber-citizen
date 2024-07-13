require 'openssl'
require 'colorize'
# Generate a 2048-bit RSA key
key = OpenSSL::PKey::RSA.generate(2048)

# Get the public key
public_key = key.public_key

str = "\n#==============================================================="
# Print the public key
puts "Public Key" + ":\n#{public_key}"
puts str.colorize(:green)
 # Print the private key (for demonstration purposes)
puts "Private Key:\n#{key}"
