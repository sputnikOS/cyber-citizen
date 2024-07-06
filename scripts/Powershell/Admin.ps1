# Prompt for the username to grant admin access
$username = Read-Host "Enter the username of the user you want to grant admin access"

# Check if the user exists
if (Get-LocalUser -Name $username -ErrorAction SilentlyContinue) {
    # Add the user to the local administrators group
    Add-LocalGroupMember -Group "Administrators" -Member $username
    Write-Host "User '$username' has been granted full admin control."
} else {
    Write-Host "User '$username' does not exist on this machine."
}
