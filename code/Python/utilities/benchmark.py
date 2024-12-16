import os
import pstats
import time
import platform
import subprocess
import psutil
import timeit
import colorama
from colorama import Fore, Style
import humanize

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

    

def display():
    print("\033[91m\tTime: \033[0m" + time.ctime())
    print("\033[91m\tCurrent directory: \033[0m" + os.getcwd())
    print("\033[91m\tOperation System: \033[0m" + platform.platform())
    print("\033[91m\tNode: \033[0m" + platform.node())
    print("\033[91m\tOS Version: \033[0m" + platform.uname()[3])
    print("\033[91m\tSystem Type: \033[0m" + platform.architecture()[0])
    print("\033")

def cpu_performance():

    print(Fore.RED + "CPU Performance Benchmark:"  + Style.RESET_ALL)
    cpu_percent = psutil.cpu_percent()
    count = psutil.cpu_count()
    print(Fore.LIGHTGREEN_EX + f"CPU Usage: {cpu_percent}%" + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX + f"CPU Count: {count} cores" + Style.RESET_ALL)



def memory_performance():

    print(Fore.LIGHTYELLOW_EX + "\nMemory Performance Benchmark:" + Style.RESET_ALL)
    memory = psutil.virtual_memory()
    print(f"Memory: {humanize.naturalsize(memory.used)}/{humanize.naturalsize(memory.total)} bytes")


    print("\033")
    print("\t" + "#" * 80 + "#")


def disk_performance():
    print(Fore.LIGHTBLUE_EX + "\nDisk Performance Benchmark:")
    disk_usage = psutil.disk_usage('/')
    print(f"Total Disk Space: {humanize.naturalsize(disk_usage.total)} bytes")
    print(f"Used Disk Space: {humanize.naturalsize(disk_usage.used)} bytes")
    print(f"Disk Usage Percentage: {disk_usage.percent}%")


def network_performance():
    print(Fore.LIGHTMAGENTA_EX + "\nNetwork Performance Benchmark:")
    network_speed = psutil.net_io_counters()
    print(f"Packets Sent: {humanize.naturalsize(network_speed.packets_sent)}")
    print(f"Packets Received: {humanize.naturalsize(network_speed.packets_recv)}")
    print(f"Bytes Sent: {humanize.naturalsize(network_speed.bytes_sent)}")
    print(f"Bytes Received: {humanize.naturalsize(network_speed.bytes_recv)}")
    
    import time

# Function to test the speed of an operation
def test_speed():
    # Start the timer
    start_time = time.time()

    # Example operation: summing a large range of numbers
    total = sum(range(1, 10**7))  # Adjust the range for more or less computation

    # End the timer
    end_time = time.time()

    # Calculate the duration
    duration = end_time - start_time

    # Calculate the total size of numbers processed in bytes
    # Assuming each integer takes 4 bytes
    total_size_in_bytes = len(range(1, 10**7)) * 4  # 4 bytes per integer

    # Convert the size to gigabytes (GB)
    total_size_in_gb = total_size_in_bytes / (1024 ** 3)  # 1024^3 to convert to GB

    # Calculate the speed in gigabytes per second (GB/s)
    speed_in_gbps = total_size_in_gb / duration if duration > 0 else 0

    # Output the formatted result
    print("="*40)
    print(" Speed Test Results ".center(40, "="))
    print("="*40)
    print(f"Operation: Summing numbers from 1 to 10 million")
    print(f"Total Sum: {total:,}")  # Format the total with commas
    print(f"Total Processed Data: {total_size_in_gb:.6f} GB")
    print(f"Speed: {speed_in_gbps:.6f} GB/s")
    print(f"Time Taken: {duration:.6f} seconds")
    print("="*40)

def nvidia():
# Command to execute
    command = "nvidia-smi"

    # Run the command and get the output
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Print the outpu
        print(Fore.LIGHTWHITE_EX+result.stdout)
        
        # Print any error message
        if result.stderr:
            print(result.stderr)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")



def main():
    display()
    cpu_performance()
    memory_performance()
    disk_performance()
    network_performance()
    test_speed()
    nvidia()

if __name__ == "__main__":
    colorama.init
    banner()
    execution_time = timeit.timeit(main, number=1)
    print(f"\nBenchmark completed in {execution_time:.2f} seconds.")
