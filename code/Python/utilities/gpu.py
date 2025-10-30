import time
import GPUtil
import torch

def benchmark_gpu_with_monitoring():
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print(f"Using GPU: {torch.cuda.get_device_name(0)}")
        
        # Set size of matrix
        N = 10000
        A = torch.randn(N, N, device=device)
        B = torch.randn(N, N, device=device)
        
        # Monitor GPU usage before the benchmark
        print("Initial GPU stats:")
        gpus = GPUtil.getGPUs()
        print(gpus) 
        for gpu in gpus:
            print(f"GPU {gpu.id}: {gpu.memoryUsed}MB / {gpu.memoryTotal}MB memory used, {gpu.load * 100}% load")
        
        # Benchmark matrix multiplication and monitor during the operation
        start_time = time.time()
        C = torch.mm(A, B)
        end_time = time.time()
        
        print(f"Time taken for matrix multiplication on GPU: {end_time - start_time:.4f} seconds")
        
        # Monitor GPU usage after the benchmark
        print("GPU stats after benchmark:")
        for gpu in gpus:
            print(f"GPU {gpu.id}: {gpu.memoryUsed}MB / {gpu.memoryTotal}MB memory used, {gpu.load * 100}% load")
    else:
        print("CUDA is not available. Running on CPU.")

benchmark_gpu_with_monitoring()
