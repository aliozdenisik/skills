#!/usr/bin/env python3
"""Extract mandatory markers and validate a compact audit; stdlib only."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

MARKER = re.compile(r"^\s*<!-- requirement: ([A-Za-z0-9][A-Za-z0-9_.:-]*) -->\s*$")
HEADER = ["ID", "Verification", "Evidence", "Status", "Missing Work"]
STATUSES = {"SATISFIED", "PARTIAL", "MISSING", "CONTRADICTED", "UNVERIFIED"}
METHODS = {"TEST", "INSPECTION", "ANALYSIS", "DEMONSTRATION"}
EMPTY = {"", "—", "-", "n/a", "none", "tbd"}


def unfenced(text):
    fence = None
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
        if match:
            run, tail = match.groups()
            if fence is None:
                fence = run
                continue
            if run[0] == fence[0] and len(run) >= len(fence) and not tail.strip():
                fence = None
                continue
        if fence is None:
            yield line
    if fence is not None:
        raise ValueError("Unclosed Markdown fence")


def duplicates(ids):
    return sorted(key for key, count in Counter(ids).items() if count > 1)


def inventory(path):
    raw = Path(path).read_bytes()
    ids = []
    for line in unfenced(raw.decode("utf-8")):
        match = MARKER.fullmatch(line)
        if match:
            ids.append(match[1])
        elif "<!-- requirement" in line:
            raise ValueError("Malformed requirement marker: " + line)
    if not ids or duplicates(ids):
        raise ValueError(f"Empty inventory or duplicate declarations: {duplicates(ids)}")
    return {"sha256": hashlib.sha256(raw).hexdigest(), "ids": ids}


def audit_rows(path):
    rows = []
    headers = 0
    for line in unfenced(Path(path).read_text(encoding="utf-8")):
        if not line.strip().startswith("|"):
            continue
        if not line.strip().endswith("|"):
            raise ValueError("Table row must end with a pipe")
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip()[1:-1])]
        if cells == HEADER:
            headers += 1
            continue
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        if len(cells) != 5:
            raise ValueError("Audit rows must have exactly five cells")
        rows.append(cells)
    if headers != 1:
        raise ValueError("Expected exactly one audit table with the prescribed header")
    return rows


def check(source, snapshot, audit):
    current = inventory(source)
    if current != json.loads(Path(snapshot).read_text(encoding="utf-8")):
        raise ValueError("Requirements changed or inventory mismatch; re-extract and reassess")
    rows = audit_rows(audit)
    actual = [row[0] for row in rows]
    expected = current["ids"]
    errors = []
    for label, values in (
        ("missing", sorted(set(expected) - set(actual))),
        ("extra", sorted(set(actual) - set(expected))),
        ("duplicate", duplicates(actual)),
    ):
        if values:
            errors.append(f"{label}: {', '.join(values)}")
    for rid, method, evidence, status, work in rows:
        if status not in STATUSES:
            errors.append(f"{rid}: invalid status")
        if method != "—" and not all(m.strip() in METHODS for m in method.split("+")):
            errors.append(f"{rid}: invalid verification method")
        if status == "SATISFIED":
            if method == "—" or evidence.lower() in EMPTY or work not in {"—", "-", ""}:
                errors.append(f"{rid}: satisfied row needs verification/evidence and no missing work")
        else:
            errors.append(f"{rid}: {status}")
            if work.lower() in EMPTY:
                errors.append(f"{rid}: missing targeted next action")
    if errors:
        raise ValueError("; ".join(errors))
    print(f"COVERAGE_OK: {len(expected)}/{len(expected)} unique IDs; all rows SATISFIED. "
          "Agent must validate evidence and semantic coverage before COMPLETE.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    extract = commands.add_parser("extract")
    extract.add_argument("requirements")
    verify = commands.add_parser("check")
    for argument in ("requirements", "inventory", "audit"):
        verify.add_argument(argument)
    args = parser.parse_args()
    try:
        if args.command == "extract":
            print(json.dumps(inventory(args.requirements), indent=2))
        else:
            check(args.requirements, args.inventory, args.audit)
    except (ValueError, OSError) as error:
        print(f"INCOMPLETE: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
