# Fathom Recordings

Call transcripts live in `Fathom recordings/`, one file per call: `YYYY-MM-DD - {topic}.md`.

## Default: the FDE pastes the transcript themselves

When a call needs to be captured, **create an empty stub file** `Fathom recordings/YYYY-MM-DD - {topic}.md` (with a small header: date, topic, attendees) and ask the FDE to open it, paste the transcript from Fathom, and save. That costs **zero tokens**.

## Only on explicit request

Pull a transcript via the Fathom MCP, or accept one pasted into chat and write it to file, **only when the FDE explicitly asks for it** — and give this disclaimer first: *routing a transcript through Claude uses tokens unnecessarily; opening the stub file and pasting into it directly is free.*

## Using transcripts

When a new transcript lands, offer to mine it: action items → TASKS.md (with this file as `Source:` per the tasks rule), decisions → DECISIONS.md, notable facts → MEMORY.md.
