# Publishes the site: regenerates the pages, commits everything and pushes to GitHub,
# where the "Deploy to GitHub Pages" workflow puts www_root online (about 30 s).
$ErrorActionPreference = 'Stop'
$git = 'D:\app-portable\git\cmd\git.exe'
Set-Location (Split-Path $PSScriptRoot)

python build.py
if ($LASTEXITCODE) { exit $LASTEXITCODE }

& $git add -A
# Commit message: the article directories (or other files) that changed.
$changed = & $git diff --cached --name-only |
    ForEach-Object { if ($_ -match '^www_root/([^/]+)/') { $Matches[1] } else { $_ } } |
    Sort-Object -Unique
if ($changed) {
    & $git commit -q -m ("Update " + ($changed -join ', '))
    if ($LASTEXITCODE) { exit $LASTEXITCODE }
    Write-Host "committed: $($changed -join ', ')"
} else {
    Write-Host 'nothing to commit'
}

& $git push -q
if ($LASTEXITCODE) { exit $LASTEXITCODE }
Write-Host 'pushed - live in about 30 s: https://github.com/radomir-polivka/www/actions'
