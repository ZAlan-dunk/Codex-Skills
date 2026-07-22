#!/usr/bin/env python3
"""Validate a PCTR-B single development Markdown document."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

FEATURE_RE = re.compile(r"^##\s+(\d+(?:\.\d+)*-[A-Z][A-Z0-9-]*-F\d{3})\s+(.+)$", re.M)
REQUIRED = (
    "### 1. 功能需求说明",
    "### 2. SDD确认文档",
    "### 3. 实施计划工件的路径",
    "### 4. 功能 Bug 修复记录文件路径",
    "### 5. 优化建议",
)
EXPECTED_COLUMNS = ("功能编码", "策案标题", "策案标题路径", "功能需求说明", "工时")
FORBIDDEN_COLUMNS = (
    "源策划进度", "策划确认", "开发状态", "验收状态", "SDD 确认文档",
    "实施计划工件路径", "Bug 修复记录文件路径", "优化建议",
)
MAX_SUMMARY_LENGTH = 140
MAX_REQUIREMENT_DESCRIPTION_LENGTH = 1200
SOURCE_MATERIAL_RE = re.compile(
    r"internal-api-drive-stream|https?://|!\[[^]]*\]\(|<\s*(?:img|table|figure|grid|source|cite|"
    r"whiteboard|sheet|bitable|synced_reference)\b",
    re.I,
)


def table_cells(line: str) -> list[str]:
    return [cell.replace("\\|", "|").strip() for cell in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def validate_requirement_text(value: str, context: str, max_length: int) -> list[str]:
    errors = []
    if len(value) > max_length:
        errors.append(f"{context}: exceeds {max_length} characters")
    if SOURCE_MATERIAL_RE.search(value):
        errors.append(f"{context}: contains source media/link/XML markup")
    if re.search(r"(?m)^\s*\|.+\|\s*$", value):
        errors.append(f"{context}: contains copied Markdown table content")
    return errors


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
        columns = table_cells(header)
        if tuple(columns) != EXPECTED_COLUMNS:
            errors.append(f"feature table columns must be exactly: {' / '.join(EXPECTED_COLUMNS)}")
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
            if body.count(heading) != 1:
                errors.append(f"{feature_id}: missing {heading}")
        if not re.search(r"^> 策案标题路径：\S+", body, re.M):
            errors.append(f"{feature_id}: missing source heading path")
        detail = re.search(
            r"^### 1\. 功能需求说明\s*$([\s\S]*?)(?=^### 2\. SDD确认文档\s*$)",
            body,
            re.M,
        )
        if not detail:
            errors.append(f"{feature_id}: 功能需求说明 section is malformed")
        else:
            description = detail.group(1).strip()
            if description:
                errors.extend(validate_requirement_text(
                    description,
                    f"{feature_id}: 功能需求说明",
                    MAX_REQUIREMENT_DESCRIPTION_LENGTH,
                ))
                if "主要功能点" not in description:
                    errors.append(f"{feature_id}: non-empty 功能需求说明 must contain 主要功能点")
                if not re.search(r"(?m)^\s*[-*+]\s+\S+", description):
                    errors.append(f"{feature_id}: non-empty 功能需求说明 must contain summary bullets")
        confirmed = re.findall(r"^\s*>?\s*- \[([ xX])\] 已确认\s*$", body, re.M)
        ambiguous = re.findall(r"^\s*>?\s*- \[([ xX])\] 存在歧义需要修改\s*$", body, re.M)
        if len(confirmed) != 1 or len(ambiguous) != 1:
            errors.append(f"{feature_id}: confirmation checkboxes missing or duplicated")
        elif confirmed[0].lower() == "x" and ambiguous[0].lower() == "x":
            errors.append(f"{feature_id}: confirmation checkboxes are mutually exclusive")
        if table and feature_id not in table.group(1):
            errors.append(f"{feature_id}: missing from feature table")
        elif table:
            row = re.search(rf"^\|\s*`?{re.escape(feature_id)}`?\s*\|(.+)$", table.group(1), re.M)
            if row:
                cells = table_cells(row.group(0))
                if len(cells) != 5 or not cells[3]:
                    errors.append(f"{feature_id}: table requirement summary is empty or malformed")
                elif len(cells) == 5:
                    errors.extend(validate_requirement_text(
                        cells[3],
                        f"{feature_id}: table requirement summary",
                        MAX_SUMMARY_LENGTH,
                    ))
        for required_block in ("🍞 本地 SDD 工件", "🏕️ SDD 状态 / Revision", "✍️ 确认状态"):
            if required_block not in body:
                errors.append(f"{feature_id}: missing highlighted block marker {required_block}")
        if "飞书 SDD 文档：" in body:
            errors.append(f"{feature_id}: separate Feishu SDD document field is forbidden")
        if not re.search(r"\|\s*序号\s*\|\s*BUG内容\s*\|\s*造成原因\s*\|", body):
            errors.append(f"{feature_id}: missing Bug table")
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
