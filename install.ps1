# Link this repo's rules and skills into ~/.claude using directory junctions.
# Junctions don't need admin rights or Developer Mode. Safe to re-run.
# An existing real folder at a target path is moved to ~/.claude/backups/claude-config-<timestamp>/, never deleted.

$ErrorActionPreference = 'Stop'
$repo = $PSScriptRoot
$claude = Join-Path $HOME '.claude'
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'

function Link-Dir([string]$target, [string]$source) {
    if (Test-Path $target) {
        $item = Get-Item $target -Force
        if ($item.LinkType -eq 'Junction' -and $item.Target -contains $source) {
            Write-Host "ok      $target"
            return
        }
        if ($item.LinkType) {
            Remove-Item $target -Force
        } else {
            # Back up outside ~/.claude/skills, or Claude Code would load the backup as a duplicate skill.
            $backupDir = Join-Path $claude "backups\claude-config-$stamp"
            New-Item -ItemType Directory -Force $backupDir | Out-Null
            $backup = Join-Path $backupDir (Split-Path $target -Leaf)
            Move-Item $target $backup
            Write-Host "backup  $target -> $backup"
        }
    }
    New-Item -ItemType Junction -Path $target -Target $source | Out-Null
    Write-Host "linked  $target -> $source"
}

New-Item -ItemType Directory -Force (Join-Path $claude 'skills') | Out-Null

# ~/.claude/rules is a real folder with one junction per repo, so claude-config and agent-home can both add rules.
# An older install linked the whole folder to this repo's rules; remove that link (the repo's files stay).
$rules = Join-Path $claude 'rules'
if ((Test-Path $rules) -and (Get-Item $rules -Force).LinkType) { Remove-Item $rules -Force }
New-Item -ItemType Directory -Force $rules | Out-Null
Link-Dir (Join-Path $rules 'claude-config') (Join-Path $repo 'rules')
Link-Dir (Join-Path $claude 'agents') (Join-Path $repo 'agents')

# Skills are linked one by one because ~/.claude/skills also holds folders Claude Code manages itself (e.g. `synced`).
Get-ChildItem (Join-Path $repo 'skills') -Directory | ForEach-Object {
    Link-Dir (Join-Path $claude "skills\$($_.Name)") $_.FullName
}
