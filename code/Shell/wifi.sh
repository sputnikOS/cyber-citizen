#!/bin/bash

# Function to benchmark CPU performance
benchmark_cpu() {
    echo "Benchmarking CPU performance..."
    
    # Measure CPU performance using 'sysbench' (make sure sysbench is installed)
    sysbench --test=cpu --cpu-max-prime=20000 run
}

# Function to benchmark memory performance
benchmark_memory() {
    echo "Benchmarking memory performance..."
    
    # Measure memory performance using 'sysbench'
    sysbench --test=memory --memory-block-size=8K --memory-total-size=10G run
}

# Function to benchmark disk I/O performance
benchmark_disk() {
    echo "Benchmarking disk I/O performance..."
    
    # Measure disk I/O using 'dd' command
    echo "Writing 1GB to disk (sequential write test)..."
    dd if=/dev/zero of=/tmp/testfile bs=1M count=1024 oflag=dsync status=progress

    # Measure random read/write performance using 'fio'
    echo "Random read/write test on disk..."
    fio --name=test --ioengine=sync --rw=randwrite --bs=4k --size=1G --numjobs=4 --runtime=30s --time_based
}

# Function to benchmark network performance (ping test to Google DNS)
benchmark_network() {
    echo "Benchmarking network performance..."

    # Measure ping to Google's DNS server (8.8.8.8)
    ping -c 10 8.8.8.8
}

# Main function to run all benchmarks
run_benchmarks() {
    echo "Starting system performance benchmarks..."
    
    # CPU
    benchmark_cpu
    
    # Memory
    benchmark_memory
    
    # Disk
    benchmark_disk
    
    # Network
    benchmark_network

    echo "Benchmarking complete."
}

# Execute the benchmarks
run_benchmarks
