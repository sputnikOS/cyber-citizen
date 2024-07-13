require 'sys/proctable'
include Sys

def get_cpu_usage
  `top -bn1 | grep "Cpu(s)"`.match(/(\d+\.\d+) us/)[1].to_f
end

def get_memory_usage
  mem_info = `free -m`.split("\n")[1].split
  used_mem = mem_info[2].to_f
  total_mem = mem_info[1].to_f
  mem_usage = (used_mem / total_mem) * 100
  [used_mem, total_mem, mem_usage]
end

def get_disk_usage
  disk_info = `df -m /`.split("\n")[1].split
  used_disk = disk_info[2].to_f
  total_disk = disk_info[1].to_f
  disk_usage = (used_disk / total_disk) * 100
  [used_disk, total_disk, disk_usage]
end

def display_hardware_performance
  cpu_usage = get_cpu_usage
  cpu = cpu_usage.cpu_info
  puts "#{cpu}"
  used_mem, total_mem, mem_usage = get_memory_usage
  used_disk, total_disk, disk_usage = get_disk_usage

  puts "=== Real-Time Hardware Performance ==="
  puts "CPU Usage: #{cpu_usage.round(2)}%"
  puts "Memory Usage: #{mem_usage.round(2)}% (Used: #{used_mem.round(2)} MB / Total: #{total_mem.round(2)} MB)"
  puts "Disk Usage: #{disk_usage.round(2)}% (Used: #{used_disk.round(2)} MB / Total: #{total_disk.round(2)} MB)"

  top_processes = ProcTable.ps.sort_by { |p| -p.pctcpu }.first(5)
  puts "\nTop 5 Processes by CPU Usage:"
  top_processes.each do |p|
    puts "PID: #{p.pid}: #{p.comm} - #{(p.pctcpu * 100).round(2)}%"
  end
end

loop do
  # system('clear') # For Windows, use system('cls')
  display_hardware_performance
  sleep 1
end
