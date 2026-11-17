# FDE Project Scaffolding

Flow Digital's template folder for Forward Deployed Engineer client engagements. Copy it once per client; Claude Code reads its `CLAUDE.md` + `.claude/rules/` automatically and works the way we work.

## Before your first project

- **1Password:** the 1Password app, signed in, and the 1Password CLI (`op`): `brew install 1password-cli` on a Mac, `winget install AgileBits.1Password.CLI` on Windows. In the app, turn on **Settings > Developer > Integrate with 1Password CLI**.
- **Team plugins:** the Flow Digital plugins (`security-toolkit`, `automation-toolkit`, `softr-vibe-coding`, `make-skills`, `zapier`) come from the company's Claude organization. If Claude says a skill such as `secrets-1password` is missing, tell Leo.

## How to start a new client project

1. **Get a project folder.** Normally the Claim button in #new-project-alerts creates it with a starter CLAUDE.md. Manual: create `First Last - Company` under Clients > your name and paste the scaffolding prompt (see the Project Scaffolding SOP). From git: clone, then run the Secrets (.env) setup in CLAUDE.md.
2. **Open Claude Code in that folder (never Cowork) and type `Start`.** The starter CLAUDE.md tells Claude to apply this template before any other request, so any first message starts the onboarding. Step-by-step setup with screenshots: [AI/Claude Project Scaffolding SOP](https://coda.io/d/_deZKBjDZAhI/AI-Claude-Project-Scaffolding_suBPVZkm).
3. Claude onboards you and sets up `.env` outside Google Drive, linked into the folder. It holds only `op://` references; every key lives in 1Password.

## Structure

```
├── CLAUDE.md              Project context, loaded every session — no-deletion rule,
│                          client/stack info, folder overview, per-app build conventions
├── TASKS.md               All tasks: P0 → P3 sections + Archive at the bottom
├── DECISIONS.md           Decision log — timestamped, ascending, append-only
├── MEMORY.md              Important things to remember about the project
├── .env                   Symlink to ~/.claude/clients/CLIENT/.env (op:// references only, outside Drive)
├── Assets/                Deliverables — empty by default, app folders created on demand
├── Archive/               Where "removed" things go; nothing is ever deleted
├── Fathom recordings/     Call transcripts, one file per call
└── .claude/rules/         Always-on working rules:
    ├── tasks.md             P0–P3 task management, task format, archiving
    ├── code-files.md        Every code file is .jsx, with a deployment header
    ├── softr.md             Softr work always via the softr-vibe-coding skill
    ├── asset-creation.md    App → folder mapping; folders created on first asset
    └── fathom-recordings.md Transcripts pasted by the FDE by default (saves tokens)
```

## House conventions (the short version)

- **Nothing gets deleted, ever** — files move to `Archive/`; client data in connected tools is never destroyed.
- **Every code file is `.jsx`**, whatever it contains — Airtable scripts, Softr blocks, Zapier code steps, HTML embeds.
- **Every credential lives in 1Password** (required) — read at run time with the `op` CLI; `.env` holds only `op://` references. See the `secrets-1password` skill (`security-toolkit` plugin).
- **Tasks** live in `TASKS.md` with AI-assigned P0–P3 priorities; **decisions** in `DECISIONS.md`; **project quirks** in `MEMORY.md`.
- **Builds go through skills**: `airtable-automation` (automations are "Run a script" scripts, never scripting extensions), `softr-vibe-coding`, `zapier-javascript` / `zapier-python`, `make-skills`. `DESIGN.md` comes from Step 1 of `softr-vibe-coding` (dembrandt), or from the `building-design-md` skill if it is installed.
- **Model**: Sonnet by default (see the SOP). Softr build work is the exception: Opus runs the session and gives the code to Sonnet subagents.

## Maintaining the template

This repo is the source of truth for the scaffolding. Client engagements are copies on Google Drive and are never pushed here — the `.gitignore` ignores `Assets/`, `Archive/`, and `Fathom recordings/` contents as a safety net. Edit, commit, push; then refresh the Drive master from here.
