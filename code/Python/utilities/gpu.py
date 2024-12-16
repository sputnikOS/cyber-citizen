import psutil
import time
try:
    import GPUtil
    import pycuda.driver as cuda
    import pycuda.autoinit
    import numpy as np
    import time
except ImportError as e:
    GPUtil = None
    cuda = None
    numpy_error = str(e)

def get_cpu_usage():
    """Get the current CPU usage percentage."""
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    """Get the current memory usage."""
    memory = psutil.virtual_memory()
    return memory.used / (1024 ** 3), memory.total / (1024 ** 3), memory.percent

def get_disk_usage():
    """Get the current disk usage."""
    disk = psutil.disk_usage('/')
    return disk.used / (1024 ** 3), disk.total / (1024 ** 3), disk.percent

def get_gpu_usage():
    """Get GPU usage information if GPUtil is available."""
    if GPUtil is None:
        return "GPUtil module not installed."
    gpus = GPUtil.getGPUs()
    if not gpus:
        return "No GPU detected."
    gpu_info = []
    for gpu in gpus:
        gpu_info.append(f"GPU {gpu.id} ({gpu.name}): {gpu.load * 100:.2f}% usage, {gpu.memoryUsed:.2f} MB / {gpu.memoryTotal:.2f} MB")
    return "\n".join(gpu_info)

def benchmark_gpu():
    """Run a simple GPU benchmark if PyCUDA is available."""
    if cuda is None:
        return "PyCUDA is not installed: " + numpy_error

    start = time.time()

    # Allocate random array
    size = 1024 * 1024 * 100  # 100 MB
    host_array = np.random.random(size).astype(np.float32)
    device_array = cuda.mem_alloc(host_array.nbytes)

    # Copy to GPU
    cuda.memcpy_htod(device_array, host_array)

    # Simple GPU operation (copying back and forth)
    result_array = np.empty_like(host_array)
    cuda.memcpy_dtoh(result_array, device_array)

    end = time.time()
    elapsed_time = end - start

    return f"GPU benchmark completed in {elapsed_time:.4f} seconds."

def display_performance_data():
    """Display system performance data in a clear format."""
    print("System Performance Data")
    print("-" * 30)

    while True:
        # CPU Usage
        cpu_usage = get_cpu_usage()
        print(f"\rCPU Usage: {cpu_usage:.2f}%", end="")

        # Memory Usage
        memory_used, memory_total, memory_percent = get_memory_usage()
        print(f"\nMemory Usage: {memory_used:.2f} GB / {memory_total:.2f} GB ({memory_percent:.2f}%)", end="")

        # Disk Usage
        disk_used, disk_total, disk_percent = get_disk_usage()
        print(f"\nDisk Usage: {disk_used:.2f} GB / {disk_total:.2f} GB ({disk_percent:.2f}%)", end="")

        # GPU Usage
        gpu_usage = get_gpu_usage()
        print(f"\nGPU Usage:\n{gpu_usage}", end="")

        # GPU Benchmark
        gpu_benchmark = benchmark_gpu()
        print(f"\nGPU Benchmark:\n{gpu_benchmark}", end="")

        print("\nPress Ctrl+C to stop.", end="")

        # Refresh every 10 seconds
        time.sleep(10)

if __name__ == "__main__":
    try:
        display_performance_data()
    except KeyboardInterrupt:
        print("\nPerformance monitoring stopped.")
