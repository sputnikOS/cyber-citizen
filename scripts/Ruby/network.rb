require 'socket'
require 'net/ping'

def my_local_ip
  # Get the local IP address of the machine running the script
  orig, Socket.do_not_reverse_lookup = Socket.do_not_reverse_lookup, true  # Turn off reverse DNS resolution temporarily

  UDPSocket.open do |s|
    s.connect('8.8.8.8', 1)
    s.addr.last
  end
ensure
  Socket.do_not_reverse_lookup = orig
end

def scan_network(base_ip, start_range, end_range)
  (start_range..end_range).each do |num|
    target_ip = "#{base_ip}.#{num}"
    if Net::Ping::External.new(target_ip).ping
      puts "Device found at: #{target_ip}"
    else
      puts "No device at: #{target_ip}"
    end
  end
end

# Example usage
local_ip = my_local_ip
base_ip = local_ip[0..local_ip.rindex('.')]
start_range = 1
end_range = 254

puts "Scanning network: #{base_ip}.1 to #{base_ip}.254"
scan_network(base_ip, start_range, end_range)
