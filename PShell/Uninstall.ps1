# Function to check if the script is running with admin rights
function Test-IsAdmin {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Function to delete the specified folder
function Delete-Folder {
    param (
        [Parameter(Mandatory = $true)]
        [string]$FolderPath
    )

    if (-Not (Test-Path -Path $FolderPath)) {
        Write-Output "Folder does not exist: $FolderPath"
        return
    }

    try {
        Remove-Item -Path $FolderPath -Recurse -Force
        Write-Output "Folder deleted successfully: $FolderPath"
    } catch {
        Write-Output "Failed to delete folder: $FolderPath"
        Write-Output "Error: $_"
    }
}

# Main script execution
if (-Not (Test-IsAdmin)) {
    Write-Output "Script is not running with administrative privileges. Restarting with elevated rights..."
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# Folder path to delete (Change this to the path you want to delete)
$folderPath = "C:\Program Files (x86)\Common Files\Adobe\AdobeGCClient\AGCInvokerUtility.exe"

Delete-Folder -FolderPath $folderPath
