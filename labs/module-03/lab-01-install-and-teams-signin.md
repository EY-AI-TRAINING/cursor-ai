# Lab 3.1 — Install Cursor & Set Up Your Teams Plan Seat

**Module 3 · Cursor Interface & Setup | Xebia — Cursor AI Training**
Day 1 · Lab 1 of 3 · ~15–20 minutes · Individual · Cursor download + training credentials (Teams plan)

> **Objective:** get from "downloaded" to "licensed and ready" using the Cursor Teams-plan credentials your
> facilitator provides. The moment you sign in, your seat and the course team's settings attach to your install —
> signing in with the wrong identity is the single most common setup failure.

**Guide reference:** Module 3, §1 — Installing/Configuring Cursor AI; Connecting the Enterprise License
**Learning objective covered:** 1 — Install/configure Cursor and connect it to the license/account.

---

## Before you start

- Your training credentials — the Cursor Teams-plan account email and password provided by your facilitator
  (use exactly the account you were given)
- Local admin rights to install an application — or your org's MDM/software-portal path
- Disk and memory minimums: 8 GB RAM (16 GB recommended), ~5 GB free disk
- If Cursor is already installed and signed in with a personal account: that's fine — Step 2 fixes it

---

## Step 1 — Install Cursor (latest stable)

1. Download from **https://cursor.com/downloads** (all platforms). On managed devices, prefer your organization's
   software portal or MDM push.
2. Install for your OS:
   - **macOS:** open the `.dmg`, drag Cursor to Applications. First launch may require approval in
     System Settings → Privacy & Security.
   - **Windows:** run the installer and follow the prompts.
   - **Linux:** make the AppImage executable (`chmod +x`) and run it, or install from the tarball.
3. Launch Cursor. If the first-run screen offers to import VS Code settings, choose **Skip for now** — Lab 3.2
   performs the import deliberately.
4. Verify the build: Command Palette (`Cmd/Ctrl+Shift+P`) → search `About` → confirm a recent stable version.

- [ ] Cursor launches and the version is visible (record it: `____________`)

---

## Step 2 — Sign in with your training credentials

1. Already signed in with a personal account? Sign out first: `Cmd/Ctrl+Shift+J` →
   **General → Account → Sign Out**.
2. On the sign-in screen, sign in with the **email and password your facilitator provided** (the Teams-plan
   training account).
   - If your facilitator told you the course team uses SSO, choose the SSO option instead and complete the flow
     in the browser.
3. Confirm you're signed in as the training account — the account panel should show the training email,
   not a personal one.

- [ ] Signed in, and the account email is the training account you were given

> **Why this matters more than "logging in":** signing in attaches your Teams-plan seat and the course team's
> settings — model access, MCP allowlists, data-handling rules — to your Cursor install. A personal account
> would not carry any of that (Module 14 revisits team controls at governance scale).

---

## Step 3 — Verify the Teams plan and seat

1. Open Cursor Settings (`Cmd/Ctrl+Shift+J`) → **General → Account**. Confirm:
   - the signed-in email matches the training credentials you were given, and
   - the plan label reads **Teams**, not Free/Hobby/personal Pro.
2. Note the team/plan signals (this is the "seat vs local settings" lesson from the guide):
   - **Model access:** the model list may be constrained by the course team's model settings.
   - **Team controls:** team rules and Run Mode policies can be enforced centrally (Module 14) — you configure
     nothing locally.
   - Optional: note whether Privacy Mode is set (Settings → General → Privacy Mode).

- [ ] Plan shows **Teams**
- [ ] Email matches the training account
- [ ] Recorded the models your seat can access (count or names: `____________`)

---

## Step 4 — Capture evidence and explain

1. Screenshot **Cursor Settings → General → Account** (email and plan visible). This is your Lab 3.1 evidence.
2. In one sentence, record why the seat/account matters beyond just logging in:

   `______________________________________________________________________________`

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Credentials rejected / can't sign in | Typo, or the account is already in use elsewhere | Re-check the credentials with your facilitator; retry. If it persists, ask them to reset the password |
| Plan shows Free/personal Pro; model list looks personal | Signed in with a personal identity | Sign out, sign in with the training credentials (Step 2) |
| "Already a member of a team" on sign-in | Teams allows one team per Cursor account | Contact the facilitator/admin to move or reprovision the account |
| No seat recognized after sign-in | Seat not assigned, or revoked between cohorts | Contact the facilitator — seats are provisioned by the course admin (guide §1 flow diagram) |
| Install blocked on a managed device | MDM/application policy | Use your org's software portal or IT-provided package |
| Login errors behind VPN or proxy | Some proxies block HTTP/2 | Cursor Settings → Network → HTTP Compatibility Mode → HTTP/1.1 |
| An expected model is missing | Team model-access policy — not a bug | Note it; team settings control model access (Module 14) |

---

## Checkpoint questions

1. Name three things that attach to your Cursor install when you sign in to the course team account.
2. A teammate's Cursor shows different models and MCP servers than yours. What is the most likely explanation?
3. Where does "my seat isn't active" get fixed, and why can't you fix it yourself?

<details>
<summary>Answers</summary>

1. Your Teams-plan seat; team-level settings (model access, MCP allowlists, data handling); team admin controls
   (audit, governance).
2. Team/seat-level policy attached to their account — not a local setting.
3. With your facilitator/course admin. Seats are provisioned centrally in the team, not self-service.

</details>

---

## Next

**Lab 3.2** — import VS Code settings, open the training workspace, and tour the four interface anchors.
