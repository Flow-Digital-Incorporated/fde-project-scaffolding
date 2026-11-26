# Code Files

**Every code asset in this project is an `.mdx` file.** A code asset is code that gets pasted by hand into an app: Airtable automation scripts, Softr Vibe Coding blocks, Zapier code steps, custom HTML/CSS embeds. Never save one as `.js`, `.jsx`, `.ts`, `.tsx`, `.html` or `.css`.

**Exception: a file that a tool runs or deploys straight from disk** keeps the extension that tool needs. Local scripts that Node runs are `.jsx` (Node cannot run `.mdx`); start each with a short `/** */` comment: what it does, how to run it, and the date it last changed. (The template's own check script, `.claude/scripts/tasks.py`, is a tool too: keep it as it is.)

## What an `.mdx` code asset holds

1. **Frontmatter:** `title`, `app`, where it is deployed with its IDs (base and automation, Zap and step, Softr page and block), `status`, and `last_matched`: the date it last matched the deployed version.
2. **A short Markdown header:** what it does, its trigger and inputs, and a link to the live automation, Zap or page, as deep as the IDs allow.
3. **The code, exactly as deployed, in one fenced block** with its language (`javascript`, `python`, `tsx`, `html`, `css`). Code in several parts (HTML plus CSS) gets one fence per part, each under its own heading.

- MDX reads `{` and `<` in prose as code: write `\{` and `\<`, or put them in backticks. Inside a fence they are safe.
- No secrets in the file (see `asset-creation.md`). Where the deployed code holds one (a webhook URL, a key), the fence has a placeholder such as `ZAPIER_HOOK_ID` and the header says where the real value lives.
- To syntax-check the code, copy the fence to a file in the scratchpad and check that file.

Skeleton:

````mdx
---
title: "New Lead > Create Activities"
app: Airtable
base: "Client CRM (appXXXXXXXXXXXXXX)"
automation_id: wflXXXXXXXXXXXXXX
status: "on"
deployed_in: "Airtable automation, Run a script action"
last_matched: 2026-11-26
---

# New Lead > Create Activities

- **Where:** link to the automation, Run a script action. Status: on.
- **Trigger:** When a record is created in Leads.
- **Input variables:** none
- **What it does:** returns the date 7 days from now as the Due Date of the follow-up activity.
- **Last matched the live script:** 2026-11-26. After changing either side, update the other and this date.

## Script

```javascript
output.set("futureDate", new Date(Date.now() + 7 * 86400000).toISOString());
```
````
