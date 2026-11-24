# Task Management

Goal: anyone can see in one minute what is open, who acts next and how urgent it is. The details stay one click away. Nothing is lost when a task closes. Never track work anywhere else. (The `task-management` skill, where it is installed, uses the same format.)

## Files

| File | Holds |
|---|---|
| [TASKS.md](../../TASKS.md) | Open tasks only. One table per priority, under `## P0`, `## P1`, `## P2`, `## P3`. The priority key and the rules block are at the end. |
| [TASKS-archive.md](../../TASKS-archive.md) | Done and cancelled tasks. One table, newest first. |
| `references/<area>.md` | One section per open task, with all the details. Make the file when its area gets its first task. |
| `references/archive/<area>.md` | The sections of done and cancelled tasks. |

`Archive/` at the project root is for removed files, not for tasks. A large topic can get its own list, `TASKS-<topic>.md`: same format, its own prefix, named in one line in the TASKS.md header.

## Table format

`| ID | Task | Description | Who | Reference |`

- **ID:** `<PREFIX>-<NN>`, for example `AIR-03`. Numbers have two digits and only go up. An ID never changes and is never used again, also not after the task is archived.
- **Task:** a name of 3 to 8 words.
- **Description:** 40 words at most. Give the state and the next step, with dates. No history and no record IDs here.
- **Who:** the first name of the person who acts next: the FDE, a client contact, or "Claude". Examples: "Emily", "Emily, then Claude", "Sarah (client)".
- **Reference:** a relative link to the area file, for example `[airtable.md](references/airtable.md)`. Write a space in a path as `%20`.
- **Order** in each table: first the rows where the FDE (the engagement lead) acts next, that is "Who" starts with their name. Then the others. Inside each group, sort by ID. Each item the FDE must do or decide gets its own row.
- An empty priority keeps its heading, with the word "None." under it and no table.
- Never put `|` inside a cell.

**Priority** (Claude sets it when it makes the task; the FDE can change it): **P0** blocks the client or the engagement now. **P1** is important, or has a date within 30 days. **P2**: do soon. **P3** is optional, or waits for someone else without a date.

## Prefixes and areas

One prefix per area, 2 to 4 capital letters. Defaults: GEN (project, client, calls, access), AIR (Airtable), SFT (Softr), ZAP (Zapier), MAK (Make), HUB (HubSpot), PIP (Pipedrive). Another app gets 2 to 4 capital letters from its name. The area file has the area name in lower case: `references/general.md`, `references/airtable.md`, `references/softr.md`, and so on.

The TASKS.md rules block lists the prefixes in use and the next free number of each. When an app joins the stack, add its prefix there with next free `<PREFIX>-01`.

## Reference sections

`## <ID> <title> (<YYYY-MM-DD opened>)`, then:
- **Source:** where the task came from. If it came from a call, name the exact file, for example `Fathom recordings/2026-08-12 - Kickoff.md`, so more context can be found there.
- The facts: links as deep as the IDs allow (base, table, record, Zap, scenario, page), record IDs, each decision with its date and the person's words (a project decision also goes in DECISIONS.md), and the next step.

## Steps

Parallel sessions can edit these files. Read a task file again just before you edit it, and change only your own rows.

- **Add:** take the next free number of the prefix and raise the number in the rules block. Add the reference section, then the row in the right table and place.
- **Change:** add a dated line to the reference section and update the row. To change the priority, move the row to the other table. When the FDE has done their part, change "Who" to the next person and move the row down.
- **Close** (only with proof: the live state, the record, the client's reply): remove the row. Add a row with the same ID at the top of the table in TASKS-archive.md. Move the section to `references/archive/<area>.md` and add `- Done <YYYY-MM-DD>: <what is true now, and the proof>`.
- **Cancel:** the same as close. The outcome starts with "Cancelled:" and gives the reason. A task is never deleted.
- **Check** after each change: `python3 -I .claude/scripts/tasks.py check .` and fix every problem it lists. If Python 3 is not installed, check by hand against this file.

## Archive format

`| ID | Done | Task | Outcome | Reference |`. Newest first. Write the date as YYYY-MM-DD. The outcome has 25 words at most and says what is now true. The reference links to `references/archive/<area>.md`. The second table, "Finished parts of tasks that are still open" (`| Open task | Done part | Reference |`), is optional.

## Old format

A TASKS.md with `### <task name>` entries and an Archive section uses the old format. To change it: copy TASKS.md to `Archive/`, give each entry an ID, and put its full text word for word in its reference section. Open entries get a row in TASKS.md. Done and cancelled entries get a row in TASKS-archive.md and their text goes in `references/archive/`. Then run the check.
