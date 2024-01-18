import psutil
import timeit

def cpu_performance():
    print("CPU Performance Benchmark:")
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    print(f"CPU Usage: {cpu_percent}%")

def memory_performance():
    print("\nMemory Performance Benchmark:")
    memory = psutil.virtual_memory()
    print(f"Total Memory: {memory.total} bytes")
    print(f"Used Memory: {memory.used} bytes")
    print(f"Memory Usage Percentage: {memory.percent}%")

def disk_performance():
    print("\nDisk Performance Benchmark:")
    disk_usage = psutil.disk_usage('/')
    print(f"Total Disk Space: {disk_usage.total} bytes")
    print(f"Used Disk Space: {disk_usage.used} bytes")
    print(f"Disk Usage Percentage: {disk_usage.percent}%")

def network_performance():
    print("\nNetwork Performance Benchmark:")
    network_speed = psutil.net_io_counters()
    print(f"Bytes Sent: {network_speed.bytes_sent}")
    print(f"Bytes Received: {network_speed.bytes_recv}")

def main():
    cpu_performance()
    memory_performance()
    disk_performance()
    network_performance()

if __name__ == "__main__":
    print("Starting Benchmark...")
    execution_time = timeit.timeit(main, number=1)
    print(f"\nBenchmark completed in {execution_time:.2f} seconds.")
