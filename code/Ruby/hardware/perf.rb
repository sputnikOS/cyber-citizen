require 'benchmark'
require 'sys/cpu'
# require 'sys/filesystem'
require 'net/ping'

include Sys

def cpu_info
  puts "CPU Model: #{CPU.processors.first.model_name}"
  # puts "CPU Speed: #{CPU.processor.} MHz"
end

def memory_info
  mem_info = `free -m`
  puts mem_info
end

# def disk_info
#   stat = Filesystem.stat('/')
#   puts "Filesystem: #{stat.filesystem_type}"
#   puts "Total Space: #{stat.bytes_total / 1024 / 1024} MB"
#   puts "Free Space: #{stat.bytes_free / 1024 / 1024} MB"
# end

def network_latency
  check = Net::Ping::External.new('8.8.8.8')
  if check.ping
    puts "Ping to 8.8.8.8: #{check.duration * 1000} ms"
  else
    puts "Ping to 8.8.8.8 failed."
  end
end

def io_benchmark
  result = Benchmark.measure do
    file = File.new("testfile", "w+")
    1_000_000.times { file.puts("This is a benchmark test.") }
    file.close
  end
  puts "I/O Benchmark Time: #{result.real} seconds"
end

def cpu_benchmark
  Benchmark.bm do |x|
    x.report("CPU Intensive Task: ") do
      (1..5000).reduce(:*)
    end
  end
end

puts "CPU Information:"
cpu_info

puts "\nMemory Information:"
memory_info

puts "\nDisk Information:"
disk_info

puts "\nNetwork Latency:"
network_latency

puts "\nI/O Benchmark:"
io_benchmark

puts "\nCPU Benchmark:"
cpu_benchmark
