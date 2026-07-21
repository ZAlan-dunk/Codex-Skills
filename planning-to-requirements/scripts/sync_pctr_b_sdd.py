#!/usr/bin/env python3
"""Synchronize one uploaded SDD link and confirmation state into PCTR-B artifacts."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def replace_line(body: str, label: str, value: str) -> str:
    pattern = re.compile(rf"^- {re.escape(label)}：.*$", re.M)
    line = f"- {label}：{value}"
    if not pattern.search(body):
        raise ValueError(f"missing line: {label}")
    return pattern.sub(line, body, count=1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("document")
    parser.add_argument("state")
    parser.add_argument("--feature", required=True)
    parser.add_argument("--sdd-local", required=True)
    parser.add_argument("--feishu-url", required=True)
    parser.add_argument("--sdd-revision", type=int, required=True)
    parser.add_argument("--sdd-status", required=True)
    parser.add_argument("--confirmation", choices=("pending", "confirmed", "ambiguous"), default="pending")
    parser.add_argument("--out-document", required=True)
    parser.add_argument("--out-state", required=True)
    args = parser.parse_args()
    text = Path(args.document).read_text(encoding="utf-8-sig")
    state = json.loads(Path(args.state).read_text(encoding="utf-8-sig"))
    heading = re.search(rf"^##\s+{re.escape(args.feature)}\s+.+$", text, re.M)
    if not heading:
        raise SystemExit(f"feature not found: {args.feature}")
    next_heading = re.search(r"^##\s+[A-Z][A-Z0-9-]*-F\d{3}\s+.+$", text[heading.end():], re.M)
    end = heading.end() + next_heading.start() if next_heading else len(text)
    body = text[heading.end():end]
    body = replace_line(body, "本地 SDD 工件", f"`{args.sdd_local}`")
    body = replace_line(body, "飞书 SDD 文档", args.feishu_url)
    body = replace_line(body, "SDD 状态 / Revision", f"{args.sdd_status} / {args.sdd_revision}")
    yes = "x" if args.confirmation == "confirmed" else " "
    no = "x" if args.confirmation == "ambiguous" else " "
    body = re.sub(r"^(\s*- \[)[ xX](\] 已确认\s*)$", rf"\g<1>{yes}\g<2>", body, count=1, flags=re.M)
    body = re.sub(r"^(\s*- \[)[ xX](\] 存在歧义需要修改\s*)$", rf"\g<1>{no}\g<2>", body, count=1, flags=re.M)
    updated = text[:heading.end()] + body + text[end:]
    table_row = re.compile(rf"^\|\s*`?{re.escape(args.feature)}`?\s*\|(.+)$", re.M)
    match = table_row.search(updated)
    if match:
        cells = [cell.strip() for cell in ("|" + match.group(0).strip("|") + "|").strip("|").split("|")]
        if len(cells) >= 8:
            cells[4] = f"[查看]({args.feishu_url})"
            updated = updated[:match.start()] + "| " + " | ".join(cells) + " |" + updated[match.end():]
    item = next((entry for entry in state.get("features", []) if entry.get("feature_id") == args.feature), None)
    if item is None:
        raise SystemExit(f"feature missing from state: {args.feature}")
    item.update({
        "sdd_local_path": args.sdd_local,
        "sdd_feishu_url": args.feishu_url,
        "sdd_revision": args.sdd_revision,
        "sdd_status": args.sdd_status,
        "sdd_confirmation_status": args.confirmation,
        "last_sync_at": datetime.now(timezone.utc).isoformat(),
    })
    Path(args.out_document).write_text(updated, encoding="utf-8")
    Path(args.out_state).write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"synchronized {args.feature}; confirmation={args.confirmation}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
