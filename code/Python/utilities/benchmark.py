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
import sounddevice as sd
import argparse

# Optional: Install GPUtil for GPU monitoring if needed (currently commented out)
# import GPUtil

from rich.console import Console
from rich.table import Table
from prettytable import PrettyTable


def banner():
    print(Fore.LIGHTCYAN_EX + """
=======================================================================================================
                    ####    #    #### ##### #   # ##### #   # #   # #   #      ###   ####
                    #   #  # #  #     #   #  # #    #   #   # #  ## #  #      #   # #
                    ####  ##### #     #   #   #     #   ##### # # # ###       #   # #
                    #     #   # #     #   #  #      #   #   # ##  # #  #      #   # #
                    #     #   #  #### #   # #       #   #   # #   # #   #      ###   ####
=======================================================================================================
                                
                    https://www.github.com/sputnikOS
                            0.1.2-curiosity 
                                GPLv3
                  
                    usage: benchmark.py [option]
                    options:
                        -h, --help  show this help message and exit
                        --all       Run all benchmarks
                        --cpu       Display CPU performance
                        --memory    Display memory performance
                        --disk      Display disk performance
                        --network   Display network performance
                        --speed     Run speed test
                        --gpu       Check GPU info
                        --battery   Display battery info (Windows)
                        --info      Display basic system info
          
========================================================================================================      
========================================================================================================
          
    """ + Style.RESET_ALL)

def clearScr():
    os.system('cls ')


def list_network_interfaces():
    # Get the network interfaces
    interfaces = psutil.net_if_addrs()

    # Print the interfaces and their addresses
    for interface, addresses in interfaces.items():
        print(f"Interface: {interface}")
        for address in addresses:
            print(f"  Address Family: {address.family.name}")
            print(f"  Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast: {address.broadcast}")
            print()
# Function to list audio devices
def list_audio_devices():
    devices = sd.query_devices()  # Get list of all audio devices
    print("Available audio devices:\n")
    
    for idx, device in enumerate(devices):
        print(f"Device #{idx}: {device['name']}")
        print(f"  - Default sample rate: {device['default_samplerate']} Hz")
        print(f"  - Input channels: {device['max_input_channels']}")
        print(f"  - Output channels: {device['max_output_channels']}")
        print(f"  - Host API: {device['hostapi']}\n")


def display_system_info():
    console = Console() 
    table = PrettyTable() 
    table.field_names = ["Key", "Value"] 
    table.add_row(["Time", time.ctime()]) 
    table.add_row(["Directory", os.getcwd()]) 
    table.add_row(["Platform", platform.platform()])
    table.add_row(["Node", platform.node()])
    table.add_row(["OS", platform.uname()])
    table.add_row(["Architecture", platform.architecture()])
    print(table)

def cpu_performance():
    """Display CPU performance."""
    print(Fore.RED + "\nCPU Performance Benchmark:" + Style.RESET_ALL)
    cpu_percent = psutil.cpu_percent()
    count = psutil.cpu_count(logical=False)
    print(Fore.LIGHTGREEN_EX + f"CPU Usage: {cpu_percent}%" + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX + f"CPU Count: {count} cores" + Style.RESET_ALL)

def get_battery():
    """Get CPU temperature on Windows."""
    battery = psutil.sensors_battery()
    print(f"Battery: {battery}")


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
    parser = argparse.ArgumentParser(description="System Benchmark and Monitoring Tool")
    parser.add_argument('--all', action='store_true', help='Run all benchmarks')
    parser.add_argument('--cpu', action='store_true', help='Display CPU performance')
    parser.add_argument('--memory', action='store_true', help='Display memory performance')
    parser.add_argument('--disk', action='store_true', help='Display disk performance')
    parser.add_argument('--network', action='store_true', help='Display network performance')
    parser.add_argument('--speed', action='store_true', help='Run speed test')
    parser.add_argument('--gpu', action='store_true', help='Check GPU info')
    parser.add_argument('--battery', action='store_true', help='Display battery info (Windows)')
    parser.add_argument('--info', action='store_true', help='Display basic system info')
    args = parser.parse_args()

    

    if args.all:
        display_system_info()
        cpu_performance()
        memory_performance()
        disk_performance()
        network_performance()
        test_speed()
        nvidia()
        get_battery()
    if args.cpu:
        cpu_performance()
    if args.memory:
        memory_performance()
    if args.disk:
        disk_performance()
    if args.network:
        network_performance()
    if args.speed:
        test_speed()
    if args.gpu:
        nvidia()
    if args.battery:
        get_battery()
    if args.info:
        display_system_info()
 
if __name__ == "__main__":
    colorama.init()
    clearScr()  # Ensure colorama is initialized
    banner()
    
    execution_time = timeit.timeit(main, number=1)
    print(f"\nBenchmark completed in {execution_time:.2f} seconds.")
