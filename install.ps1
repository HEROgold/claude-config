# Link this repo's rules, skills, and hooks into ~/.claude using directory junctions.
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

Link-Dir (Join-Path $claude 'rules') (Join-Path $repo 'rules')
Link-Dir (Join-Path $claude 'hooks') (Join-Path $repo 'hooks')

# Skills are linked one by one because ~/.claude/skills also holds folders Claude Code manages itself (e.g. `synced`).
Get-ChildItem (Join-Path $repo 'skills') -Directory | ForEach-Object {
    Link-Dir (Join-Path $claude "skills\$($_.Name)") $_.FullName
}
