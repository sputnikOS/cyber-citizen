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

def nvidia():
# Command to execute
    command = "nvidia-smi"

    # Run the command and get the output
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Print the output
        print("Output:")
        print(Fore.LIGHTWHITE_EX+result.stdout)
        
        # Print any error message
        if result.stderr:
            print("Error:")
            print(result.stderr)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def main():
    display()
    cpu_performance()
    memory_performance()
    disk_performance()
    network_performance()
    nvidia()

if __name__ == "__main__":
    colorama.init
    banner()
    execution_time = timeit.timeit(main, number=1)
    print(f"\nBenchmark completed in {execution_time:.2f} seconds.")
