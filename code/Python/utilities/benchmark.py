import os
import platform
import psutil
import time
import timeit
import subprocess
import colorama
from colorama import Fore, Style, init
import humanize
import sounddevice as sd
import soundfile as sf
import argparse

# Optional: Install GPUtil for GPU monitoring if needed (currently commented out)
# import GPUtil

from rich.console import Console
from rich.table import Table
from prettytable import PrettyTable


def banner():
    divider = (Fore.BLUE + """      
===================================================================================================================================================================          
===================================================================================================================================================================
    """ + Style.RESET_ALL)
    header = (Fore.LIGHTYELLOW_EX + """
          
                    ####    #    #### ##### #   # ##### #   # #   # #   #      ###   ####
                    #   #  # #  #     #   #  # #    #   #   # #  ## #  #      #   # #
                    ####  ##### #     #   #   #     #   ##### # # # ###       #   # #
                    #     #   # #     #   #  #      #   #   # ##  # #  #      #   # #
                    #     #   #  #### #   # #       #   #   # #   # #   #      ###   ####

                                        https://www.github.com/sputnikOS
                                                GPLv3 License    
                                        usage: python3 benchmark.py [options]       
                               
          """ + Style.RESET_ALL)
  
    
    print(divider)
    print(header)
    print(divider)

def clear_terminal():
    """Clear the terminal screen based on the OS."""
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix-based systems (Linux/macOS)
        os.system('clear')

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
    # List all audio devices (input and output)
    devices = sd.query_devices()
    
    print("Audio Devices:")
    for i, device in enumerate(devices):
        print(f"Device {i}: {device['name']} - {'Input' if device['max_input_channels'] > 0 else 'Output'}")

def list_supported_formats():
    # List common supported audio formats for reading/writing with soundfile
    formats = sf.available_formats()
    
    print("\nSupported Audio Formats:")
    for fmt in formats:
        print(f" - {fmt}")


def display_system_info():
    console = Console() 
    table = PrettyTable() 
    table.field_names = ["Key", "Value"] 
    table.add_row(["Time", time.ctime()]) 
    # table.add_row(["User", os.getlogin()])
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
    
    # Get memory details
    memory = psutil.virtual_memory()
    
    # Display overall memory usage
    print(f"Total Memory: {humanize.naturalsize(memory.total)}")
    print(f"Used Memory: {humanize.naturalsize(memory.used)}")
    print(f"Available Memory: {humanize.naturalsize(memory.available)}")
    print(f"Memory Usage: {memory.percent}%")
    
def ram_performance():
    """Analyze RAM performance over time."""
    print(Fore.LIGHTGREEN_EX + "\nRAM Performance Over Time:" + Style.RESET_ALL)
    
    # Measure memory usage over a period
    start_time = time.time()
    for i in range(10):  # Example: monitor over 10 seconds
        memory = psutil.virtual_memory()
        print(f"Time: {time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))}")
        print(f"Used Memory: {humanize.naturalsize(memory.used)} | Available Memory: {humanize.naturalsize(memory.available)} | Memory Usage: {memory.percent}%")
        time.sleep(1)  # Sleep for 1 second before the next update
        

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
    parser.add_argument('--nvidia', action='store_true', help='Check GPU info')
    parser.add_argument('--battery', action='store_true', help='Display battery info (Windows)')
    parser.add_argument('--info', action='store_true', help='Display basic system info')
    parser.add_argument('--audio', action='store_true', help='Display audio')
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
        ram_performance()
    if args.disk:
        disk_performance()
    if args.network:
        network_performance()
    if args.speed:
        test_speed()
    if args.nvidia:
        nvidia()
    if args.battery:
        get_battery()
    if args.info:
        display_system_info()
    if args.audio:
        list_audio_devices()
        list_supported_formats()

if __name__ == "__main__":

    # Initialize colorama
    init(autoreset=True)
    clear_terminal()  # Ensure colorama is initialized
    banner()
    
    execution_time = timeit.timeit(main, number=1)
    print(f"\nBenchmark completed in {execution_time:.2f} seconds.")
