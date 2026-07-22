#!/usr/bin/env python3
"""Register one local SDD Markdown attachment and confirmation state in PCTR-B artifacts."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def replace_code_block(body: str, label: str, value: str) -> str:
    pattern = re.compile(
        rf"(`{re.escape(label)}：`\s*\n+\s*```text\s*\n)([\s\S]*?)(\n```)",
        re.M,
    )
    if not pattern.search(body):
        raise ValueError(f"missing code block: {label}")
    return pattern.sub(lambda match: match.group(1) + value + match.group(3), body, count=1)


def resolve_feature(state: dict, requested: str) -> dict:
    matches = []
    for entry in state.get("features", []):
        identities = {
            entry.get("feature_id", ""),
            entry.get("base_feature_id", ""),
            *entry.get("legacy_feature_ids", []),
        }
        if requested in identities:
            matches.append(entry)
    if len(matches) != 1:
        raise SystemExit(f"feature identity matched {len(matches)} entries: {requested}")
    return matches[0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("document")
    parser.add_argument("state")
    parser.add_argument("--feature", required=True)
    parser.add_argument("--sdd-local", required=True)
    parser.add_argument("--attachment-name", required=True)
    parser.add_argument("--attachment-token", default="")
    parser.add_argument("--attachment-url", default="")
    parser.add_argument("--development-revision", type=int, required=True)
    parser.add_argument("--sdd-version", required=True)
    parser.add_argument("--sdd-status", required=True)
    parser.add_argument("--confirmation", choices=("pending", "confirmed", "ambiguous"), default="pending")
    parser.add_argument("--out-document", required=True)
    parser.add_argument("--out-state", required=True)
    args = parser.parse_args()
    sdd_path = Path(args.sdd_local)
    if sdd_path.suffix.lower() != ".md":
        raise SystemExit("SDD attachment must be a local .md file")
    if not args.attachment_token.strip() and not args.attachment_url.strip():
        raise SystemExit("attachment token or URL is required after automatic/manual insertion")
    if args.development_revision < 0:
        raise SystemExit("containing development-document revision must be non-negative")
    text = Path(args.document).read_text(encoding="utf-8-sig")
    state = json.loads(Path(args.state).read_text(encoding="utf-8-sig"))
    if state.get("schema_version") != 2 or state.get("mode") != "B":
        raise SystemExit("state schema/mode is not PCTR-B v2")
    item = resolve_feature(state, args.feature)
    current_feature_id = item["feature_id"]
    if not sdd_path.is_file():
        raise SystemExit(f"local SDD Markdown not found: {args.sdd_local}")
    sdd_text = sdd_path.read_text(encoding="utf-8-sig")
    if current_feature_id not in sdd_text:
        raise SystemExit(f"local SDD metadata does not contain current Feature ID: {current_feature_id}")
    heading = re.search(rf"^##\s+{re.escape(current_feature_id)}\s+.+$", text, re.M)
    if not heading:
        raise SystemExit(f"feature not found: {current_feature_id}")
    next_heading = re.search(r"^##\s+\d+(?:\.\d+)*-[A-Z][A-Z0-9-]*-F\d{3}\s+.+$", text[heading.end():], re.M)
    end = heading.end() + next_heading.start() if next_heading else len(text)
    body = text[heading.end():end]
    body = replace_code_block(body, "路径", args.sdd_local)
    attachment_display = (
        f"[Markdown 附件：{args.attachment_name}]({args.attachment_url})"
        if args.attachment_url
        else f"Markdown 附件：{args.attachment_name}（token: `{args.attachment_token}`）"
    )
    attachment_pattern = re.compile(r"^Markdown 附件：.*$|^\[Markdown 附件：.*$", re.M)
    if not attachment_pattern.search(body):
        raise SystemExit("feature section is missing Markdown attachment placeholder")
    body = attachment_pattern.sub(attachment_display, body, count=1)
    status_pattern = re.compile(r"^> 🏕️ SDD 状态 / Revision：.*$", re.M)
    if not status_pattern.search(body):
        raise SystemExit("feature section is missing SDD status highlighted block")
    body = status_pattern.sub(
        f"> 🏕️ SDD 状态 / Revision：{args.sdd_status} / {args.sdd_version}",
        body,
        count=1,
    )
    yes = "x" if args.confirmation == "confirmed" else " "
    no = "x" if args.confirmation == "ambiguous" else " "
    body = re.sub(r"^(\s*>?\s*- \[)[ xX](\] 已确认\s*)$", rf"\g<1>{yes}\g<2>", body, count=1, flags=re.M)
    body = re.sub(r"^(\s*>?\s*- \[)[ xX](\] 存在歧义需要修改\s*)$", rf"\g<1>{no}\g<2>", body, count=1, flags=re.M)
    updated = text[:heading.end()] + body + text[end:]
    item.update({
        "sdd_local_path": args.sdd_local,
        "sdd_attachment_name": args.attachment_name,
        "sdd_attachment_token": args.attachment_token,
        "sdd_attachment_url": args.attachment_url,
        "sdd_attachment_document_revision": args.development_revision,
        "sdd_version": args.sdd_version,
        "sdd_status": args.sdd_status,
        "sdd_confirmation_status": args.confirmation,
        "last_sync_at": datetime.now(timezone.utc).isoformat(),
    })
    state.setdefault("development_document", {})["revision"] = args.development_revision
    Path(args.out_document).write_text(updated, encoding="utf-8")
    Path(args.out_state).write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"registered Markdown attachment for {current_feature_id}; confirmation={args.confirmation}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
