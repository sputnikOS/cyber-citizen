require 'artii'
require 'colorize'
require 'terminal-table'
require 'io/console'

def clear_terminal
  if Gem.win_platform?
    system("cls")  # Clear command for Windows
  else
    system("clear")  # Clear command for Unix-based systems
  end
end

def get_os_info
  { "OS" => `uname -s`.strip, "Version" => `uname -r`.strip }
end

def get_cpu_info
  cpu_info = `lscpu`
  cpu_details = {}
  cpu_info.each_line do |line|
    key, value = line.split(':')
    if key && value
      cpu_details[key.strip] = value.strip
    end
  end
  cpu_details
end

def get_memory_info
  { "Total Memory" => `free -h | grep Mem | awk '{print $2}'`.strip, "Used Memory" => `free -h | grep Mem | awk '{print $3}'`.strip }
end

def get_disk_info
  `df -h`
end

def get_network_info
  { "IP Address" => `hostname -I`.strip, "MAC Address" => `cat /sys/class/net/$(ip route show default | awk '/default/ {print $5}')/address`.strip }
end

def get_uptime
  { "Uptime" => `uptime -p`.strip }
end

def center_text(text)
  terminal_width = IO.console.winsize[1] rescue 100  # Default to 100 if terminal width can't be determined
  padding = [(terminal_width - text.length) / 2, 0].max
  puts " " * padding + text
end

def display_table(title, data)
  rows = data.map { |key, value| [key, value] }
  table = Terminal::Table.new(title: title, rows: rows)
  puts table
end

def display_info
  clear_terminal
  artii = Artii::Base.new(font: "slant")
  banner = artii.asciify("SputnikOS")
  puts banner.center(140).colorize(:yellow)

  headers = ["System Information", "CPU Information", "Memory Information", "Disk Information", "Network Information", "Uptime Information"]
  methods = [method(:get_os_info), method(:get_cpu_info), method(:get_memory_info), method(:get_disk_info), method(:get_network_info), method(:get_uptime)]

  headers.each_with_index do |header, index|
  puts "\n" + "=" *   140
    puts header.center(140).colorize(:yellow)
    puts "=" * 140
    data = methods[index].call
    if header == "Disk Information"
      puts data.colorize(:green)
    else
      display_table(header, data)
    end
  end
end

# Call the function to display system information
display_info
