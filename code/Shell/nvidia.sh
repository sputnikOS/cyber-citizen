#!/bin/bash

# Interval between updates (in seconds)
INTERVAL=10

# Check if nvidia-smi is available
if ! command -v nvidia-smi > /dev/null; then
    echo "Error: nvidia-smi is not installed or not in PATH."
    exit 1
fi

clear
echo "Starting real-time NVIDIA GPU benchmark. Press Ctrl+C to stop."
echo "Refreshing every $INTERVAL second(s)..."

while true; do
    # Clear the screen
    clear

    # Display current timestamp
    echo "NVIDIA GPU Benchmark - $(date)"
    echo "----------------------------------------"

    # Run nvidia-smi and format the output
    nvidia-smi --query-gpu=index,name,utilization.gpu,utilization.memory,memory.total,memory.used,memory.free --format=csv,nounits |
    awk -F, '
    NR == 1 { 
        printf "%-6s %-30s %-15s %-15s %-10s %-10s %-10s\n", "Index", "GPU Name", "GPU Util (%)", "Memory Util (%)", "Total Mem (MB)", "Used Mem (MB)", "Free Mem (MB)"
        printf "----------------------------------------------------------------------------------------\n"
    }
    NR > 1 { 
        printf "%-6s %-30s %-15s %-15s %-10s %-10s %-10s\n", $1, $2, $3"%", $4"%", $5, $6, $7
    }'

    # Wait for the specified interval
    sleep $INTERVAL
done
