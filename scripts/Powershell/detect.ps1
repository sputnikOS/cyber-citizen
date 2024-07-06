# Function to check for suspicious network connections
function Check-NetworkConnections {
    Write-Output "Checking for suspicious network connections..."
    Get-NetTCPConnection -State Listen | Format-Table -Property LocalAddress, LocalPort, State, OwningProcess,Name
}

# Function to check for suspicious processes
function Check-SuspiciousProcesses {
    Write-Output "Checking for suspicious processes..."
    Get-Process | Where-Object {
        $_.Name -match 'malware|crypto|mining|botnet|suspicious'
    } | Format-Table -Property Id, ProcessName, CPU, StartTime
}

# Function to check for modified system files
function Check-SystemFiles {
    Write-Output "Checking for modified system files..."
    $files = @(
        "$env:SystemRoot\System32\cmd.exe",
        "$env:SystemRoot\System32\powershell.exe",
        "$env:SystemRoot\System32\notepad.exe",
        "$env:SystemRoot\System32\taskmgr.exe"
    )

    foreach ($file in $files) {
        if (Test-Path $file) {
            Write-Output "File: $file"
            Get-FileHash $file -Algorithm SHA256 | Format-Table -Property Path, Hash
        }
    }
}

# Function to check for unusual startup items
function Check-StartupItems {
    Write-Output "Checking for unusual startup items..."
    Get-CimInstance -ClassName Win32_StartupCommand | Format-Table -Property Name, Command, Location, User
}

# Function to check for known malicious files
# function Check-KnownMaliciousFiles {
#     Write-Output "Checking for known malicious files..."
#     Get-ChildItem -Path C:\ -Recurse -Include 'malware', 'suspicious', 'botnet' -ErrorAction SilentlyContinue | Format-Table -Property FullName, Length, CreationTime
# }

# Function to check for suspicious scheduled tasks
function Check-ScheduledTasks {
    Write-Output "Checking for suspicious scheduled tasks..."
    Get-ScheduledTask | Where-Object {
        $_.TaskName -match 'malware|crypto|mining|botnet|suspicious'
    } | Format-Table -Property TaskName, TaskPath, State, Actions
}

# Run all checks
Check-NetworkConnections
Check-SuspiciousProcesses
Check-SystemFiles
Check-StartupItems
# Check-KnownMaliciousFiles
Check-ScheduledTasks

Write-Output "Detection complete."
