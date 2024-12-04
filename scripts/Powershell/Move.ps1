# Note: This script requires administrative privileges to run

# Function to modify a specific security policy (Example: User Rights Assignment)
function Set-SecurityPolicy {
    param (
        [string]$Policy,
        [string]$Value
    )
    # Load the secedit.exe tool to modify security policies
    secedit /export /cfg "C:\Windows\Temp\secpol.cfg"
    
    # Read the configuration file
    $content = Get-Content "C:\Windows\Temp\secpol.cfg"
    
    # Modify the specific policy
    $index = $content.IndexOf($Policy)
    if ($index -ne -1) {
        $content[$index + 1] = $Value
    } else {
        $content += "$Policy = $Value"
    }
    
    # Write the changes back to the configuration file
    $content | Set-Content "C:\Windows\Temp\secpol.cfg"
    
    # Apply the modified security policy
    secedit /configure /db secedit.sdb /cfg "C:\Windows\Temp\secpol.cfg" /areas USER_RIGHTS
}

# Example usage: Grant "SeBackupPrivilege" to the "Administrators" group
Set-SecurityPolicy "SeBackupPrivilege" "*S-1-5-32-544"

# Function to move files with elevated permissions
function Move-Files {
    param (
        [string]$SourcePath,
        [string]$DestinationPath
    )
    if (-Not (Test-Path $SourcePath)) {
        Write-Host "Source path does not exist."
        return
    }
    
    if (-Not (Test-Path $DestinationPath)) {
        New-Item -ItemType Directory -Path $DestinationPath
    }
    
    Get-ChildItem -Path $SourcePath -Recurse | ForEach-Object {
        $dest = $_.FullName -replace [regex]::Escape($SourcePath), $DestinationPath
        if ($_.PSIsContainer) {
            New-Item -ItemType Directory -Path $dest -Force
        } else {
            Move-Item -Path $_.FullName -Destination $dest -Force
        }
    }
}

# Example usage: Move all files from "C:\Source" to "D:\Destination"
Move-Files -SourcePath "C:\Users\stephan.sabsowitz\Desktop\career\doc.pdf" -DestinationPath "D:\"
