param([Parameter(Mandatory)][string]$File)

$root = 'D:\project\www\www_root'
$full = (Resolve-Path -LiteralPath $File).Path
if (-not $full.StartsWith($root + '\', [StringComparison]::OrdinalIgnoreCase)) {
    Write-Error "Not inside $root - nothing uploaded: $full"
    exit 1
}
# The remote is case-sensitive, so take every path segment's real casing from disk
# (Resolve-Path and VS Code may pass the casing the folder had earlier).
$real = $root
foreach ($seg in $full.Substring($root.Length + 1).Split('\')) {
    $real = (Get-ChildItem -LiteralPath $real -Force | Where-Object Name -EQ $seg | Select-Object -First 1).FullName
}
$full = $real
$remote = $full.Substring($root.Length).Replace('\', '/')

# The saved WinSCP site has a stale local directory, hence 'batch continue' around 'open'.
& 'D:\app-portable\winscp\WinSCP.com' /command `
    'option batch continue' `
    'open radekpolivka.cz' `
    'option batch abort' `
    "put `"$full`" `"$remote`"" `
    'exit'
exit $LASTEXITCODE
