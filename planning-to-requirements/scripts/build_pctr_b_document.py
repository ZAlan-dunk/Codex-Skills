#!/usr/bin/env python3
"""Build a PCTR-B single development document and sidecar from normalized Markdown."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def clean_title(value: str) -> str:
    return re.sub(r"\s+#+\s*$", "", value).strip()


def esc(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def parse_leaf_features(text: str) -> list[dict]:
    lines = text.splitlines()
    headings = []
    stack: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if not match:
            continue
        level = len(match.group(1))
        title = clean_title(match.group(2))
        while stack and stack[-1][0] >= level:
            stack.pop()
        path = [entry[1] for entry in stack] + [title]
        headings.append({"line": index, "level": level, "title": title, "path": path, "has_child": False})
        if stack:
            parent_path = path[:-1]
            for candidate in reversed(headings[:-1]):
                if candidate["path"] == parent_path:
                    candidate["has_child"] = True
                    break
        stack.append((level, title))

    result = []
    for idx, heading in enumerate(headings):
        if heading["has_child"]:
            continue
        end = headings[idx + 1]["line"] if idx + 1 < len(headings) else len(lines)
        body = "\n".join(lines[heading["line"] + 1 : end]).strip()
        result.append({
            "title": heading["title"],
            "path": " / ".join(heading["path"]),
            "body": body,
        })
    return result


def load_existing(path: str | None) -> dict:
    if not path:
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def assign_ids(features: list[dict], document_code: str, existing: dict) -> None:
    old = {item.get("source_heading_path"): item for item in existing.get("features", [])}
    used = {item.get("feature_id", "") for item in existing.get("features", [])}
    numbers = []
    for value in used:
        match = re.search(r"-F(\d{3})$", value)
        if match:
            numbers.append(int(match.group(1)))
    next_number = max(numbers, default=0) + 1
    for feature in features:
        prior = old.get(feature["path"])
        if prior and prior.get("feature_id"):
            feature["feature_id"] = prior["feature_id"]
            continue
        while f"{document_code}-F{next_number:03d}" in used:
            next_number += 1
        feature["feature_id"] = f"{document_code}-F{next_number:03d}"
        used.add(feature["feature_id"])
        next_number += 1


def build_document(features: list[dict], args: argparse.Namespace, existing: dict) -> str:
    prior_document = existing.get("development_document", {})
    development_url = prior_document.get("url") or "待上传/待填写"
    development_revision = prior_document.get("revision", -1)
    feishu_parent_url = args.feishu_parent_url or prior_document.get("feishu_parent_url", "")
    last_sync_at = prior_document.get("last_sync_at") or "待同步"
    out = [
        f"# {args.title}", "", "## 文档定位", "",
        "| 字段 | 内容 |", "|---|---|",
        "| PCTR 模式 | B |",
        f"| 来源策案 | {args.source_url or '待填写'} |",
        f"| 来源 Revision | {args.source_revision} |",
        f"| 本开发文档 | {development_url} |",
        f"| 本文档 Revision | {development_revision} |",
        f"| 飞书 SDD 目标目录 | {feishu_parent_url or '待填写'} |",
        f"| 项目根目录 | `{args.project_root}` |",
        f"| 文档编码 | `{args.document_code}` |",
        f"| 本地状态清单 | `{args.state_out}` |",
        f"| SDD 工件根目录 | `{args.sdd_root}` |",
        f"| 实施计划根目录 | `{args.plan_root}` |",
        f"| Bug 记录根目录 | `{args.bug_root}` |",
        f"| 最后同步时间 | {last_sync_at} |", "",
        "> 本文档严格保持来源策案的功能标题和顺序。存在子标题时以叶子/小标题作为功能；没有子标题时以大标题作为功能。", "",
        "## 功能总表", "",
        "| 功能编码 | 策案标题 | 策案标题路径 | 功能需求说明 | SDD 确认文档 | 实施计划工件路径 | Bug 修复记录文件路径 | 优化建议 |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for feature in features:
        fid = feature["feature_id"]
        out.append(f"| `{fid}` | {esc(feature['title'])} | {esc(feature['path'])} |  | 待上传 | 待生成 | 暂无 | 见下文 |")
    for feature in features:
        out += [
            "", "---", "", f"## {feature['feature_id']} {feature['title']}", "",
            f"> 策案标题路径：{feature['path']}", "",
            "### 1. 功能需求说明", "", "",
            "### 2. SDD确认文档", "",
            "- 本地 SDD 工件：", "- 飞书 SDD 文档：", "- SDD 状态 / Revision：", "- 确认状态：",
            "  - [ ] 已确认", "  - [ ] 存在歧义需要修改", "",
            "### 3. 实施计划工件的路径", "",
            "- 本地路径：", "- 上传说明：默认不自动上传；成功开发后由程序手动上传，或在用户明确要求时同步链接。", "",
            "### 4. 功能 Bug 修复记录文件路径", "", "- 暂无", "",
            "### 5. 优化建议", "", "- 由 SDD、ACSDM 与代码检索补充；不得改写来源策案事实。",
        ]
    return "\n".join(out).rstrip() + "\n"


def build_state(features: list[dict], args: argparse.Namespace, existing: dict) -> dict:
    old = {item.get("feature_id"): item for item in existing.get("features", [])}
    items = []
    for feature in features:
        prior = old.get(feature["feature_id"], {})
        fingerprint = hashlib.sha256((feature["path"] + "\n" + feature["body"]).encode("utf-8")).hexdigest()
        items.append({
            "feature_id": feature["feature_id"],
            "source_heading": feature["title"],
            "source_heading_path": feature["path"],
            "source_fingerprint": fingerprint,
            "sdd_local_path": prior.get("sdd_local_path", ""),
            "sdd_feishu_url": prior.get("sdd_feishu_url", ""),
            "sdd_revision": prior.get("sdd_revision", -1),
            "sdd_status": prior.get("sdd_status", ""),
            "sdd_confirmation_status": prior.get("sdd_confirmation_status", "pending"),
            "implementation_plan_path": prior.get("implementation_plan_path", ""),
            "bug_record_paths": prior.get("bug_record_paths", []),
            "last_sync_at": prior.get("last_sync_at", ""),
        })
    prior_document = existing.get("development_document", {})
    return {
        "schema_version": 1,
        "mode": "B",
        "document_code": args.document_code,
        "source": {"url": args.source_url, "revision": args.source_revision},
        "development_document": {
            "url": prior_document.get("url", ""),
            "revision": prior_document.get("revision", -1),
            "local_path": args.out,
            "feishu_parent_url": args.feishu_parent_url or prior_document.get("feishu_parent_url", ""),
            "last_sync_at": prior_document.get("last_sync_at", ""),
        },
        "features": items,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("--out", required=True)
    parser.add_argument("--state-out", required=True)
    parser.add_argument("--document-code", required=True)
    parser.add_argument("--title", default="SDD 工件开发文档")
    parser.add_argument("--source-url", default="")
    parser.add_argument("--source-revision", type=int, default=-1)
    parser.add_argument("--project-root", default="")
    parser.add_argument("--feishu-parent-url", default="")
    parser.add_argument("--sdd-root", default="CodexTemp/OrangeUnityForge/specs/")
    parser.add_argument("--plan-root", default="CodexTemp/PCTR/B/plans/")
    parser.add_argument("--bug-root", default="CodexTemp/PCTR/B/bugs/")
    parser.add_argument("--existing-state")
    args = parser.parse_args()
    args.document_code = re.sub(r"[^A-Z0-9]+", "-", args.document_code.upper()).strip("-")
    if not args.document_code:
        raise SystemExit("document code is empty after normalization")
    source = Path(args.source).read_text(encoding="utf-8-sig")
    features = parse_leaf_features(source)
    if not features:
        raise SystemExit("no leaf/source feature headings found")
    existing = load_existing(args.existing_state)
    assign_ids(features, args.document_code, existing)
    Path(args.out).write_text(build_document(features, args, existing), encoding="utf-8")
    Path(args.state_out).write_text(json.dumps(build_state(features, args, existing), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"created {args.out}; state={args.state_out}; features={len(features)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
