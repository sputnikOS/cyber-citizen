# Check if the script is running as administrator
function Test-IsAdmin {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $currentPrincipal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (Test-IsAdmin)) {
    Write-Warning "You do not have administrator rights to run this script. Please run PowerShell as an administrator."
    exit
}

# Function to uninstall software
function Uninstall-Software {
    param (
        [Parameter(Mandatory=$true)]
        [string]$softwareName
    )

    $software = Get-WmiObject -Class Win32_Product | Where-Object { $_.Name -like "*$softwareName*" }

    if ($null -eq $software) {
        Write-Output "Software not found: $softwareName"
        return
    }

    foreach ($app in $software) {
        Write-Output "Uninstalling $($app.Name)..."
        try {
            $app.InvokeMethod("Uninstall", $null)
            Write-Output "Successfully uninstalled: $($app.Name)"
        } catch {
            Write-Error "Failed to uninstall: $($app.Name). Error: $_"
        }
    }
}

# Example usage: replace 'SoftwareName' with the actual name of the software you want to uninstall
$softwareToUninstall = ""
Uninstall-Software -softwareName $softwareToUninstall
