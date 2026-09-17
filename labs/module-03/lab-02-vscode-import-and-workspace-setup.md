# Lab 3.2 — Import VS Code Settings & Open the Training Workspace

**Module 3 · Cursor Interface & Setup | Xebia — Cursor AI Training**
Day 1 · Lab 2 of 3 · ~15–20 minutes · Individual

> **Objective:** carry over your VS Code muscle memory (optional but recommended), then open the training sandbox
> repository **as a workspace** — the unit that owns rules, MCP configuration, and trust decisions for everything
> that follows in this course.

**Guide references:** Module 3, §2 (Interface Walkthrough) and §3 (Importing VS Code Settings/Extensions; Workspace & Project Setup)
**Learning objectives covered:** 2 — navigate the four interface anchors; 3 — import VS Code settings and set up a workspace correctly.

---

## Before you start

- The path to `<sandbox-repo>` (facilitator-provided)
- Optional: an existing VS Code install/profile and ~10 minutes for extensions to reinstall
- Cursor installed and signed in with the training credentials (Lab 3.1 complete)

---

## Step 1 — Import from VS Code (optional, recommended)

**Why:** Cursor is a VS Code fork, and the import brings over keybindings, themes, settings, snippets, and compatible
extensions — so you're not starting from a blank editor (guide §3).

1. Cursor Settings (`Cmd/Ctrl+Shift+J`) → **General → Account**.
2. Under **VS Code Import**, click **Import**. Wait for extensions to reinstall.
3. Verify:
   - your usual theme and a custom keybinding work,
   - the Extensions view (`Cmd/Ctrl+Shift+X`) shows the extensions you expect.
4. Head's up on compatibility: Cursor uses the **Open VSX** registry, not the VS Code Marketplace. Most popular
   extensions are available, but some may be missing or behave differently — note any gaps rather than fighting them.
5. If the one-click import misses something, use the manual profile route: in VS Code, Command Palette →
   `Preferences: Open Profiles (UI)` → export the profile; then run the same palette command in Cursor and import it.
6. Don't use VS Code? Skip this step deliberately and record "no prior config to import" — nothing later depends on it.

- [ ] Theme/keybindings feel familiar — or the import was deliberately skipped
- [ ] Extensions view checked; anything missing is noted

---

## Step 2 — Open the training sandbox repository as a workspace

1. `File → Open Folder…` → select **`<sandbox-repo>`** — the repository **root**, not a subfolder.
   The folder you open *is* the workspace; workspace-level config (`.cursor/`, rules, MCP, permissions) attaches to
   that folder and only that folder.
2. Open the integrated terminal (`` Ctrl+` ``) and run:

   ```bash
   pwd
   git status
   git branch --show-current
   ```

   Confirm you're at the repo root, on the expected branch, with a clean-enough working tree.
3. Check what workspace config already exists:

   ```bash
   ls -a
   ls -a .cursor 2>/dev/null || echo "no .cursor directory yet"
   ```

   If there's no `.cursor/` yet, that's expected: Module 8 creates `.cursor/rules/`, Module 12 adds workspace-level
   MCP config, and `.cursor/permissions.json` is where auto-run allowlists can live (looked at in Lab 3.3).

- [ ] Explorer shows the sandbox repo at its root
- [ ] Terminal works and `git status` runs cleanly (branch: `____________`)
- [ ] Noted whether `.cursor/` already exists (yes / no)

---

## Step 3 — Tour the four interface anchors

Reference (guide §2):

| Anchor | Where | What it's for |
|---|---|---|
| **Editor** | Center | Open files/tabs, inline Tab suggestions, diff review |
| **Sidebar** | Left | File explorer, Search, Source Control (Git), Extensions |
| **Command Palette** | `Cmd/Ctrl+Shift+P` | Any command without hunting menus — the fastest escape hatch when the UI moves |
| **Chat/Agent Panel** | Right | Mode selector, model selector, @-mention context picker — Modules 4–7 live here |

**Anchor drills:**

1. **Editor:** open a source file from the Explorer. Note the Tab ghost-text hints as you type — observe only,
   Module 5 covers Tab properly.
2. **Sidebar:** open Search (`Cmd/Ctrl+Shift+F`) and find a string you know exists in the repo.
3. **Command Palette:** practice the escape hatch. Search each of these and note what exists in your build:
   `Cursor Settings`, `Import`, `MCP`, `auto-run`, `Run Mode`, `Workspace Trust`, `Keyboard Shortcuts`.
4. **Chat/Agent Panel:** open it (`Cmd/Ctrl+L` or `Cmd/Ctrl+I`; `Cmd/Ctrl+E` toggles the agent layout). Locate the
   **mode selector**, the **model selector**, and the `@` context picker. Don't execute anything yet — Lab 3.3 runs
   the first agent command.

- [ ] All four anchors located
- [ ] Command Palette searched for all seven strings
- [ ] Chat/Agent Panel can be toggled without the mouse (`Cmd/Ctrl+L`, `Cmd/Ctrl+I`, or `Cmd/Ctrl+E`)
- [ ] Mode selector, model selector, and `@` picker located (not used yet)

---

## Step 4 — Understand config ownership: user vs workspace

| Scope | Where it lives | Travels with |
|---|---|---|
| User-level (personal) | `~/.cursor/`, VS Code settings (`Cmd/Ctrl+,`) | Your machine only — not your team |
| Workspace-level (team) | `<repo>/.cursor/` — rules, MCP config, `permissions.json` | The repository — everyone who opens it |

**Engineering takeaway (guide §3):** treat the workspace folder as the unit of configuration. Workspace-level settings
travel with the repo for your whole team; user-level settings are personal and don't.

- [ ] Can state one example of a user-level setting and one workspace-level asset

---

## Evidence

- Screenshot: Explorer with the sandbox repo open **and** terminal output of `git status` / branch
- Note the import result: extensions that came over, and any that didn't (`____________`)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Import didn't bring extensions | Open VSX registry differences; occasional import bugs in older builds | Reinstall from the Extensions view; or use the manual profile import |
| Workspace config doesn't seem to apply | You opened a subfolder | `File → Open Folder…` → reopen at the repo root |
| `git: command not found` | Git not installed / not on PATH | Install Git and restart Cursor's terminal |
| Theme/keybindings unchanged | Import skipped or partial | Re-run the import, or set them manually |
| Terminal opens a different shell (zsh/PowerShell) | Shell configuration | Fine — all lab commands are shell-agnostic |

---

## Checkpoint questions

1. Which folder must you open for workspace-level rules/MCP/permissions to apply?
2. Name one thing you can import from VS Code and one thing Cursor adds that VS Code doesn't have.
3. Why does "the workspace is the unit of configuration" matter for a team?

<details>
<summary>Answers</summary>

1. The repository root — the workspace folder. Config attaches to the opened folder, not to Cursor globally.
2. Imported: keybindings/themes/settings/snippets/extensions. Cursor adds: `.cursor/rules` (project rules),
   workspace-level MCP configuration, agent permissions — assets with no VS Code equivalent (guide §3 diagram).
3. Team-shared assets (rules, MCP, permissions) live in the repo and are version-controlled; personal settings
   don't follow teammates, so shared behavior must be committed in the workspace.

</details>

---

## Next

**Lab 3.3** — workspace trust, permission scoping, model/mode selection, and your first agent command.
