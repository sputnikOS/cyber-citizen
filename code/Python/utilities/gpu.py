import psutil
import time
import numpy as np
import os

try:
    import pycuda.driver as cuda
    import pycuda.autoinit
except ImportError:
    cuda = None

def cpu_benchmark():
    """Run a simple CPU benchmark."""
    start_time = time.time()
    size = 1000
    matrix_a = np.random.random((size, size))
    matrix_b = np.random.random((size, size))
    np.dot(matrix_a, matrix_b)  # Matrix multiplication
    elapsed_time = time.time() - start_time
    return f"CPU benchmark completed in {elapsed_time:.4f} seconds."

def gpu_benchmark():
    """Run a simple GPU benchmark if PyCUDA is available."""
    if cuda is None:
        return "PyCUDA not installed or GPU unavailable."
    size = 1024 * 1024 * 10  # 10 MB
    host_array = np.random.random(size).astype(np.float32)
    device_array = cuda.mem_alloc(host_array.nbytes)

    start_time = time.time()
    cuda.memcpy_htod(device_array, host_array)  # Copy to GPU
    cuda.memcpy_dtoh(host_array, device_array)  # Copy back to host
    elapsed_time = time.time() - start_time

    return f"GPU benchmark completed in {elapsed_time:.4f} seconds."

def disk_benchmark():
    """Run a simple disk benchmark."""
    file_path = "disk_benchmark_test.tmp"
    data = os.urandom(100 * 1024 * 1024)  # 100 MB of random data
    start_time = time.time()

    with open(file_path, "wb") as f:
        f.write(data)
    write_time = time.time() - start_time

    start_time = time.time()
    with open(file_path, "rb") as f:
        _ = f.read()
    read_time = time.time() - start_time

    os.remove(file_path)
    return f"Disk write: {write_time:.4f} seconds, read: {read_time:.4f} seconds."

def memory_benchmark():
    """Run a simple memory benchmark."""
    size = 1024 * 1024 * 500  # 500 MB
    start_time = time.time()
    _ = np.zeros(size, dtype=np.float32)  # Allocate memory
    elapsed_time = time.time() - start_time
    return f"Memory benchmark completed in {elapsed_time:.4f} seconds."

def display_benchmark_data():
    """Display benchmark data for CPU, GPU, memory, and disk."""
    print("System Benchmark Data")
    print("-" * 30)

    # CPU Benchmark
    print(cpu_benchmark())

    # GPU Benchmark
    print(gpu_benchmark())

    # Memory Benchmark
    print(memory_benchmark())

    # Disk Benchmark
    print(disk_benchmark())

if __name__ == "__main__":
    try:
        display_benchmark_data()
    except KeyboardInterrupt:
        print("\nBenchmarking stopped.")
