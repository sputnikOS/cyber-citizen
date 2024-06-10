# Define an array of process IDs you want to disable
$processIDsToDisable = @(1234, 5678, 9012) # Add the desired PIDs here

# Function to check if a process is running
function IsProcessRunning($pid) {
    return Get-Process -Id $pid -ErrorAction SilentlyContinue
}

# Trap Ctrl+C to gracefully exit the script
$handler = {
    Write-Host "Exiting..."
    exit
}
$null = [System.Console]::TreatControlCAsInput = $true
$null = [System.Console]::CancelKeyPress.Add($handler)

# Loop to continuously check and disable the processes
while ($true) {
    foreach ($pidToDisable in $processIDsToDisable) {
        if (IsProcessRunning $pidToDisable) {
            Write-Host "Disabling process with PID $pidToDisable..."
            Stop-Process -Id $pidToDisable -Force
        }
    }
    
    # Sleep for a period of time before checking again
    Start-Sleep -Seconds 5
}
