---
title: 'The Developer''s Bunker in KDE Plasma 6: Taming Baloo and KWallet via Plain
  Text'
slug: the-developers-bunker-in-kde-plasma-6-taming-baloo-and-kwallet-via-plain-text
status: published
legacy_url: https://dagorret.com.ar/the-developers-bunker-in-kde-plasma-6-taming-baloo-and-kwallet-via-plain-text/
wordpress_id: 1292
published_at: '2026-06-16T20:01:27'
modified_at: '2026-06-16T20:01:27'
wordpress_category_ids:
- 358
- 21
wordpress_tag_ids:
- 352
categories:
- &id001
  id: 358
  name: English
  slug: english
- id: 21
  name: Sistemas
  slug: sistemas
tags:
- id: 352
  name: Linux
  slug: linux
category: *id001
---

Keywords: Baloo, CachyOS, KDE, KWallet, Plasma, Sysadmin

In systems administration, we do not operate on “it seems to work,” but on technical certainty. This article stems from a recent KDE Plasma 6 update that forced me to chase background processes, run diagnostic commands, and—most importantly—clone the KDE source code to confirm what the machine was actually doing, rather than echoing forum folklore.

The result is not a manifesto against KDE. Quite the opposite: once the code is read, the environment proves to be far more reasonable than mythology suggests. What follows is the recipe to tame Baloo (the indexer) and KWallet (the keyring) under your own rules, without breaking anything, and understanding exactly why each directive does what it does.

---

### 1. Two Philosophies That Coexist Better Than It Seems

The design of Plasma 6 is tailored for the general user: automatic indexing to find files instantly, and a graphical keyring that centralizes credentials. A developer’s workflow is entirely different: manual directory control from the terminal, Git keys managed via `ssh-agent`, and environment secrets stored in variables or local `.env` files. For those who live in the console, the indexer and the graphical keyring do not add value; they get in the way.

Up to this point, the inherited community narrative usually takes a leap that is worth halting: _“KDE doesn’t give you a toggle and forces you to rummage through hidden files.”_ That is false, and it is worth stating because honesty is the only thing that sustains a technical article. Both Baloo and KWallet have their respective on/off checkboxes in System Settings (File Search and KDE Wallet, respectively), and Baloo’s GUI even allows adding folders to exclude.

So, why use plain text? For the same reason we do anything in a bunker: reproducibility and determinism. An `.ini` file is versionable, replicable across machines, scriptable in a provisioning workflow, and auditable at a glance. Clicking a GUI is for the user; configuration files are for the administrator who needs ten machines to look identical without touching ten mouses. It is not that KDE hides the switch; it is that we prefer to operate it with the precision of plain text.

---

### 2. Certainty from the Source Code

Before applying any `chmod -x` or creating symlinks to `/dev/null`—brute-force workarounds that will inevitably break upon the next `pacman -Syu`—it pays to read what the system actually does. The following two findings come directly from the public KDE repositories, master branch, and shut down the paranoia immediately.

#### Baloo Already Protects Your Development Directories

In `src/file/fileexcludefilters.cpp` of the KDE/baloo repository, there are two arrays of constants. One filters file patterns (`s_defaultFileExcludeFilters[]`) and the other filters folder names (`s_defaultFolderExcludeFilters[]`). The second one is the one we care about:

```javascript
const char* const s_defaultFolderExcludeFilters[] = {
    "po",
    // VCS
    "CVS", ".svn", ".git", "_darcs", ".bzr", ".hg",
    // development
    "CMakeFiles", "CMakeTmp", "CMakeTmpQmake",
    ".moc", ".obj", ".pch", ".uic",
    ".npm", ".yarn", ".yarn-cache",
    "__pycache__", "node_modules", "node_packages",
    "nbproject", ".terraform", ".venv", "venv",
    // misc
    "core-dumps", "lost+found",
    nullptr
};
```

At the file level, the other array additionally excludes items such as `*.pyc`, `*.pyo`, `*.o`, `*.class`, `*.so`, `*.a`, and even `*.tfstate*`. Both lists are concatenated inside the `Baloo::defaultExcludeFilterList()` function.

The conclusion is straightforward: __node\_modules, Python virtual environments, \_\_pycache\_\_, .git, CMakeFiles, and .terraform are already excluded out of the box.__ The massive creation of temporary files that makes developers fear Baloo in a programming environment is ignored by the engine before it even hits the disk. Anyone killing the indexer with a sledgehammer to “protect their SSD” is solving a problem that KDE has already solved.

#### Baloo’s Real Switch is systemd, Not a Phantom Process

Here I must correct a widespread rumor—one that I myself had taken for granted—: the idea that, when turned off, Baloo “remains lightweight in ps as a link to KRunner.” It does not. In Plasma 6, Baloo starts as a systemd user service defined in `kde-baloo.service`:

```javascript
[Service]
ExecStart=.../baloo_file
ExecCondition=.../kde-systemd-start-condition --condition \
    "baloofilerc:Basic Settings:Indexing-Enabled:true"
Slice=background.slice
CPUWeight=1
IOWeight=1
MemoryHigh=25%
```

Two things are structurally proven here. First, that `ExecCondition`: when `Indexing-Enabled` is set to `false`, the condition fails, and the service simply does not start. There is no lingering lightweight daemon; there is an absolute absence of a daemon. Second, even when enabled, KDE deliberately throttles it: CPU and I/O weights are pinned to the minimum (1), and memory consumption is capped at 25%. The resource-hogging indexer of popular imagination is, in code, a deliberately constrained process.

#### KWallet: The “Invasive Wizard” is Now Commented-Out Code

The “first-use” logic of the keyring lives in `src/runtime/ksecretd/ksecretd.cpp` (in Plasma 6, the daemon is `ksecretd`). The reading of the directive is exactly this:

```javascript
// inside KSecretD::reconfigure()
_firstUse = walletGroup.readEntry("First Use", true);
```

And the point where it is utilized, inside `doTransactionOpen()`, is far more sober than legends imply:

```php
if (_firstUse && !isPath) {
    // sets the default wallet and, if a local one already exists,
    // marks First Use = false and moves along.
    // ...
    // The block that instantiated KWalletWizard (the "graphical wizard")
    // is COMMENTED OUT in the current master.
}
```

Confronting this with honesty: the graphical wizard that many of us remember as an interruption is, in the current codebase, commented-out dead code. What does have a real and definitive effect is the `Enabled` key inside the `[Wallet]` group. Setting it to `false` prevents the subsystem from spawning entirely. The `First Use` key complements this, but the root cut is made by `Enabled`. _(As a side note: the First Wallet key found in various legacy tutorials does not exist in the code; the real keys are Enabled, First Use, and Default Wallet.)_

---

### 3. The Human Factor: No Configuration is an Absolute Truth

A serious analysis requires recognizing that there are user profiles who legitimately want both tools turned on. Anyone delegating their browser or Wi-Fi passwords to the convenience of a graphical interface needs KWallet active. Anyone accumulating gigabytes of technical documentation, books, or PDFs and searching for them instantly from the application launcher benefits enormously from Baloo—which, as we have seen, already dodges their code directories without being asked.

The goal of this recipe is not to blindly destroy system services, but to reclaim conscious choice. Whether a tool is enabled or disabled must be an administrative choice, not an automatism accepted by inertia. And because KDE exposes these toggles both in the GUI and via plain text, reproducible control is well within reach without relying on fragile hacks.

---

### 4. Configuration Guide via Plain Text

KDE stores its directives in `.ini` files inside `~/.config/`. Modifying them via the official `kwriteconfig6` utility guarantees a clean, reversible environment that remains safe across updates.

#### Option A — Pure Console Profile (Disabling)

```php
# 1) Disable Baloo indexing.
#    This causes the ExecCondition of kde-baloo.service to fail:
#    the service will not start again.
kwriteconfig6 --file baloofilerc --group "Basic Settings" \
              --key "Indexing-Enabled" false

# 2) Cut the KWallet subsystem at the root.
kwriteconfig6 --file kwalletrc --group Wallet --key Enabled false
kwriteconfig6 --file kwalletrc --group Wallet --key "First Use" false
```

Regarding the KRunner plugin that displays file search results: once indexing is turned off, it no longer has an index to pull data from. If you also wish to hide that runner from your global search, the cleanest way is to toggle it off via __System Settings → KRunner__. The equivalent backend key lives in `krunnerrc` under `[Plugins]` as `<id>Enabled`, but the specific plugin identifier varies between Plasma versions; before scripting it, confirm the exact name on your machine:

```
kreadconfig6 --file krunnerrc --group Plugins
```

Your files should end up looking like this:

```php
# ~/.config/baloofilerc
[Basic Settings]
Indexing-Enabled=false

# ~/.config/kwalletrc
[Wallet]
Enabled=false
First Use=false
```

#### Option B — Hybrid Profile (Returning to Factory Default)

If you choose to maintain the native behavior—KWallet securely storing your visual keys and Baloo indexing your PDFs, knowing its code already protects your development directories—execute the rollback block:

```javascript
kwriteconfig6 --file baloofilerc --group "Basic Settings" \
              --key "Indexing-Enabled" true

kwriteconfig6 --file kwalletrc --group Wallet --key Enabled true
kwriteconfig6 --file kwalletrc --group Wallet --key "First Use" true
```

#### Empirical Verification

Do not just assume that “it should work.” Verify it yourself:

```php
# What do the config files say?
kreadconfig6 --file baloofilerc --group "Basic Settings" --key "Indexing-Enabled"
kreadconfig6 --file kwalletrc   --group Wallet           --key Enabled

# Did the indexing service start or not?
systemctl --user status kde-baloo.service

# Is there any live Baloo daemon?
pgrep -a baloo_file || echo "Baloo is not running."
```
