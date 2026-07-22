#!/usr/bin/env python3
"""Register a created Feishu development document in PCTR-B local artifacts."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def table_value(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def replace_metadata_row(text: str, label: str, value: str) -> str:
    pattern = re.compile(rf"^\|\s*{re.escape(label)}\s*\|.*\|\s*$", re.M)
    matches = pattern.findall(text)
    if len(matches) != 1:
        raise ValueError(f"expected one metadata row for {label}, found {len(matches)}")
    return pattern.sub(f"| {label} | {table_value(value)} |", text, count=1)


def remove_metadata_row(text: str, label: str) -> str:
    pattern = re.compile(rf"^\|\s*{re.escape(label)}\s*\|.*\|\s*\r?\n?", re.M)
    return pattern.sub("", text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("document")
    parser.add_argument("state")
    parser.add_argument("--feishu-url", required=True)
    parser.add_argument("--revision", type=int, required=True)
    parser.add_argument("--sdd-parent-url", default="", help=argparse.SUPPRESS)
    parser.add_argument("--synced-at")
    parser.add_argument("--out-document", required=True)
    parser.add_argument("--out-state", required=True)
    args = parser.parse_args()

    if not args.feishu_url.strip():
        raise SystemExit("Feishu development-document URL is empty")
    if args.revision < 0:
        raise SystemExit("Feishu development-document revision must be non-negative")

    document_path = Path(args.document)
    state_path = Path(args.state)
    text = document_path.read_text(encoding="utf-8-sig")
    state = json.loads(state_path.read_text(encoding="utf-8-sig"))
    if state.get("mode") != "B" or state.get("schema_version") != 2:
        raise SystemExit("state schema/mode is not PCTR-B v2")

    synced_at = args.synced_at or datetime.now(timezone.utc).isoformat()
    text = replace_metadata_row(text, "本开发文档", args.feishu_url)
    text = replace_metadata_row(text, "本文档 Revision", str(args.revision))
    text = remove_metadata_row(text, "飞书 SDD 目标目录")
    text = replace_metadata_row(text, "最后同步时间", synced_at)

    development_document = state.setdefault("development_document", {})
    development_document.update(
        {
            "url": args.feishu_url,
            "revision": args.revision,
            "last_sync_at": synced_at,
        }
    )

    Path(args.out_document).write_text(text, encoding="utf-8")
    Path(args.out_state).write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        "registered PCTR-B Feishu development document; "
        f"revision={args.revision}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
