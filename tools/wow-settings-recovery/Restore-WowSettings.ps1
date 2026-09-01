<#
.SYNOPSIS
    Recover World of Warcraft interface settings, addon config and keybindings
    after an accidental "reset to default".

.DESCRIPTION
    Report-only by default. Nothing on disk changes until you pass -Apply, and
    even then the entire WTF folder is copied to a timestamped backup first.

    Recovery sources, in the order the script tries them:

      1. SavedVariables .bak files  - addon settings (ElvUI, Bartender, WeakAuras,
         Details, ...). WoW renames the old .lua to .lua.bak on every logout, so
         the .bak is the previous session. Recoverable only if you have logged
         out FEWER THAN TWO times since the reset.
      2. An untouched character folder - keybindings, Edit Mode layout and macros
         are stored per character. A character you have not logged into since the
         reset still has good copies you can clone across.
      3. Volume Shadow Copies (Previous Versions) - a whole-folder snapshot from
         before the reset. Needs an elevated shell.

.PARAMETER WowPath
    Root of the WoW install, e.g. "C:\Program Files (x86)\World of Warcraft".
    Auto-detected from the registry and common locations if omitted.

.PARAMETER Flavor
    _retail_ (default), _classic_, _classic_era_, _ptr_, _xptr_, _beta_.

.PARAMETER ResetMinutesAgo
    How long ago the reset happened. Used to classify each file as PRE-RESET
    (good, worth restoring) or POST-RESET (already clobbered). Default 60.

.PARAMETER ResetTime
    Exact timestamp of the reset. Overrides -ResetMinutesAgo.

.PARAMETER Apply
    Perform the selected restore actions. Without this the script only reports.

.PARAMETER RestoreSavedVariables
    Swap eligible .lua.bak files back into place.

.PARAMETER OnlyAddon
    Limit -RestoreSavedVariables to these addons, e.g. ElvUI,WeakAuras.

.PARAMETER FromCharacter
    Source character for a UI clone, as "Realm\Character".

.PARAMETER ToCharacter
    Destination character for a UI clone, as "Realm\Character".
    Use "*" to push the source character's UI to every other character.

.PARAMETER DisableCloudSync
    Set synchronizeSettings/Config/Bindings/Macros to 0 in Config.wtf so that
    Blizzard's account-side copy does not overwrite the files you just restored
    on your next login. Strongly recommended alongside a keybinding restore.

.PARAMETER ListShadowCopies
    List Volume Shadow Copies that contain the WTF folder. Requires elevation.

.PARAMETER BackupRoot
    Where backups are written. Default: Desktop\WoW-WTF-Backups.

.EXAMPLE
    .\Restore-WowSettings.ps1 -ResetMinutesAgo 45
    Report only. Start here - it tells you what is actually recoverable.

.EXAMPLE
    .\Restore-WowSettings.ps1 -ResetMinutesAgo 45 -RestoreSavedVariables -Apply

.EXAMPLE
    .\Restore-WowSettings.ps1 -FromCharacter "Ravencrest\Altchar" -ToCharacter "Ravencrest\Main" -DisableCloudSync -Apply
#>
[CmdletBinding()]
param(
    [string]   $WowPath,
    [ValidateSet('_retail_','_classic_','_classic_era_','_ptr_','_xptr_','_beta_')]
    [string]   $Flavor = '_retail_',
    [int]      $ResetMinutesAgo = 60,
    [datetime] $ResetTime,
    [switch]   $Apply,
    [switch]   $RestoreSavedVariables,
    [string[]] $OnlyAddon,
    [string]   $FromCharacter,
    [string]   $ToCharacter,
    [switch]   $DisableCloudSync,
    [switch]   $ListShadowCopies,
    [string]   $BackupRoot
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

# Desktop can come back empty when the shell folder is redirected (OneDrive
# Known Folder Move, some domain profiles), so fall back rather than crash.
if (-not $BackupRoot) {
    $base = @([Environment]::GetFolderPath('Desktop'),
              [Environment]::GetFolderPath('UserProfile'),
              $env:USERPROFILE,
              (Get-Location).Path) |
            Where-Object { $_ -and (Test-Path $_) } |
            Select-Object -First 1
    $BackupRoot = Join-Path $base 'WoW-WTF-Backups'
}

# --------------------------------------------------------------------------
# Output helpers
# --------------------------------------------------------------------------
function Write-Head ($t) { Write-Host ''; Write-Host "== $t" -ForegroundColor Cyan }
function Write-Ok   ($t) { Write-Host "   [ ok ] $t"   -ForegroundColor Green }
function Write-Warn ($t) { Write-Host "   [warn] $t"   -ForegroundColor Yellow }
function Write-Bad  ($t) { Write-Host "   [ !! ] $t"   -ForegroundColor Red }
function Write-Info ($t) { Write-Host "   $t" }
function Write-Act  ($t) {
    if ($Apply) { Write-Host "   [ DO ] $t" -ForegroundColor Magenta }
    else        { Write-Host "   [plan] $t" -ForegroundColor DarkGray }
}

# The moment the settings were lost. Anything written before it is good.
if (-not $PSBoundParameters.ContainsKey('ResetTime')) {
    $ResetTime = (Get-Date).AddMinutes(-$ResetMinutesAgo)
}

Write-Host ''
Write-Host ' WoW settings recovery' -ForegroundColor White
Write-Host " Reset assumed at : $($ResetTime.ToString('yyyy-MM-dd HH:mm:ss'))"
Write-Host " Mode             : $(if ($Apply) {'APPLY - files will be written'} else {'REPORT ONLY - nothing will change'})" `
    -ForegroundColor $(if ($Apply) { 'Magenta' } else { 'DarkGray' })

# --------------------------------------------------------------------------
# 1. Preflight - the game must be closed
# --------------------------------------------------------------------------
Write-Head 'Preflight'

$wowProcs = @(Get-Process -ErrorAction SilentlyContinue |
              Where-Object { $_.ProcessName -match '^Wow(Classic)?(T|B)?$' })
if ($wowProcs.Count -gt 0) {
    Write-Bad "World of Warcraft is running (PID $($wowProcs.Id -join ', '))."
    Write-Info 'WoW rewrites every settings file on logout and exit, so it would'
    Write-Info 'undo the restore - and each extra logout destroys another .bak.'
    Write-Info 'Close the game completely, then run this again.'
    exit 1
}
Write-Ok 'World of Warcraft is not running.'

# --------------------------------------------------------------------------
# 2. Locate the install
# --------------------------------------------------------------------------
function Find-WowInstall {
    $candidates = New-Object System.Collections.Generic.List[string]

    foreach ($key in @(
        'HKLM:\SOFTWARE\WOW6432Node\Blizzard Entertainment\World of Warcraft',
        'HKLM:\SOFTWARE\Blizzard Entertainment\World of Warcraft'
    )) {
        try {
            $p = (Get-ItemProperty -Path $key -ErrorAction Stop).InstallPath
            if ($p) { $candidates.Add(($p -replace '[\\/]_[a-z]+_[\\/]?$','')) }
        } catch { }
    }

    foreach ($root in @($env:ProgramFiles, ${env:ProgramFiles(x86)}, 'C:', 'D:', 'E:')) {
        if ($root) { $candidates.Add((Join-Path $root 'World of Warcraft')) }
    }

    foreach ($c in $candidates) {
        if ($c -and (Test-Path (Join-Path $c $Flavor))) { return (Resolve-Path $c).Path }
    }

    # Last resort: a shallow sweep of every fixed drive.
    Write-Info 'Not in the usual places - scanning fixed drives (a few seconds)...'
    foreach ($drive in (Get-PSDrive -PSProvider FileSystem |
                        Where-Object { $_.Free -ne $null })) {
        $hit = Get-ChildItem -Path "$($drive.Root)" -Filter 'World of Warcraft' `
                   -Directory -Depth 3 -ErrorAction SilentlyContinue |
               Where-Object { Test-Path (Join-Path $_.FullName $Flavor) } |
               Select-Object -First 1
        if ($hit) { return $hit.FullName }
    }
    return $null
}

if (-not $WowPath) { $WowPath = Find-WowInstall }
if (-not $WowPath -or -not (Test-Path $WowPath)) {
    Write-Bad 'Could not find the World of Warcraft folder.'
    Write-Info 'Pass it explicitly, e.g.:'
    Write-Info '  -WowPath "D:\Games\World of Warcraft"'
    exit 1
}

$wtf = Join-Path $WowPath "$Flavor\WTF"
if (-not (Test-Path $wtf)) {
    Write-Bad "No WTF folder at: $wtf"
    Write-Info "Check -Flavor (currently $Flavor)."
    exit 1
}
Write-Ok "WTF folder: $wtf"

$accounts = @(Get-ChildItem (Join-Path $wtf 'Account') -Directory -ErrorAction SilentlyContinue)
if ($accounts.Count -eq 0) {
    Write-Bad 'No account folders under WTF\Account - nothing to recover from here.'
    Write-Info 'Skip to the Volume Shadow Copy section (-ListShadowCopies).'
}
foreach ($a in $accounts) { Write-Ok "Account: $($a.Name)" }

# --------------------------------------------------------------------------
# 3. Back up WTF before touching anything
# --------------------------------------------------------------------------
$script:BackupPath = $null
function Ensure-Backup {
    if ($script:BackupPath) { return $script:BackupPath }
    Write-Head 'Backup'
    $stamp = Get-Date -Format 'yyyy-MM-dd_HHmmss'
    $dest  = Join-Path $BackupRoot "WTF_$Flavor`_$stamp"
    if (-not $Apply) {
        Write-Act "copy `"$wtf`" -> `"$dest`""
        $script:BackupPath = $dest
        return $dest
    }
    New-Item -ItemType Directory -Path $dest -Force | Out-Null
    Copy-Item -Path (Join-Path $wtf '*') -Destination $dest -Recurse -Force
    $size = '{0:N1} MB' -f ((Get-ChildItem $dest -Recurse -File |
                             Measure-Object Length -Sum).Sum / 1MB)
    Write-Ok "Backed up $size to $dest"
    Write-Info 'To undo everything this script does, copy that folder back over WTF.'
    $script:BackupPath = $dest
    return $dest
}

# --------------------------------------------------------------------------
# 4. Inventory and report
# --------------------------------------------------------------------------
function Get-Age ($file) {
    $mins = [int]((Get-Date) - $file.LastWriteTime).TotalMinutes
    if ($mins -lt 90)   { return "$mins min ago" }
    if ($mins -lt 2880) { return "{0:N1} hours ago" -f ($mins / 60) }
    return "{0:N1} days ago" -f ($mins / 1440)
}
function Is-PreReset ($file) { return $file.LastWriteTime -lt $ResetTime }

Write-Head 'Core settings files'
$coreNames = 'Config.wtf','config-cache.wtf','bindings-cache.wtf','layout-local.txt',
             'macros-cache.txt','AddOns.txt','ChatCache.txt'
$core = @(Get-ChildItem $wtf -Recurse -File -ErrorAction SilentlyContinue |
          Where-Object { $coreNames -contains $_.Name })

if ($core.Count -eq 0) {
    Write-Warn 'No core settings files found.'
} else {
    foreach ($f in ($core | Sort-Object LastWriteTime)) {
        $rel  = $f.FullName.Substring($wtf.Length).TrimStart('\')
        $tag  = if (Is-PreReset $f) { 'PRE-RESET  ' } else { 'post-reset ' }
        $col  = if (Is-PreReset $f) { 'Green' } else { 'DarkGray' }
        Write-Host ("   {0} {1,-52} {2}" -f $tag, $rel, (Get-Age $f)) -ForegroundColor $col
    }
    Write-Host ''
    Write-Info 'PRE-RESET (green) files were never touched by the reset. Those are'
    Write-Info 'your recovery source - see the character-clone section below.'
}

Write-Head 'Addon settings (SavedVariables)'
$svPairs = @()
foreach ($svDir in (Get-ChildItem $wtf -Recurse -Directory -Filter 'SavedVariables' `
                    -ErrorAction SilentlyContinue)) {
    foreach ($bak in (Get-ChildItem $svDir.FullName -Filter '*.lua.bak' -File `
                      -ErrorAction SilentlyContinue)) {
        $live = Join-Path $svDir.FullName ($bak.BaseName)   # strips .bak -> Name.lua
        $liveItem = $null
        if (Test-Path $live) { $liveItem = Get-Item $live }
        $svPairs += [pscustomobject]@{
            Addon    = [IO.Path]::GetFileNameWithoutExtension($bak.BaseName)
            Scope    = $svDir.FullName.Substring($wtf.Length).TrimStart('\')
            Bak      = $bak
            LivePath = $live
            Live     = $liveItem
        }
    }
}

if ($svPairs.Count -eq 0) {
    Write-Warn 'No .lua.bak files found - no addon settings to roll back.'
} else {
    $eligible = @()
    foreach ($p in ($svPairs | Sort-Object Addon)) {
        $bakGood  = Is-PreReset $p.Bak
        $liveBad  = ($p.Live -eq $null) -or (-not (Is-PreReset $p.Live))
        if ($bakGood -and $liveBad) {
            $eligible += $p
            Write-Host ("   RECOVERABLE  {0,-24} .bak {1}" -f $p.Addon, (Get-Age $p.Bak)) `
                -ForegroundColor Green
        } elseif (-not $bakGood) {
            Write-Host ("   too new      {0,-24} .bak {1} - already overwritten" `
                -f $p.Addon, (Get-Age $p.Bak)) -ForegroundColor Red
        } else {
            Write-Host ("   already ok   {0,-24} live file predates the reset" `
                -f $p.Addon) -ForegroundColor DarkGray
        }
    }
    Write-Host ''
    Write-Info "$($eligible.Count) of $($svPairs.Count) addon files can be rolled back."
    if ($eligible.Count -gt 0 -and -not $RestoreSavedVariables) {
        Write-Info 'Add -RestoreSavedVariables to act on these.'
    }
}

Write-Head 'Characters (keybindings, Edit Mode layout, macros)'
$charFolders = @()
foreach ($acct in $accounts) {
    foreach ($realm in (Get-ChildItem $acct.FullName -Directory -ErrorAction SilentlyContinue |
                        Where-Object { $_.Name -ne 'SavedVariables' })) {
        foreach ($char in (Get-ChildItem $realm.FullName -Directory -ErrorAction SilentlyContinue)) {
            $bind   = Join-Path $char.FullName 'bindings-cache.wtf'
            $layout = Join-Path $char.FullName 'layout-local.txt'
            $newest = @(Get-ChildItem $char.FullName -File -ErrorAction SilentlyContinue |
                        Sort-Object LastWriteTime -Descending | Select-Object -First 1)
            $lastWrite = [datetime]::MinValue
            $touched   = $false
            if ($newest.Count -gt 0) {
                $lastWrite = $newest[0].LastWriteTime
                $touched   = -not (Is-PreReset $newest[0])
            }
            $charFolders += [pscustomobject]@{
                Key        = "$($realm.Name)\$($char.Name)"
                Account    = $acct.Name
                Path       = $char.FullName
                HasBind    = Test-Path $bind
                HasLayout  = Test-Path $layout
                Touched    = $touched
                LastWrite  = $lastWrite
            }
        }
    }
}

$intact = @($charFolders | Where-Object { -not $_.Touched -and $_.HasBind })
if ($charFolders.Count -eq 0) {
    Write-Warn 'No character folders found.'
} else {
    foreach ($c in ($charFolders | Sort-Object LastWrite)) {
        $tag = if ($c.Touched) { 'touched by reset' } else { 'UNTOUCHED       ' }
        $col = if ($c.Touched) { 'Red' } else { 'Green' }
        $has = @(); if ($c.HasBind) { $has += 'keybinds' }; if ($c.HasLayout) { $has += 'editmode' }
        Write-Host ("   {0} {1,-34} [{2}] {3}" -f `
            $tag, $c.Key, ($has -join ', '), $c.LastWrite.ToString('MM-dd HH:mm')) -ForegroundColor $col
    }
    Write-Host ''
    if ($intact.Count -gt 0) {
        Write-Ok "$($intact.Count) character(s) still hold pre-reset keybindings."
        Write-Info 'Clone one of them onto the character you lost, e.g.:'
        Write-Info "  -FromCharacter `"$($intact[0].Key)`" -ToCharacter `"*`" -DisableCloudSync -Apply"
    } else {
        Write-Warn 'Every character folder was written after the reset.'
        Write-Info 'Keybindings are only recoverable from a shadow copy or cloud'
        Write-Info 'version history now - see the section below.'
    }
}

# --------------------------------------------------------------------------
# 5. Action: roll back addon SavedVariables
# --------------------------------------------------------------------------
if ($RestoreSavedVariables) {
    Write-Head 'Restoring addon settings from .bak'
    $todo = @($svPairs | Where-Object {
        (Is-PreReset $_.Bak) -and (($_.Live -eq $null) -or (-not (Is-PreReset $_.Live)))
    })
    if ($OnlyAddon) {
        $todo = @($todo | Where-Object { $OnlyAddon -contains $_.Addon })
    }
    if ($todo.Count -eq 0) {
        Write-Warn 'Nothing eligible to restore.'
    } else {
        Ensure-Backup | Out-Null
        foreach ($p in $todo) {
            Write-Act "$($p.Scope)\$($p.Addon).lua  <-  .bak from $(Get-Age $p.Bak)"
            if ($Apply) {
                if (Test-Path $p.LivePath) {
                    Move-Item $p.LivePath "$($p.LivePath).reset-state" -Force
                }
                Copy-Item $p.Bak.FullName $p.LivePath -Force
            }
        }
        Write-Host ''
        Write-Info "$($todo.Count) addon file(s) $(if ($Apply) {'restored'} else {'would be restored'})."
        if ($Apply) { Write-Info 'The reset versions are kept alongside as *.lua.reset-state' }
    }
}

# --------------------------------------------------------------------------
# 6. Action: clone a character's UI onto another character
# --------------------------------------------------------------------------
if ($FromCharacter) {
    Write-Head 'Cloning character UI'
    $src = @($charFolders | Where-Object { $_.Key -eq $FromCharacter })
    if ($src.Count -eq 0) {
        Write-Bad "Source character not found: $FromCharacter"
        Write-Info 'Use one of the "Realm\Character" keys listed above.'
    } elseif (-not $ToCharacter) {
        Write-Bad 'Specify -ToCharacter "Realm\Character", or "*" for all others.'
    } else {
        $targets = if ($ToCharacter -eq '*') {
            @($charFolders | Where-Object { $_.Key -ne $FromCharacter })
        } else {
            @($charFolders | Where-Object { $_.Key -eq $ToCharacter })
        }
        if ($targets.Count -eq 0) {
            Write-Bad "Destination character not found: $ToCharacter"
        } else {
            Ensure-Backup | Out-Null
            $files = 'bindings-cache.wtf','layout-local.txt','macros-cache.txt','config-cache.wtf'
            foreach ($t in $targets) {
                foreach ($name in $files) {
                    $s = Join-Path $src[0].Path $name
                    if (-not (Test-Path $s)) { continue }
                    $d = Join-Path $t.Path $name
                    Write-Act "$($t.Key)\$name  <-  $($src[0].Key)\$name"
                    if ($Apply) {
                        if (Test-Path $d) { Move-Item $d "$d.reset-state" -Force }
                        Copy-Item $s $d -Force
                    }
                }
            }
            Write-Host ''
            Write-Info "$($targets.Count) character(s) targeted."
            if (-not $DisableCloudSync) {
                Write-Warn 'Without -DisableCloudSync, Blizzard''s account-side copy can'
                Write-Warn 'overwrite these files the moment you log in. Add that switch.'
            }
        }
    }
}

# --------------------------------------------------------------------------
# 7. Action: stop Blizzard's cloud copy from overwriting the restore
# --------------------------------------------------------------------------
if ($DisableCloudSync) {
    Write-Head 'Disabling account-side settings sync'
    Write-Info 'Retail WoW mirrors settings, keybindings and macros to Blizzard''s'
    Write-Info 'servers. On your next login the server copy - which is the reset'
    Write-Info 'one - wins unless sync is off. These CVars turn that off so the'
    Write-Info 'client uses your restored local files and re-uploads them.'
    Write-Host ''

    $cvars = 'synchronizeSettings','synchronizeConfig','synchronizeBindings','synchronizeMacros'
    $cfg   = Join-Path $wtf 'Config.wtf'
    if (-not (Test-Path $cfg)) {
        Write-Bad "Config.wtf not found at $cfg"
    } else {
        Ensure-Backup | Out-Null
        $lines = @(Get-Content $cfg)
        foreach ($cv in $cvars) {
            $rx = '^\s*SET\s+' + [regex]::Escape($cv) + '\s'
            if ($lines -match $rx) {
                $lines = $lines | ForEach-Object {
                    if ($_ -match $rx) { "SET $cv `"0`"" } else { $_ }
                }
                Write-Act "Config.wtf: SET $cv `"0`"  (was set, now forced off)"
            } else {
                $lines += "SET $cv `"0`""
                Write-Act "Config.wtf: SET $cv `"0`"  (added)"
            }
        }
        if ($Apply) {
            $utf8 = New-Object System.Text.UTF8Encoding($false)
            [IO.File]::WriteAllLines($cfg, [string[]]$lines, $utf8)
            Write-Ok 'Config.wtf updated.'
        }
        Write-Host ''
        Write-Info 'Turn sync back on in-game once your UI looks right:'
        Write-Info '  Options > System > Advanced > "Sync settings to Battle.net"'
    }
}

# --------------------------------------------------------------------------
# 8. Volume Shadow Copies - the last resort, and the best one
# --------------------------------------------------------------------------
if ($ListShadowCopies) {
    Write-Head 'Volume Shadow Copies (Previous Versions)'
    $elevated = ([Security.Principal.WindowsPrincipal] `
                 [Security.Principal.WindowsIdentity]::GetCurrent()
                ).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    if (-not $elevated) {
        Write-Warn 'Not elevated - shadow copies cannot be enumerated.'
        Write-Info 'Re-run this from an Administrator PowerShell to use this path.'
    } else {
        $vol = (Get-Item $wtf).PSDrive.Root
        $shadows = @(Get-CimInstance Win32_ShadowCopy -ErrorAction SilentlyContinue |
                     Sort-Object InstallDate -Descending)
        if ($shadows.Count -eq 0) {
            Write-Warn "No shadow copies exist on this machine."
            Write-Info 'System Protection / File History was off. Nothing to pull from.'
        } else {
            $rel = $wtf.Substring(3)   # strip "C:\"
            $useful = 0
            foreach ($s in $shadows) {
                $probe = "$($s.DeviceObject)\$rel"
                $when  = $s.InstallDate
                $good  = $when -lt $ResetTime
                $mark  = if ($good) { 'BEFORE reset' } else { 'after reset ' }
                $col   = if ($good) { 'Green' } else { 'DarkGray' }
                Write-Host ("   {0}  {1}  {2}" -f $mark, $when, $s.DeviceObject) -ForegroundColor $col
                if ($good) { $useful++ }
            }
            Write-Host ''
            if ($useful -gt 0) {
                Write-Ok "$useful snapshot(s) predate the reset."
                Write-Info 'A shadow copy path is not browsable directly. Mount one with:'
                Write-Info '  cmd /c mklink /d C:\ShadowWTF "\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopyN\"'
                Write-Info '(replace N with the number from the DeviceObject above, keep the'
                Write-Info ' trailing backslash), then copy from:'
                Write-Info "  C:\ShadowWTF\$rel"
                Write-Info 'Remove the link afterwards with: rmdir C:\ShadowWTF'
                Write-Info ''
                Write-Info 'Simpler equivalent: right-click the WTF folder > Properties >'
                Write-Info 'Previous Versions > Restore to a DIFFERENT location, then copy'
                Write-Info 'the pieces you want across by hand.'
            } else {
                Write-Warn 'Every snapshot is newer than the reset - none of them help.'
            }
        }
    }
}

# --------------------------------------------------------------------------
# 9. Cloud storage version history
# --------------------------------------------------------------------------
Write-Head 'Cloud storage'
$cloudRoots = @($env:OneDrive, $env:OneDriveConsumer, $env:OneDriveCommercial,
                (Join-Path $env:USERPROFILE 'Dropbox'),
                (Join-Path $env:USERPROFILE 'Google Drive')) |
              Where-Object { $_ -and (Test-Path $_) }
$inCloud = @($cloudRoots | Where-Object { $wtf.StartsWith($_, 'OrdinalIgnoreCase') })
if ($inCloud.Count -gt 0) {
    Write-Ok "WTF sits inside a synced folder: $($inCloud[0])"
    Write-Info 'Open that service in a browser and use version history on'
    Write-Info 'Config.wtf, bindings-cache.wtf and the SavedVariables .lua files.'
    Write-Info 'Cloud history often reaches back further than anything on disk.'
} else {
    Write-Info 'WTF is not inside OneDrive, Dropbox or Google Drive - no version'
    Write-Info 'history available from that route.'
}

# --------------------------------------------------------------------------
# 10. Summary
# --------------------------------------------------------------------------
Write-Head 'Next steps'
if (-not $Apply) {
    Write-Host '   This was a REPORT ONLY run - nothing changed.' -ForegroundColor Yellow
    Write-Host ''
    Write-Info 'Re-run with the actions you want plus -Apply, for example:'
    Write-Info "  .\Restore-WowSettings.ps1 -ResetMinutesAgo $ResetMinutesAgo -RestoreSavedVariables -Apply"
    if ($intact.Count -gt 0) {
        Write-Info "  .\Restore-WowSettings.ps1 -FromCharacter `"$($intact[0].Key)`" -ToCharacter `"*`" -DisableCloudSync -Apply"
    }
    Write-Info '  .\Restore-WowSettings.ps1 -ListShadowCopies      (run elevated)'
} else {
    Write-Ok 'Done. Launch WoW and check the result before doing anything else.'
    if ($script:BackupPath) { Write-Info "Rollback copy: $script:BackupPath" }
    Write-Info 'If it looks wrong, close the game IMMEDIATELY - logging out will'
    Write-Info 'overwrite the restored files - and copy the backup back over WTF.'
}
Write-Host ''
