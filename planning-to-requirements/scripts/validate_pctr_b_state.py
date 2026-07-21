#!/usr/bin/env python3
"""Validate PCTR-B document/sidecar identity and confirmation state."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

FEATURE_RE = re.compile(r"^##\s+([A-Z][A-Z0-9-]*-F\d{3})\s+(.+)$", re.M)
ALLOWED = {"pending", "confirmed", "ambiguous"}


def checked(body: str, label: str) -> bool:
    match = re.search(rf"^\s*- \[([ xX])\] {re.escape(label)}\s*$", body, re.M)
    return bool(match and match.group(1).lower() == "x")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("document")
    parser.add_argument("state")
    args = parser.parse_args()
    text = Path(args.document).read_text(encoding="utf-8-sig")
    state = json.loads(Path(args.state).read_text(encoding="utf-8-sig"))
    errors = []
    if state.get("schema_version") != 1 or state.get("mode") != "B":
        errors.append("state schema/mode must be 1/B")
    matches = list(FEATURE_RE.finditer(text))
    document_items = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        document_items.append((match.group(1), match.group(2).strip(), text[match.end():end]))
    state_items = state.get("features", [])
    ids = [item.get("feature_id") for item in state_items]
    if len(ids) != len(set(ids)):
        errors.append("duplicate feature IDs in state")
    if [item[0] for item in document_items] != ids:
        errors.append("document/state feature order or IDs differ")
    by_id = {item.get("feature_id"): item for item in state_items}
    for feature_id, title, body in document_items:
        item = by_id.get(feature_id)
        if not item:
            continue
        if item.get("source_heading") != title:
            errors.append(f"{feature_id}: source heading differs")
        status = item.get("sdd_confirmation_status")
        if status not in ALLOWED:
            errors.append(f"{feature_id}: invalid confirmation status {status}")
            continue
        yes = checked(body, "已确认")
        no = checked(body, "存在歧义需要修改")
        expected = {"pending": (False, False), "confirmed": (True, False), "ambiguous": (False, True)}[status]
        if (yes, no) != expected:
            errors.append(f"{feature_id}: checkbox state does not match sidecar status")
        if status == "confirmed" and (not item.get("sdd_feishu_url") or int(item.get("sdd_revision", -1)) < 0):
            errors.append(f"{feature_id}: confirmed without Feishu SDD URL/revision")
        if status == "confirmed" and item.get("sdd_status") != "Approved":
            errors.append(f"{feature_id}: confirmed SDD status must be Approved")
    if errors:
        print("INVALID")
        for error in errors:
            print("-", error)
        return 1
    print(f"VALID: PCTR-B document/state features={len(document_items)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
