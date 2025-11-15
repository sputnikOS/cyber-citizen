require 'shodan'
require 'set'
require 'dotenv/load'

API_KEY = ENV['key']
TARGET_IP = "50.87.16.103" # Replace with your network's public IP address
CHECK_INTERVAL = 3600 # Check every hour

def fetch_open_ports(api, ip)
  begin
    host_info = api.host(ip)
    ports = host_info['ports']
    Set.new(ports)
  rescue => e
    puts "Error fetching open ports: #{e}"
    Set.new
  end
end

def monitor_network(api_key, target_ip)
  api = Shodan::Shodan.new(api_key)
  known_ports = fetch_open_ports(api, target_ip)

  puts "Monitoring started for #{target_ip}..."
  puts "Known open ports at start: #{known_ports.to_a.sort.join(', ')}"

  loop do
    sleep(CHECK_INTERVAL)
    current_ports = fetch_open_ports(api, target_ip)

    new_ports = current_ports - known_ports
    unless new_ports.empty?
      puts "ALERT: New open ports detected: #{new_ports.to_a.sort.join(', ')}"
      known_ports = current_ports
    end
  end
end

monitor_network(API_KEY, TARGET_IP)
