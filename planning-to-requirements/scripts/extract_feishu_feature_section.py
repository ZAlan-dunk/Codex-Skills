#!/usr/bin/env python3
"""Extract one feature section from a Markdown/Feishu-exported planning document."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.M)


def clean_heading(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().strip("#").strip()


def heading_entries(text: str) -> list[dict]:
    matches = list(HEADING_RE.finditer(text))
    stack: list[tuple[int, str]] = []
    entries = []
    for idx, match in enumerate(matches):
        level = len(match.group(1))
        title = clean_heading(match.group(2))
        while stack and stack[-1][0] >= level:
            stack.pop()
        stack.append((level, title))
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        entries.append({
            "level": level,
            "title": title,
            "path": " / ".join(item[1] for item in stack),
            "start": match.start(),
            "end": end,
            "body_start": match.end(),
        })
    return entries


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_markdown")
    parser.add_argument("--heading-path", default="")
    parser.add_argument("--title", default="")
    parser.add_argument("--feature", default="", help="feature id to look for in heading/body")
    parser.add_argument("--revision", type=int, default=-1)
    parser.add_argument("--out", default="")
    parser.add_argument("--json", dest="json_out", action="store_true")
    args = parser.parse_args()

    source_path = Path(args.source_markdown)
    text = source_path.read_text(encoding="utf-8-sig")
    entries = heading_entries(text)
    matches = []
    for entry in entries:
        section = text[entry["start"]:entry["end"]]
        if args.heading_path and entry["path"] == args.heading_path:
            matches.append(entry)
        elif args.title and entry["title"] == args.title:
            matches.append(entry)
        elif args.feature and args.feature in section:
            matches.append(entry)
    if len(matches) != 1:
        raise SystemExit(f"feature section matched {len(matches)} headings; provide a stricter --heading-path/title/feature")
    entry = matches[0]
    section = text[entry["start"]:entry["end"]].strip() + "\n"
    result = {
        "source_markdown": str(source_path),
        "revision": args.revision,
        "heading_path": entry["path"],
        "title": entry["title"],
        "level": entry["level"],
        "sha256": hashlib.sha256(section.encode("utf-8")).hexdigest(),
        "content": section,
    }
    if args.out:
        Path(args.out).write_text(section, encoding="utf-8")
    if args.json_out:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(section, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
