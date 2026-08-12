# Real-Time GRC SEO Progress Monitor
# Displays live stats and log streams in a loop. Refreshing every 5 seconds.

$logPath = "c:\Users\Charwiz43\.gemini\antigravity\scratch\Affirm\regulatory-archive-2026\search_continuous.log"

while ($true) {
    Clear-Host
    Write-Host "=== GRC & SEO CAMPAIGN REAL-TIME PROGRESS ===" -ForegroundColor Cyan
    Write-Host "Current Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
    Write-Host "=============================================" -ForegroundColor Cyan
    
    # Check if the Python simulator is running
    $proc = Get-CimInstance -Query "SELECT * FROM Win32_Process WHERE Name = 'python.exe' AND CommandLine LIKE '%run_continuous_search.py%'" -ErrorAction SilentlyContinue
    if ($proc) {
        Write-Host "Search Simulator Daemon: RUNNING (PID: $($proc.ProcessId))" -ForegroundColor Green
    } else {
        Write-Host "Search Simulator Daemon: NOT RUNNING" -ForegroundColor Red
    }
    
    if (Test-Path $logPath) {
        $lines = Get-Content -Path $logPath -ErrorAction SilentlyContinue
        
        # Calculate stats
        $totalQueries = 0
        $totalMatches = 0
        foreach ($line in $lines) {
            if ($line -like "*QUERY SUCCESS*") { $totalQueries++ }
            if ($line -like "*MATCH*" -or $line -like "*Target found*") { $totalMatches++ }
        }
        
        Write-Host "Total Simulated Queries Run:  $totalQueries" -ForegroundColor Yellow
        Write-Host "Total Verified Search Matches: $totalMatches" -ForegroundColor Green
        Write-Host "=============================================" -ForegroundColor Cyan
        
        Write-Host "Last 8 Log Entries:" -ForegroundColor Gray
        $last8 = $lines | Select-Object -Last 8
        foreach ($line in $last8) {
            if ($line -like "*MATCH*" -or $line -like "*Target found*") {
                Write-Host "  $line" -ForegroundColor Green
            } elseif ($line -like "*QUERY SUCCESS*") {
                Write-Host "  $line" -ForegroundColor Gray
            } else {
                Write-Host "  $line" -ForegroundColor White
            }
        }
    } else {
        Write-Host "Status: Awaiting creation of search_continuous.log..." -ForegroundColor Yellow
    }
    
    Write-Host "`nPress Ctrl+C to exit. Refreshing in 5 seconds..." -ForegroundColor DarkGray
    Start-Sleep -Seconds 5
}
