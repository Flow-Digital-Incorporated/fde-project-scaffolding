# Tasks

Open work for {{BUSINESS_NAME}}. Details: `references/<area>.md`, one section per task ID. Done work: [TASKS-archive.md](TASKS-archive.md). Format and steps: `.claude/rules/tasks.md`. Last update: {{START_DATE}}.

## P0
None.

## P1
None.

## P2
None.

## P3
None.

**Priority:** P0 blocks the client or the engagement now. P1 is important, or has a date within 30 days. P2: do soon. P3 is optional, or waits for someone else without a date. Claude sets the priority; the FDE can change it.

**Rules**
- One row per task, 40 words at most. Details, history and record IDs go in the reference section.
- In each table, the rows where {{FDE_FIRST_NAME}} acts next come first, then the others; inside each group, sort by ID.
- An ID never changes and is never used again. Prefixes: {{TASK_PREFIXES}}. Next free: {{TASK_NEXT_FREE}}.
- When a task is done or cancelled: remove its row, add a row with the same ID at the top of TASKS-archive.md, and move its section to `references/archive/<area>.md`.
- Parallel sessions edit this file. Re-read it just before an edit, and change only your own rows.
- Check after each change: `python3 -I .claude/scripts/tasks.py check .`
