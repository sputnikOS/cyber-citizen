# Function to measure CPU performance
function Measure-CPU {
    Write-Output "Measuring CPU performance..."
    $cpuCounter = Get-Counter '\Processor(_Total)\% Processor Time'
    $cpuUsage = $cpuCounter.CounterSamples.CookedValue
    Write-Output "CPU Usage: $cpuUsage%"
}

# Function to measure memory performance
function Measure-Memory {
    Write-Output "Measuring memory performance..."
    $memory = Get-WmiObject -Class Win32_OperatingSystem
    $totalMemory = [math]::round($memory.TotalVisibleMemorySize / 1MB, 2)
    $freeMemory = [math]::round($memory.FreePhysicalMemory / 1MB, 2)
    $usedMemory = [math]::round($totalMemory - $freeMemory, 2)
    $memoryUsage = [math]::round(($usedMemory / $totalMemory) * 100, 2)
    Write-Output "Total Memory: $totalMemory MB"
    Write-Output "Used Memory: $usedMemory MB"
    Write-Output "Free Memory: $freeMemory MB"
    Write-Output "Memory Usage: $memoryUsage%"
}

# Function to measure disk performance
function Measure-Disk {
    Write-Output "Measuring disk performance..."
    $diskCounters = Get-Counter '\PhysicalDisk(_Total)\% Disk Time'
    $diskUsage = $diskCounters.CounterSamples.CookedValue
    Write-Output "Disk Usage: $diskUsage%"
}

# Function to measure network performance
function Measure-Network {
    Write-Output "Measuring network performance..."
    $networkCounters = Get-Counter '\Network Interface(*)\Bytes Total/sec'
    $totalBytes = ($networkCounters.CounterSamples | Measure-Object -Property CookedValue -Sum).Sum
    $totalMB = [math]::round($totalBytes / 1MB, 2)
    Write-Output "Total Network Throughput: $totalMB MB/sec"
}

# Function to run all benchmarks
function Run-Benchmarks {
    Write-Output "Starting system performance benchmarks..."

    Measure-CPU
    Measure-Memory
    Measure-Disk
    Measure-Network
cd 
    Write-Output "Performance benchmarks completed."
}

# Run the benchmarks
Run-Benchmarks
