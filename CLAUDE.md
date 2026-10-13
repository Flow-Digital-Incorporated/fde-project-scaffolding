# CLAUDE.md — {{CLIENT_FULL_NAME}} / {{BUSINESS_NAME}}

## ⚠️ IMPORTANT — nothing gets deleted. Ever.

- **Never delete anything.** No `rm` / `rm -rf` in this project folder, no deleting files or folders, and no deleting client data through MCPs or APIs (Airtable records/tables/bases, Softr pages, CRM records, Zaps, Make scenarios, …).
- To "remove" a local file: **move it to `Archive/`**, then create the new file.
- If something truly must be destroyed, flag it to the FDE — a human deletes it manually, never you.

> **TEMPLATE CHECK:** if this file still contains `{{...}}` placeholders, this is a fresh copy of the template — onboard before any other work:
> 1. Ask in chat: client full name · business name · one-paragraph TLDR · engagement scope · your name (FDE, becomes Engagement lead) · kickoff date (default today).
> 2. `AskUserQuestion` (multiSelect): apps involved — Airtable, Softr, Zapier, HubSpot; others (Pipedrive, Make, Notion, …) via Other.
> 3. Per app, in chat: one-line role + links ("TBD" is fine).
> 4. Fill every placeholder here and in TASKS.md / DECISIONS.md / MEMORY.md, build the Stack table, then delete this banner. Verify no `{{` remains in the project. Then run the "Secrets (.env)" setup below. Never create a real `.env` in this folder.
> 5. Setup template found at: https://github.com/Flow-Digital-Incorporated/fde-project-scaffolding

## Client
- **Client:** {{CLIENT_FULL_NAME}}
- **Business:** {{BUSINESS_NAME}}
- **What they do:** {{BUSINESS_TLDR}}
- **Engagement lead:** {{FDE_NAME}} (Flow Digital)
- **Kickoff:** {{START_DATE}}

## Engagement scope
{{ENGAGEMENT_SCOPE}}

## Stack
| App | Role in this project | Link |
|---|---|---|
| {{APP_NAME}} | {{APP_ROLE}} | {{APP_LINK}} |

## Folder overview
| Location | What it is |
|---|---|
| [TASKS.md](TASKS.md) | All tasks, P0–P3. **New tasks are always created here**, following `.claude/rules/tasks.md`; completed tasks move to its Archive section |
| [DECISIONS.md](DECISIONS.md) | Decision log — **every decision gets appended with a timestamp, in ascending order** (newest at the bottom) |
| [MEMORY.md](MEMORY.md) | The important things to remember about this project — client quirks, preferences, gotchas, conventions. Read at session start; add to it as you learn |
| `.env` | Symlink to the real file at `~/.claude/clients/CLIENT/.env` (outside Google Drive). **All secrets live there** — API keys, tokens, webhook secrets. Never in code, specs, or docs; reference by variable name. If missing or BROKEN, follow "Secrets (.env)" below |
| `Assets/` | Deliverables. **Empty by default** — folders are created on demand per `.claude/rules/asset-creation.md` |
| `Archive/` | Where "removed" things go. Nothing is ever deleted — it's moved here |
| `Fathom recordings/` | Call transcripts, one file per call — handled per `.claude/rules/fathom-recordings.md` |
| `DESIGN.md` | Brand + design tokens — exists once the `building-design-md` skill has run |

## Build conventions
- **Every code file is a `.jsx` file** — see `.claude/rules/code-files.md`.
- **Airtable:** automations are **Automation "Run a script" scripts — never scripting extensions**. Build them with the `airtable-automation` skill.
- **Softr:** anything Softr goes through the `softr-vibe-coding` skill — see `.claude/rules/softr.md`.
- **Zapier:** code steps via the `zapier-javascript` skill; `zapier-python` only on explicit request.
- **Make** (similar tool to Zapier): scenarios via the `make-skills` plugin skills.
- **Design/brand:** the `building-design-md` skill produces `DESIGN.md`.

## Rules (`.claude/rules/`)
All always-on, all short: `tasks.md` · `code-files.md` · `softr.md` · `asset-creation.md` · `fathom-recordings.md`

## Secrets (.env)

This project folder syncs to Google Drive, so real API keys must never be stored in it. The real file lives outside Drive, and `.env` in this folder is a symlink to it. Never print, copy, log, or commit key values.

**Locations**
- Home folder: `$HOME` on macOS/Linux, `$env:USERPROFILE` on Windows.
- CLIENT slug: take the project folder name ("First Last - Company"), keep the part after " - ", lowercase it, replace spaces with hyphens, and remove everything except a-z, 0-9 and hyphens. If there is no " - ", ask the user.
- Real file: `$HOME/.claude/clients/CLIENT/.env` (Windows: `$env:USERPROFILE\.claude\clients\CLIENT\.env`)

**Setup** (run during onboarding before any other app work, and again whenever the check below reports BROKEN)
1. Detect the OS. Use Claude Code's file tools (Read/Write) to create folders and files so it works everywhere. Use the shell only for the symlink, deletion, and checks. Claude Code may ask permission to write outside this folder; that is expected.
2. Create `$HOME/.claude/clients/CLIENT/` if it does not exist (macOS/Linux: also `chmod 700`).
3. If `$HOME/.claude/clients/CLIENT/.env` does not exist, create it as an exact copy of this folder's `.env.example` (same lines, comments, and order). If it already exists, do not touch it.
4. Handle `.env` in this project folder:
   - Symlink to the correct target: do nothing.
   - Symlink to anywhere else: stop and tell the user.
   - Regular file: this is the one exception to the "nothing gets deleted" rule. Do not read, move, or merge it. Send this heads-up and wait for a reply: "A regular .env exists in this Google Drive synced folder and will be permanently deleted. Copy any API keys you need to keep first. Reply 'delete' when ready." Only after the user replies "delete", delete it explicitly (macOS/Linux `rm .env`, Windows `Remove-Item .env`), then create the symlink.
   - Missing: create the symlink.
5. Create the symlink:
   - macOS/Linux: `ln -s "$HOME/.claude/clients/CLIENT/.env" .env`
   - Windows (use PowerShell even if the shell is Git Bash, because `ln -s` there makes a copy): `New-Item -ItemType SymbolicLink -Path .env -Target "$env:USERPROFILE\.claude\clients\CLIENT\.env"`
   - If Windows reports a missing privilege, tell the user to turn on Developer Mode (Windows Settings, search "Developer Mode") and retry. Never fall back to a copy or a hard link, and never place a real .env in this folder.
6. Tell the user to open `.env` and paste their keys. They save to the non-synced file.
7. Verify with the check below, without showing contents.

**Check** (before and after any task that edits .env)
- macOS/Linux: `test -L .env && echo OK || echo BROKEN`
- Windows: `if ((Get-Item .env -Force -ErrorAction SilentlyContinue).LinkType -eq 'SymbolicLink') {'OK'} else {'BROKEN'}`
- BROKEN usually means an editor replaced the symlink with a regular file on save. Follow the "Regular file" case in step 4.

## Notes
- This folder lives on Google Drive (shared drive) — expect sync latency. Not a git repo.
