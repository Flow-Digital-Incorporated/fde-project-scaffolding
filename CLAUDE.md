# CLAUDE.md — {{CLIENT_FULL_NAME}} / {{BUSINESS_NAME}}

## ⚠️ IMPORTANT — nothing gets deleted. Ever.

- **Never delete anything.** No `rm` / `rm -rf` in this project folder, no deleting files or folders, and no deleting client data through MCPs or APIs (Airtable records/tables/bases, Softr pages, CRM records, Zaps, Make scenarios, …).
- To "remove" a local file: **move it to `Archive/`**, then create the new file.
- If something truly must be destroyed, flag it to the FDE — a human deletes it manually, never you.

> **TEMPLATE CHECK:** if this file still contains `{{...}}` placeholders, this is a fresh copy of the template — onboard before any other work:
> 1. Ask in chat: client full name · business name · one-paragraph TLDR · engagement scope · your name (FDE, becomes Engagement lead) · kickoff date (default today).
> 2. `AskUserQuestion` (multiSelect): apps involved — Airtable, Softr, Zapier, HubSpot; others (Pipedrive, Make, Notion, …) via Other.
> 3. Per app, in chat: one-line role + links ("TBD" is fine).
> 4. Fill every placeholder here and in TASKS.md / DECISIONS.md / MEMORY.md, build the Stack table, then delete this banner. Verify no `{{` remains in the project. If `.env` is missing (fresh clone), copy `.env.example` to `.env`.

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
| `.env` | **All secrets live here** — API keys, tokens, webhook secrets. Never in code, specs, or docs; reference by variable name. Gitignored — if missing (fresh clone), copy `.env.example` to `.env` |
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

## Notes
- This folder lives on Google Drive (shared drive) — expect sync latency. Not a git repo.
