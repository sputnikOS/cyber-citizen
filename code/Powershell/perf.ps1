# Run as Administrator

# Clear temporary files
Write-Host "Cleaning temporary files..."
Remove-Item -Path "$env:Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
Clear-DnsClientCache
Write-Host "Temporary files cleared."

# Disable startup programs
Write-Host "Disabling unnecessary startup programs..."
$startupItems = Get-CimInstance -Class Win32_StartupCommand
foreach ($item in $startupItems) {
    if ($item.Caption -notlike "*Security*" -and $item.Caption -notlike "*Antivirus*") {
        try {
            Disable-CimInstance -CimInstance $item
            Write-Host "$($item.Caption) disabled."
        } catch {
            Write-Host "Failed to disable $($item.Caption)"
        }
    }
}

# Disable visual effects for best performance
Write-Host "Disabling visual effects for best performance..."
$performanceSettings = Get-WmiObject -Class Win32_OperatingSystem
$performanceSettings.AutomaticManagedPagefile = $false
$performanceSettings.Put()

# Set power plan to High Performance
Write-Host "Setting power plan to High Performance..."
powercfg -setactive SCHEME_MIN

# Disable unnecessary services
Write-Host "Disabling unnecessary services..."
$services = Get-Service
$servicesToDisable = @("Fax", "PrintNotify", "Spooler", "WSearch")  # Add other services if necessary
foreach ($service in $services) {
    if ($servicesToDisable -contains $service.Name) {
        Set-Service -Name $service.Name -StartupType Disabled
        Write-Host "$($service.Name) service disabled."
    }
}

# Clean up Windows Update files
Write-Host "Cleaning up Windows Update files..."
$updateFolder = "C:\Windows\SoftwareDistribution\Download"
Remove-Item -Path "$updateFolder\*" -Recurse -Force -ErrorAction SilentlyContinue

# Perform Disk Cleanup
Write-Host "Performing Disk Cleanup..."
$cleanup = New-Object -ComObject "Microsoft.CleanUp.CleanUp"
$cleanup.CleanUpDisk()

# Optimize drives
Write-Host "Optimizing drives..."
Optimize-Volume -DriveLetter C -ReTrim -Verbose

Write-Host "Performance optimization complete."
