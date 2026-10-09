#!/usr/bin/env python3
"""Generate site/corpus.js, the data behind the project page's paper explorer.

    python3 scripts/build_site_data.py          # rewrite site/corpus.js
    python3 scripts/build_site_data.py --check  # exit 1 if it is out of date

README.md stays the single source of truth for entries; docs/claim-audit.md
for verdicts. The page never carries a hand-edited copy of either, so an entry
added to the list reaches the explorer only through this script, and
check_consistency.py fails if the generated file has drifted.
"""

import argparse
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
AUDIT = os.path.join(ROOT, "docs", "claim-audit.md")
OUTPUT = os.path.join(ROOT, "site", "corpus.js")

# Top-level README sections that hold entries, mapped to explorer groups.
GROUPS = [
    ("Precursors", "precursors", "Precursors"),
    ("1. Interpreted Update Targets", "interpreted", "Interpreted targets"),
    ("2. Executable Update Targets", "executable", "Executable targets"),
    ("3. Evaluation & Benchmarks", "evaluation", "Evaluation & benchmarks"),
    ("4. Theory", "theory", "Theory"),
    ("6. Persistent-State Risks", "risks", "Persistent-state risks"),
    ("7. Deployed Harnesses & Product Surfaces", "products", "Deployed products"),
    ("Related Surveys", "surveys", "Related surveys"),
]
ENTRY = re.compile(r"^- \*\*(?P<name>.+?)\*\*(?: `(?P<venue>[^`]+)`)? — (?P<desc>.+?)(?P<links>(?: ?(?:·\s*)?\[\[\w+\]\]\([^)]+\))+)\s*$")
LINK = re.compile(r"\[\[(\w+)\]\]\(([^)]+)\)")
VERDICT_ROW = re.compile(r"^\| \[\*\*(?P<name>.+?)\*\*\]\([^)]+\).*?\| (?P<s>\S+) \| (?P<a>\S+) \| (?P<t>\S+) \| (?P<i>\S+) \|$")
VERDICT_CODE = {"✅": "C", "◐": "O", "—": "N", "n/a": "X"}


def inline_markdown(text):
    """The handful of inline forms the mechanism sentences use, as HTML."""
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return text


def read_verdicts():
    verdicts = {}
    for line in open(AUDIT, encoding="utf-8"):
        match = VERDICT_ROW.match(line.strip())
        if match:
            verdicts[match["name"]] = "".join(VERDICT_CODE[match[k]] for k in "sati")
    return verdicts


def read_entries(verdicts):
    group_of = {title: (key, label) for title, key, label in GROUPS}
    group = subsection = mechanism = None
    blurbs = {}
    entries, seen = [], set()
    fenced = False
    pending_blurb = None
    for raw in open(README, encoding="utf-8"):
        line = raw.rstrip("\n")
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if line.startswith("## "):
            group = group_of.get(line[3:])
            subsection = mechanism = None
            continue
        if group is None:
            continue
        if line.startswith("### "):
            subsection, mechanism = line[4:], None
            pending_blurb = subsection
            continue
        if line.startswith("#### "):
            mechanism = line[5:]
            pending_blurb = mechanism
            continue
        # The italic line right under a heading is that node's one-line gloss.
        if pending_blurb and line.startswith("*") and line.endswith("*") and not line.startswith("**"):
            blurbs[pending_blurb] = inline_markdown(line.strip("*"))
            pending_blurb = None
            continue
        match = ENTRY.match(line)
        if not match:
            continue
        pending_blurb = None
        name = match["name"]
        # SkillForge is the declared repeat (Section 4 re-lists it); the
        # explorer shows each work once, at its taxonomy position.
        if name in seen:
            continue
        seen.add(name)
        node = mechanism or subsection or ""
        entries.append({
            "name": name,
            "venue": match["venue"] or "",
            "desc": inline_markdown(match["desc"].strip()),
            "links": [[kind, url] for kind, url in LINK.findall(match["links"])],
            "group": group[0],
            "sub": re.sub(r"^\d+\.\d+ ", "", subsection or ""),
            "node": re.sub(r"^\d+\.\d+ ", "", node),
            "verdict": verdicts.get(name, ""),
        })
    return entries, blurbs


def render():
    verdicts = read_verdicts()
    entries, blurbs = read_entries(verdicts)
    audited = [e for e in entries if e["verdict"]]
    if len(audited) != len(verdicts):
        missing = sorted(set(verdicts) - {e["name"] for e in audited})
        raise SystemExit(f"audit rows without a README entry: {missing}")
    data = {
        "groups": [{"key": key, "label": label} for _, key, label in GROUPS],
        "blurbs": blurbs,
        "entries": entries,
    }
    body = json.dumps(data, ensure_ascii=False, indent=1)
    return ("// Generated by scripts/build_site_data.py from README.md and docs/claim-audit.md.\n"
            "// Do not edit by hand; rerun the script after changing either file.\n"
            f"window.CORPUS = {body};\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if site/corpus.js is out of date")
    args = parser.parse_args()
    content = render()
    if args.check:
        current = open(OUTPUT, encoding="utf-8").read() if os.path.exists(OUTPUT) else ""
        if current != content:
            print("site/corpus.js is out of date; run python3 scripts/build_site_data.py")
            return 1
        print("site/corpus.js is up to date")
        return 0
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as handle:
        handle.write(content)
    count = content.count('"name":')
    print(f"wrote {os.path.relpath(OUTPUT, ROOT)} with {count} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
