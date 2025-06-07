require 'artii'
require 'colorize'
require 'terminal-table'
require 'io/console'

def clear_terminal
  system(Gem.win_platform? ? 'cls' : 'clear')
end

def terminal_width
  IO.console.winsize[1] rescue 100
end

def center_line(line)
  padding = [(terminal_width - line.length) / 2, 0].max
  ' ' * padding + line
end

def center_text(text, color = :default)
  puts center_line(text).colorize(color)
end

def center_block(text, color = :default)
  text.lines.each { |line| puts center_line(line.rstrip).colorize(color) }
end

def get_os_info
  { "Operating System" => `uname -s`.strip, "Kernel Version" => `uname -r`.strip }
end

def get_cpu_info
  cpu_info = `lscpu`
  cpu_details = {}
  cpu_info.each_line do |line|
    key, value = line.split(':')
    cpu_details[key.strip] = value.strip if key && value
  end
  {
    "Model Name" => cpu_details["Model name"],
    "Cores" => cpu_details["CPU(s)"],
    "Architecture" => cpu_details["Architecture"],
    "CPU MHz" => cpu_details["CPU MHz"]
  }
end

def get_memory_info
  {
    "Total Memory" => `free -h | grep Mem | awk '{print $2}'`.strip,
    "Used Memory" => `free -h | grep Mem | awk '{print $3}'`.strip,
    "Free Memory" => `free -h | grep Mem | awk '{print $4}'`.strip
  }
end

def get_disk_info
  `df -h --output=source,fstype,size,used,avail,pcent,target | grep -v tmpfs`.strip
end

def get_network_info
  iface = `ip route show default | awk '/default/ {print $5}'`.strip
  {
    "IP Address" => `hostname -I`.strip,
    "MAC Address" => iface.empty? ? "Unavailable" : `cat /sys/class/net/#{iface}/address`.strip
  }
end

def get_uptime
  { "Uptime" => `uptime -p`.strip }
end

def display_table_centered(title, data)
  rows = data.map { |key, value| [key, value] }
  table = Terminal::Table.new(title: title, rows: rows)
  table.to_s.each_line { |line| puts center_line(line.rstrip) }
end

def display_disk_info_centered(disk_text)
  disk_text.each_line { |line| puts center_line(line.rstrip).colorize(:light_green) }
end

def display_info
  clear_terminal
  artii = Artii::Base.new(font: "slant")
  center_block(artii.asciify("SputnikOS"), :green)

  center_text("Generated at: #{Time.now.strftime("%A, %d %B %Y %H:%M:%S")}", :light_black)
  puts "\n" + center_line("-" * 100)

  sections = [
    { title: "System Information", data: get_os_info },
    { title: "CPU Information", data: get_cpu_info },
    { title: "Memory Information", data: get_memory_info },
    { title: "Disk Information", data: get_disk_info },
    { title: "Network Information", data: get_network_info },
    { title: "Uptime Information", data: get_uptime }
  ]

  sections.each do |section|
    puts "\n" + center_line("=" * 100)
    center_text(section[:title], :yellow)
    puts center_line("=" * 100) + "\n"

    if section[:title] == "Disk Information"
      display_disk_info_centered(section[:data])
    else
      display_table_centered(section[:title], section[:data])
    end
  end

  puts "\n" + center_line("-" * 100)
  center_text("End of Report", :light_blue)
  puts center_line("-" * 100) + "\n\n"
end

# Execute
display_info
