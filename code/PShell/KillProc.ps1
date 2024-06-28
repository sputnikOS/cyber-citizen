$processes = Get-Process |  Group-Object -Property ProcessName

foreach($group in $processes) {
    if($group.Count -gt 1) {
        $group.Group | Select-Object -Skip 1 | ForEach-Object {
            try {
                Stop-Process -id $_id _Force
                Write-Output "Terminated process: $($_.ProcessName) with ID $($_id)"
            } catch {
                Write-Output "Failed to terminate process: $($_ProcessName) with ID $($_id)"
            }
        }
    }
}