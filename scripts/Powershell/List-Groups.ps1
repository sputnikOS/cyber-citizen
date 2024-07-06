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

# Function to list all local groups
function List-AllGroups {
    Write-Output "Listing all local groups on the system..."

    try {
        $groups = Get-LocalGroup
        foreach ($group in $groups) {
            Write-Output "Group Name: $($group.Name)"
        }
    } catch {
        Write-Error "Failed to retrieve local groups. Error: $_"
    }
}

# Run the function to list all groups
List-AllGroups
