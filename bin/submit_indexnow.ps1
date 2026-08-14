Param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [String[]]$Args
)
$script = Join-Path $PSScriptRoot "..\submit_indexnow.py"
if (-not (Test-Path $script)) { Write-Error "Entry script not found: $script"; exit 2 }
& python $script @Args
exit $LASTEXITCODE
