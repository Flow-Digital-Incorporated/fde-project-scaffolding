# Asset Creation

`Assets/` starts **empty**. Create an app's folder **on demand** — only at the moment the first asset of that type is actually being saved. Never pre-create empty folders.

| Asset | Folder |
|---|---|
| Airtable automation scripts | `Assets/Airtable Automations/` |
| Airtable base schema docs | `Assets/Airtable Base Schema/` |
| Softr blocks & custom code | `Assets/Softr App/{Page Name}/` |
| Zapier Zap specs & code steps | `Assets/Zaps/` |
| Make scenarios | `Assets/Make Scenarios/` |
| HubSpot / Pipedrive docs & code | `Assets/HubSpot/` · `Assets/Pipedrive/` |
| Embeds outside the stack apps | `Assets/Custom HTML/` |
| Any other app | `Assets/{App Name}/` |

- Saved code files are **source-of-truth mirrors** of what's deployed inside the tools — after changing either side, update the other and the header date.
- **Never store API keys, tokens, webhook secrets, or credentials in any asset file** — all secrets go in `.env` at the project root; reference them by variable name.
- Removing an asset = **moving it to `Archive/`** (see CLAUDE.md). Never deleting it.
