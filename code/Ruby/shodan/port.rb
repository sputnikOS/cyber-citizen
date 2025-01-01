require 'socket'
require 'net/http'
require 'openssl'

# Function to perform a port scan on the target
def port_scan(target, ports)
  open_ports = []

  ports.each do |port|
    begin
      socket = Socket.tcp(target, port, connect_timeout: 1)
      open_ports << port
    rescue Errno::ECONNREFUSED, Errno::ETIMEDOUT
      # Connection refused or timeout means the port is closed or filtered
    ensure
      socket.close if socket
    end
  end

  open_ports
end

# Function to get service information for a specific port
def get_service_info(target, port)
  begin
    socket = Socket.tcp(target, port, connect_timeout: 1)
    socket.puts "HEAD / HTTP/1.0\r\n\r\n"
    response = socket.read
    return response
  rescue => e
    return "Error retrieving service info: #{e.message}"
  ensure
    socket.close if socket
  end
end

# Example usage
target = '99.155.151.121' # Replace with the target IP address
ports = (1..1024).to_a # Scan the first 1024 ports

# Perform port scan
open_ports = port_scan(target, ports)
puts "Open ports on #{target}: #{open_ports.join(', ')}" unless open_ports.empty?

# Get service information for each open port
open_ports.each do |port|
  service_info = get_service_info(target, port)
  puts "Service info on port #{port}:"
  puts service_info
end
