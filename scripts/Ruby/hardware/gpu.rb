require 'colorize'
require 'benchmark'
require 'sysinfo'
require 'sys/cpu'
require 'open3'

# Method to display a terminal banner
def display_banner(title)
  width = 100
  padding = (width - title.length) / 2
  puts "-" * width
  puts "|" + " " * padding + title + " " * padding + "|"
  puts "-" * width
  puts
end

# Method to get GPU information using PowerShell commands (Windows example)
def get_gpu_info
  powershell_cmd = <<-CMD
  Get-WmiObject -Class Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion, CurrentRefreshRate, MaxRefreshRate
  CMD

  stdout, stderr, status = Open3.capture3("powershell -Command \"#{powershell_cmd}\"")

  if status.success?
    gpu_info = stdout.encode('UTF-8', 'binary', invalid: :replace, undef: :replace, replace: '')

    # Print formatted GPU information
    puts "GPU Information:"
    gpu_info.each_line do |line|
      puts "  #{line.strip}" unless line.strip.empty?
    end
  else
    puts "Failed to retrieve GPU information: #{stderr}"
  end
end

# Call the method to retrieve and display GPU information

# Example usage:
display_banner("GPU Hardware")
get_gpu_info



