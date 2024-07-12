require 'net/http'
require 'json'

def fetch_my_ip
  uri = URI('https://api.ipify.org?format=json')
  response = Net::HTTP.get(uri)
  result = JSON.parse(response)
  puts "Your IP is: #{result['ip']}"
rescue => e
  puts "Error fetching IP: #{e}"
end

fetch_my_ip
