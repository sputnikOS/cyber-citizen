# Define the username to be added to the Administrators group
$UserName = "samson"

# Add the user to the Administrators group
Add-LocalGroupMember -Group "Administrators" -Member $UserName

# Confirm the user has been added
$UserAdded = Get-LocalGroupMember -Group "Administrators" | Where-Object { $_.Name -eq $UserName }

if ($UserAdded) {
    Write-Host "User $UserName has been added to the Administrators group."
} else {
    Write-Host "Failed to add user $UserName to the Administrators group."
}
