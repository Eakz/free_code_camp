# WoW settings recovery

Recovers World of Warcraft interface settings, addon configuration and
keybindings after an accidental **reset to default**.

## Do this first

**Close WoW and stay logged out.** WoW rewrites every settings file on logout
and exit. Each extra session overwrites another layer of exactly what you are
trying to get back — including the `.bak` files this script restores from.

## Run it

### Option A — one command, from any directory, no install

Put `Restore-WowSettings.ps1` anywhere (Downloads is fine) and run this in
**cmd**, from whatever folder you happen to be in:

```bat
powershell -NoProfile -ExecutionPolicy Bypass -File "%USERPROFILE%\Downloads\Restore-WowSettings.ps1" -ResetMinutesAgo 90
```

Adjust the path if you saved it elsewhere. Lost track of it?

```bat
where /r "%USERPROFILE%" Restore-WowSettings.ps1
```

### Option B — install it as a global `wowfix` command

Run `Install.cmd` once (double-click, or run it from cmd). It copies the
script to `%LOCALAPPDATA%\WowFix` and drops a launcher into
`%LOCALAPPDATA%\Microsoft\WindowsApps`, which is already on your PATH — so no
PATH editing, no admin rights, no registry changes.

Then, from **any** directory in a **new** cmd window:

```bat
wowfix -ResetMinutesAgo 90
```

Every option below works the same way — `wowfix` just forwards them:

```bat
wowfix -ResetMinutesAgo 90 -RestoreSavedVariables -Apply
```

Need an elevated run (for `-ListShadowCopies`, or if WoW is under
`C:\Program Files (x86)`):

```bat
powershell -NoProfile -Command "Start-Process cmd -Verb RunAs -ArgumentList '/k wowfix -ListShadowCopies'"
```

To uninstall: delete `%LOCALAPPDATA%\WowFix` and
`%LOCALAPPDATA%\Microsoft\WindowsApps\wowfix.cmd`.

---

Either way, the default run is **report only** — nothing on disk changes. It finds your install,
timestamps every settings file against the moment of the reset, and tells you
which ones are actually recoverable and how.

Then re-run with the actions it suggests plus `-Apply`. The whole `WTF` folder
is copied to `Desktop\WoW-WTF-Backups\` before anything is written, and each
replaced file is kept alongside as `*.reset-state`.

If WoW lives under `C:\Program Files (x86)`, run PowerShell **as Administrator**
or Windows blocks the writes.

## What is recoverable, and from where

| Lost | Stored in | Recovered by |
|---|---|---|
| Addon settings (ElvUI, Bartender, WeakAuras, Details) | `SavedVariables\*.lua` | `-RestoreSavedVariables` — rolls back to the `.lua.bak` |
| Keybindings | `<Character>\bindings-cache.wtf` | `-FromCharacter` — cloned from a character you have not logged into since |
| Edit Mode layout | `<Character>\layout-local.txt` | same clone |
| Macros | `<Character>\macros-cache.txt` | same clone |
| Graphics / system options | `Config.wtf` | shadow copy or cloud version history only |

### The two things that decide your odds

**`.bak` files are one logout deep.** WoW renames the old `.lua` to `.lua.bak`
and writes a fresh `.lua` on every logout. So the `.bak` holds your *previous*
session. Log out twice after a reset and the good copy is gone. The report
flags each addon as `RECOVERABLE` or `too new` on exactly this basis.

**Keybindings are not purely server-side.** They live locally in
`bindings-cache.wtf`, *per character*, and are mirrored to Blizzard's servers.
Two consequences:

- A character you have not logged into since the reset still has intact
  keybindings and Edit Mode layout. That is a real recovery source — clone it
  across with `-FromCharacter "Realm\Alt" -ToCharacter "*"`.
- On your next login the account-side copy can overwrite what you just
  restored. Pass **`-DisableCloudSync`** alongside any keybinding restore; it
  sets `synchronizeSettings`, `synchronizeConfig`, `synchronizeBindings` and
  `synchronizeMacros` to `0` in `Config.wtf` so the client trusts your local
  files and re-uploads them. Turn sync back on in-game once the UI looks right.

## Worked examples

```powershell
# 1. See what survived. Always start here.
.\Restore-WowSettings.ps1 -ResetMinutesAgo 45

# 2. Roll addon settings back to the pre-reset .bak
.\Restore-WowSettings.ps1 -ResetMinutesAgo 45 -RestoreSavedVariables -Apply

# 2b. ...or only specific addons
.\Restore-WowSettings.ps1 -ResetMinutesAgo 45 -RestoreSavedVariables -OnlyAddon ElvUI,WeakAuras -Apply

# 3. Rebuild keybinds + Edit Mode from an untouched alt, onto every character
.\Restore-WowSettings.ps1 -FromCharacter "Ravencrest\Altchar" -ToCharacter "*" -DisableCloudSync -Apply

# 4. Last resort: a whole-folder snapshot from before the reset (run elevated)
.\Restore-WowSettings.ps1 -ListShadowCopies
```

Add `-WowPath "D:\Games\World of Warcraft"` if auto-detection misses, and
`-Flavor _classic_` for Classic.

## If it made things worse

Close the game immediately — logging out overwrites the restored files — and
copy `Desktop\WoW-WTF-Backups\WTF_<flavor>_<timestamp>\` back over
`_retail_\WTF\`.

## Scope

Read-only until `-Apply`. Touches nothing outside the `WTF` folder, except
writing backups. Makes no network calls. A Blizzard support ticket will not
help with any of this — they do not back up UI settings.
