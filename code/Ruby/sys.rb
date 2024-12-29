require 'sys/proctable'
require 'sys/uname'
require 'socket'
require 'terminal-table'
require 'colorize'
require 'artii'


def get_os_info
  os_info = Sys::Uname.uname
  {
    "System" => os_info.sysname,
    "Node Name" => os_info.nodename,
    "Release" => os_info.release,
    "Version" => os_info.version,
    "Machine" => os_info.machine
  }
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
  mem_info = {}
  File.readlines('/proc/meminfo').each do |line|
    key, value = line.split(':')
    mem_info[key.strip] = value.strip if key && value
  end
  mem_info
end

def get_disk_info
  disk_info = `df -h`
  disk_info
end

def get_network_info
  hostname = Socket.gethostname
  ip_address = Socket.ip_address_list.detect(&:ipv4_private?).ip_address
  {
    "Hostname" => hostname,
    "IP Address" => ip_address
  }
end

def get_uptime
  uptime_seconds = File.read('/proc/uptime').split[0].to_i
  uptime_string = Time.at(uptime_seconds).utc.strftime("%H:%M:%S")
  {
    "Uptime (seconds)" => uptime_seconds,
    "Uptime (formatted)" => uptime_string
  }
end

def display_table(title, data)
  rows = data.map { |key, value| [key, value] }
  table = Terminal::Table.new(title: title, rows: rows)
  puts table
end

def display_info
  artii = Artii::Base.new(font: "slant")
  puts artii.asciify("SYS")
  puts "System Information".colorize(:yellow).center(40, "=")
  display_table("OS Information", get_os_info)

  puts "\nCPU Information".colorize(:yellow).center(40, "=")
  display_table("CPU Information", get_cpu_info)

  puts "\nMemory Information".colorize(:yellow).center(40, "=")
  display_table("Memory Information", get_memory_info)

  puts "\nDisk Information".colorize(:yellow).center(40, "=")
  puts get_disk_info.colorize(:green)

  puts "\nNetwork Information".colorize(:yellow).center(40, "=")
  display_table("Network Information", get_network_info)

  puts "\nUptime Information".colorize(:yellow).center(40, "=")
  display_table("Uptime Information", get_uptime)
end

display_info
