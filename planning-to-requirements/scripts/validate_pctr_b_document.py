#!/usr/bin/env python3
"""Validate a PCTR-B single development Markdown document."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

FEATURE_RE = re.compile(r"^##\s+([A-Z][A-Z0-9-]*-F\d{3})\s+(.+)$", re.M)
REQUIRED = (
    "### 1. 功能需求说明",
    "### 2. SDD确认文档",
    "### 3. 实施计划工件的路径",
    "### 4. 功能 Bug 修复记录文件路径",
    "### 5. 优化建议",
)
FORBIDDEN_COLUMNS = ("源策划进度", "策划确认", "开发状态", "验收状态")


def validate(text: str) -> list[str]:
    errors = []
    if "## 文档定位" not in text:
        errors.append("missing 文档定位")
    if "| PCTR 模式 | B |" not in text:
        errors.append("document mode is not B")
    table = re.search(r"^## 功能总表\s*$([\s\S]*?)(?=^##\s+|\Z)", text, re.M)
    if not table:
        errors.append("missing 功能总表")
    else:
        header = next((line for line in table.group(1).splitlines() if line.strip().startswith("| 功能编码")), "")
        expected = ("功能编码", "策案标题", "策案标题路径", "功能需求说明", "SDD 确认文档", "实施计划工件路径", "Bug 修复记录文件路径", "优化建议")
        for column in expected:
            if column not in header:
                errors.append(f"feature table missing column: {column}")
        for column in FORBIDDEN_COLUMNS:
            if column in header:
                errors.append(f"forbidden status column: {column}")

    matches = list(FEATURE_RE.finditer(text))
    if not matches:
        errors.append("no PCTR-B feature headings found")
        return errors
    seen = set()
    for index, match in enumerate(matches):
        feature_id = match.group(1)
        if feature_id in seen:
            errors.append(f"duplicate feature id: {feature_id}")
        seen.add(feature_id)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end():end]
        for heading in REQUIRED:
            if heading not in body:
                errors.append(f"{feature_id}: missing {heading}")
        if not re.search(r"^> 策案标题路径：\S+", body, re.M):
            errors.append(f"{feature_id}: missing source heading path")
        confirmed = re.findall(r"^\s*- \[([ xX])\] 已确认\s*$", body, re.M)
        ambiguous = re.findall(r"^\s*- \[([ xX])\] 存在歧义需要修改\s*$", body, re.M)
        if len(confirmed) != 1 or len(ambiguous) != 1:
            errors.append(f"{feature_id}: confirmation checkboxes missing or duplicated")
        elif confirmed[0].lower() == "x" and ambiguous[0].lower() == "x":
            errors.append(f"{feature_id}: confirmation checkboxes are mutually exclusive")
        if table and feature_id not in table.group(1):
            errors.append(f"{feature_id}: missing from feature table")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("document")
    args = parser.parse_args()
    path = Path(args.document)
    errors = validate(path.read_text(encoding="utf-8-sig"))
    if errors:
        print("INVALID:", path)
        for error in errors:
            print("-", error)
        return 1
    print(f"VALID: {path} ({len(FEATURE_RE.findall(path.read_text(encoding='utf-8-sig')))} features)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
