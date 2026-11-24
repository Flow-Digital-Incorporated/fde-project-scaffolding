#!/usr/bin/env python3
"""Task file tools for the task-management skill.

  tasks.py check   <project folder>
  tasks.py compare <old file> [<old file> ...] --in <project folder>
  tasks.py regroup <task file> [--owner NAME] [--write]

Run with python3 -I. Reads only Markdown files; writes only with regroup --write.
"""
import argparse
import glob
import hashlib
import os
import re
import sys
import urllib.parse

PRIOS = ["P0", "P1", "P2", "P3"]
ID_RE = re.compile(r"^[A-Z]{2,4}-\d{2,}$")
SEP_RE = re.compile(r"^\|\s*:?-{3,}")
OPEN_COLS = ["ID", "Task", "Description", "Who", "Reference"]


def cells(line):
    s = line.rstrip("\n")
    if not (s.startswith("|") and s.rstrip().endswith("|")):
        return None
    return [c.strip() for c in s.strip()[1:-1].split("|")]


def tables(text):
    """Return a list of dicts: heading, header, rows [(line number, cells)], start, end (line indexes)."""
    lines = text.split("\n")
    out, heading, heading_idx, i, fence = [], None, None, 0, False
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("```"):
            fence = not fence
            i += 1
            continue
        if fence:
            i += 1
            continue
        if line.startswith("#"):
            heading, heading_idx = line.lstrip("#").strip(), i
        head = cells(line)
        if head is not None and i + 1 < len(lines) and SEP_RE.match(lines[i + 1]):
            rows, j = [], i + 2
            while j < len(lines) and cells(lines[j]) is not None:
                rows.append((j + 1, cells(lines[j])))
                j += 1
            out.append({"heading": heading, "heading_idx": heading_idx, "header": head,
                        "rows": rows, "start": i, "end": j})
            i = j
            continue
        i += 1
    return out


def link_target(cell, base):
    m = re.search(r"\]\(<?([^)>]+)>?\)", cell)
    if not m:
        return None
    href = m.group(1).split("#")[0]
    if not href or re.match(r"^[a-z][a-z0-9+.-]*:", href):
        return None
    return os.path.normpath(os.path.join(base, urllib.parse.unquote(href)))


def id_key(tid):
    p, n = tid.split("-", 1)
    return (p, int(n) if n.isdigit() else 0)


def check(folder):
    problems, notes = [], []
    seen, used, nextfree = {}, {}, {}
    task_files = sorted(f for f in glob.glob(os.path.join(folder, "TASKS*.md"))
                        if os.path.basename(f) != "TASKS-archive.md")
    if not task_files:
        print("No TASKS*.md in", folder)
        return 1

    def use(tid, where):
        if tid in seen:
            problems.append(f"{tid} is used twice: {seen[tid]} and {where}")
        seen[tid] = where
        p, n = id_key(tid)
        used[p] = max(used.get(p, 0), n)

    def ref_ok(tid, cell, base, where):
        tgt = link_target(cell, base)
        if tgt is None:
            problems.append(f"{where}: {tid} has no reference link")
            return None
        if not os.path.exists(tgt):
            problems.append(f"{where}: {tid} reference not found: {os.path.relpath(tgt, folder)}")
            return None
        if tid not in open(tgt, encoding="utf-8").read():
            problems.append(f"{where}: {tid} is not named in {os.path.relpath(tgt, folder)}")
        return tgt

    for f in task_files:
        name = os.path.basename(f)
        text = open(f, encoding="utf-8").read()
        for m in re.finditer(r"(?i)next free([^\n]*)", text):
            for p, n in re.findall(r"\b([A-Z]{2,4})-(\d{2,})\b", m.group(1)):
                nextfree.setdefault(p, int(n))
        heads = re.findall(r"^## (P[0-3])\s*$", text, re.M)
        if heads != PRIOS:
            problems.append(f"{name}: priority headings are {heads or 'missing'}; expected ## P0, ## P1, ## P2, ## P3 in that order")
        counts = {}
        for t in tables(text):
            header = t["header"]
            if not header or header[0] != "ID":
                continue
            if "P" in header:
                problems.append(f"{name}: table under '{t['heading']}' has a P column; run tasks.py regroup")
            elif header != OPEN_COLS:
                problems.append(f"{name}: table under '{t['heading']}' has columns {header}; expected {OPEN_COLS}")
            prio = t["heading"] if t["heading"] in PRIOS else None
            for ln, c in t["rows"]:
                where = f"{name}:{ln}"
                if len(c) != len(header):
                    problems.append(f"{where}: {len(c)} cells, the header has {len(header)}")
                    continue
                row = dict(zip(header, c))
                tid = row["ID"]
                if not ID_RE.match(tid):
                    problems.append(f"{where}: bad ID {tid!r}")
                    continue
                tgt = ref_ok(tid, row.get("Reference", ""), os.path.dirname(f), where)
                mirror = tgt is not None and os.path.basename(tgt).startswith("TASKS") and tgt != os.path.normpath(f)
                if not mirror:
                    use(tid, where)
                key = prio or row.get("P", "?")
                counts[key] = counts.get(key, 0) + 1
                words = len(row.get("Description", "").split())
                if words > 45:
                    notes.append(f"{where}: {tid} description has {words} words (aim for 40 at most)")
        notes.insert(0, f"{name}: " + (", ".join(f"{k} {counts[k]}" for k in sorted(counts)) or "no task rows"))

    arch = os.path.join(folder, "TASKS-archive.md")
    if os.path.exists(arch):
        text = open(arch, encoding="utf-8").read()
        dates = []
        for t in tables(text):
            header = t["header"]
            if not header or header[0] != "ID":
                continue
            for ln, c in t["rows"]:
                where = f"TASKS-archive.md:{ln}"
                if len(c) != len(header):
                    problems.append(f"{where}: {len(c)} cells, the header has {len(header)}")
                    continue
                row = dict(zip(header, c))
                tid = row["ID"]
                if not ID_RE.match(tid):
                    problems.append(f"{where}: bad ID {tid!r}")
                    continue
                use(tid, where)
                ref_ok(tid, row.get("Reference", ""), folder, where)
                if "Done" in row:
                    if not re.match(r"^\d{4}-\d{2}-\d{2}$", row["Done"]):
                        problems.append(f"{where}: date {row['Done']!r} is not YYYY-MM-DD")
                    dates.append(row["Done"])
        if dates != sorted(dates, reverse=True):
            problems.append("TASKS-archive.md: the rows are not newest first")
        notes.insert(0, f"TASKS-archive.md: {len(dates)} done")
    else:
        notes.append("No TASKS-archive.md yet")

    for p, mx in sorted(used.items()):
        if p not in nextfree:
            problems.append(f"prefix {p}: no 'Next free' number in a rules block (highest used {p}-{mx:02d})")
        elif nextfree[p] <= mx:
            problems.append(f"prefix {p}: next free {p}-{nextfree[p]:02d} is not above the highest used {p}-{mx:02d}")

    for n in notes:
        print("note:", n)
    for p in problems:
        print("PROBLEM:", p)
    print(f"{len(problems)} problem(s)")
    return 1 if problems else 0


TOKEN = re.compile(
    r"https?://[^\s)\]>`\"']+"          # links
    r"|claude://[^\s)]+"
    r"|\b[a-z]{2,6}_[0-9A-Za-z]{12,}\b"   # record IDs such as evs_..., tsk_..., lea_...
    r"|\b[0-9a-f]{12,64}\b"              # hashes and hex record IDs
    r"|`[^`\n]{3,120}`"                   # code, file names, keys
)


def compare(old_files, folder):
    corpus = []
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
        for fn in files:
            if fn.endswith(".md"):
                try:
                    corpus.append(open(os.path.join(root, fn), encoding="utf-8").read())
                except (OSError, UnicodeDecodeError):
                    pass
    corpus = "\n".join(corpus)
    total, missing = 0, []
    for f in old_files:
        for tok in sorted(set(TOKEN.findall(open(f, encoding="utf-8").read()))):
            total += 1
            probe = tok.strip("`").rstrip(".,;:")
            if probe not in corpus:
                missing.append((os.path.basename(f), tok))
    for f, tok in missing:
        print(f"MISSING ({f}): {tok}")
    print(f"{total} item(s) checked, {len(missing)} missing")
    return 1 if missing else 0


def regroup(path, owner, write):
    src = open(path, encoding="utf-8").read()
    h0 = hashlib.sha256(src.encode()).hexdigest()
    lines = src.split("\n")
    ts = [t for t in tables(src) if t["header"] and t["header"][0] == "ID" and "P" in t["header"]]
    if not ts:
        print("No table with an ID and a P column: nothing to regroup.")
        return 0
    rows = []
    for t in ts:
        for ln, c in t["rows"]:
            if len(c) != len(t["header"]):
                print(f"STOP: line {ln} has {len(c)} cells, the header has {len(t['header'])}")
                return 1
            row = dict(zip(t["header"], c))
            if row["P"] not in PRIOS:
                print(f"STOP: line {ln} has priority {row['P']!r}")
                return 1
            rows.append(row)
    # Replace from the heading of the first table (only a ## or lower heading directly above it)
    # to the end of the last table. The text before and after stays as it is.
    start = ts[0]["start"]
    h = ts[0]["heading_idx"]
    if h is not None and lines[h].startswith("##") and all(not l.strip() for l in lines[h + 1:start]):
        start = h
    end = ts[-1]["end"]
    inside = set()
    for t in ts:
        inside.update(range(t["start"], t["end"]))
    stray = [l for k, l in enumerate(lines[start:end], start)
             if k not in inside and l.strip() and not l.startswith("#")]
    if stray:
        print("STOP: this text between the tables would be lost; move it first:")
        for l in stray:
            print("   ", l[:120])
        return 1
    dropped = [l for l in lines[start:end] if l.startswith("#")]

    def first(row):
        return 0 if owner and row.get("Who", "").startswith(owner) else 1

    out = []
    for p in PRIOS:
        out.append(f"## {p}")
        group = sorted((r for r in rows if r["P"] == p), key=lambda r: (first(r), id_key(r["ID"])))
        if not group:
            out += ["None.", ""]
            continue
        out.append("| " + " | ".join(OPEN_COLS) + " |")
        out.append("|" + "---|" * len(OPEN_COLS))
        for r in group:
            out.append("| " + " | ".join(r.get(col, "") for col in OPEN_COLS) + " |")
        out.append("")
    before, after = lines[:start], lines[end:]
    while before and not before[-1].strip():
        before.pop()
    while after and not after[0].strip():
        after.pop(0)
    new = "\n".join(before + [""] + out + after)
    counts = {p: sum(1 for r in rows if r["P"] == p) for p in PRIOS}
    print("rows:", len(rows), counts, "| owner first:", owner or "(none)")
    print("old headings replaced:", ", ".join(dropped) or "none")
    if not write:
        print("\n".join(out))
        print("(preview only; add --write to save)")
        return 0
    if hashlib.sha256(open(path, encoding="utf-8").read().encode()).hexdigest() != h0:
        print("STOP: the file changed while the script ran; run it again")
        return 1
    open(path, "w", encoding="utf-8").write(new)
    print("written:", path)
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("folder")
    m = sub.add_parser("compare")
    m.add_argument("old", nargs="+")
    m.add_argument("--in", dest="folder", required=True)
    r = sub.add_parser("regroup")
    r.add_argument("file")
    r.add_argument("--owner", default="")
    r.add_argument("--write", action="store_true")
    a = ap.parse_args()
    if a.cmd == "check":
        return check(a.folder)
    if a.cmd == "compare":
        return compare(a.old, a.folder)
    return regroup(a.file, a.owner, a.write)


if __name__ == "__main__":
    sys.exit(main())
