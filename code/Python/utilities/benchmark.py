import os
import platform
import psutil
import time
import timeit
import subprocess
import colorama
from colorama import Fore, Style
import humanize
import wmi

# Optional: Install GPUtil for GPU monitoring if needed (currently commented out)
# import GPUtil

def banner():
    print(Fore.MAGENTA + """
 =======================================================================
  ####    #    #### ##### #   # ##### #   # #   # #   #      ###   ####
  #   #  # #  #     #   #  # #    #   #   # #  ## #  #      #   # #
  ####  ##### #     #   #   #     #   ##### # # # ###       #   # #
  #     #   # #     #   #  #      #   #   # ##  # #  #      #   # #
  #     #   #  #### #   # #       #   #   # #   # #   #      ###   ####
  ======================================================================
                    version 0.1.2-alpha (curiosity)
                    License: GPLv3
                    https://www.github.com/sputnikOS
  =======================================================================
    """ + Style.RESET_ALL)

def display_system_info():
    """Display system information."""
    print(Fore.CYAN + f"Time: {time.ctime()}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Operating System: {platform.platform()}")
    print(f"Node: {platform.node()}")
    print(f"OS Version: {platform.uname()[3]}")
    print(f"System Type: {platform.architecture()[0]}")
    print(Style.RESET_ALL)

def cpu_performance():
    """Display CPU performance."""
    print(Fore.RED + "\nCPU Performance Benchmark:" + Style.RESET_ALL)
    cpu_percent = psutil.cpu_percent()
    count = psutil.cpu_count(logical=False)
    print(Fore.LIGHTGREEN_EX + f"CPU Usage: {cpu_percent}%" + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX + f"CPU Count: {count} cores" + Style.RESET_ALL)

def get_cpu_temp_windows():
    """Get CPU temperature on Windows."""
    w = wmi.WMI(namespace="root\\wmi")
    temperature_info = w.MSAcpi_ThermalZoneTemperature()
    for temp in temperature_info:
        # WMI temperature is in tenths of Kelvin, convert it to Celsius
        temp_celsius = (temp.CurrentTemperature / 10) - 273.15
        return temp_celsius
    return "Unable to get CPU temperature"

def memory_performance():
    """Display memory performance."""
    print(Fore.LIGHTYELLOW_EX + "\nMemory Performance Benchmark:" + Style.RESET_ALL)
    memory = psutil.virtual_memory()
    print(f"Memory: {humanize.naturalsize(memory.used)}/{humanize.naturalsize(memory.total)} bytes")

def disk_performance():
    """Display disk performance."""
    print(Fore.LIGHTBLUE_EX + "\nDisk Performance Benchmark:")
    disk_usage = psutil.disk_usage('/')
    print(f"Total Disk Space: {humanize.naturalsize(disk_usage.total)} bytes")
    print(f"Used Disk Space: {humanize.naturalsize(disk_usage.used)} bytes")
    print(f"Disk Usage Percentage: {disk_usage.percent}%")

def network_performance():
    """Display network performance."""
    print(Fore.LIGHTMAGENTA_EX + "\nNetwork Performance Benchmark:")
    network_speed = psutil.net_io_counters()
    print(f"Packets Sent: {humanize.naturalsize(network_speed.packets_sent)}")
    print(f"Packets Received: {humanize.naturalsize(network_speed.packets_recv)}")
    print(f"Bytes Sent: {humanize.naturalsize(network_speed.bytes_sent)}")
    print(f"Bytes Received: {humanize.naturalsize(network_speed.bytes_recv)}")

def test_speed():
    """Test speed of a computational operation."""
    start_time = time.time()
    total = sum(range(1, 10**7))  # Sum of numbers from 1 to 10 million
    end_time = time.time()
    
    duration = end_time - start_time
    total_size_in_bytes = len(range(1, 10**7)) * 4  # 4 bytes per integer
    total_size_in_gb = total_size_in_bytes / (1024 ** 3)  # Convert to GB
    speed_in_gbps = total_size_in_gb / duration if duration > 0 else 0

    print("=" * 40)
    print(" Speed Test Results ".center(40, "="))
    print("=" * 40)
    print(f"Operation: Summing numbers from 1 to 10 million")
    print(f"Total Sum: {total:,}")
    print(f"Total Processed Data: {total_size_in_gb:.6f} GB")
    print(f"Speed: {speed_in_gbps:.6f} GB/s")
    print(f"Time Taken: {duration:.6f} seconds")
    print("=" * 40)

def nvidia():
    """Display GPU info using nvidia-smi (if available)."""
    try:
        result = subprocess.run("nvidia-smi", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(Fore.LIGHTWHITE_EX + result.stdout)
        if result.stderr:
            print(result.stderr)
    except FileNotFoundError:
        print("nvidia-smi not found, make sure NVIDIA drivers are installed.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def main():
    """Main function to run all benchmarks."""
    display_system_info()
    cpu_performance()
    memory_performance()
    disk_performance()
    network_performance()
    test_speed()
    # get_cpu_temp_windows()
    nvidia()

if __name__ == "__main__":
    colorama.init()  # Ensure colorama is initialized
    banner()
    execution_time = timeit.timeit(main, number=1)
    print(f"\nBenchmark completed in {execution_time:.2f} seconds.")
