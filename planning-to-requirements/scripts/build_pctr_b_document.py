#!/usr/bin/env python3
"""Build a PCTR-B single development document and sidecar from normalized Markdown."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
EXPLICIT_SEQUENCE_RE = re.compile(r"^(?P<sequence>\d+(?:\.\d+)*)(?:[.)、])?\s+(?P<title>.+)$")
BASE_FEATURE_ID_RE = re.compile(r"(?P<base>[A-Z][A-Z0-9-]*-F\d{3})$")
CITE_TITLE_RE = re.compile(r'<cite\b[^>]*\btitle="([^"]+)"', re.I)
MEDIA_MARKER_RE = re.compile(
    r"internal-api-drive-stream|https?://|<\s*(?:img|table|figure|grid|source|whiteboard|sheet|bitable)\b",
    re.I,
)
GENERIC_LABEL_RE = re.compile(
    r"^(?:玩法说明|实现方式|交互相关|交互表现|视觉表现|相关处理|与现有道具的相关处理|"
    r"关卡失败/重开的处理|弹窗触发时机|道具使用效果|存档触发时机|自动提示效果|"
    r"道具提醒效果|关于自动提示和道具提醒的倒计时)[：:]\s*"
)


def clean_title(value: str) -> str:
    return re.sub(r"\s+#+\s*$", "", value).strip()


def esc(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def split_explicit_sequence(title: str) -> tuple[str, str]:
    match = EXPLICIT_SEQUENCE_RE.match(title)
    if not match:
        return "", title
    return match.group("sequence"), match.group("title").strip()


def normalize_summary_line(raw: str) -> str:
    line = raw.strip()
    if not line:
        return ""
    if line.startswith("|") and line.endswith("|"):
        return ""
    if "<" in line:
        prefix = line.split("<", 1)[0].strip()
        if not prefix:
            return ""
        line = prefix
    if MEDIA_MARKER_RE.search(line):
        return ""
    if re.fullmatch(r"\|?\s*:?-+:?\s*(?:\|\s*:?-+:?\s*)+\|?", line):
        return ""
    if re.fullmatch(r"[-*+>]\s*\*\*[^*]{1,40}[：:]?\*\*", line):
        return ""
    line = re.sub(r"^#{1,6}\s+", "", line)
    line = re.sub(r"^[-*+>]\s*", "", line)
    line = re.sub(r"^\d+[.)、]\s*", "", line)
    line = re.sub(r"!\[([^]]*)\]\([^)]*\)", "", line)
    line = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", line)
    line = re.sub(r"<[^>]+>", " ", line)
    line = re.sub(r"[`*_~]", "", line)
    line = re.sub(r"[（(]?如(?:下)?图\s*\d*(?:所示)?[）)]?", "", line)
    line = re.sub(r"[（(]?见(?:下)?图\s*\d*[）)]?", "", line)
    line = re.sub(r"[（(]?下面视频(?:这个动效)?[）)]?", "", line)
    line = GENERIC_LABEL_RE.sub("", line)
    line = re.sub(r"\s+", " ", line).strip(" |；，。:：　")
    if not line or re.fullmatch(r"[^：:]{1,30}[：:]", line):
        return ""
    return line


def requirement_summary(body: str, title: str, limit: int = 90) -> str:
    candidates = []
    in_fence = False
    for raw in body.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        line = normalize_summary_line(raw)
        if line and line not in candidates:
            candidates.append(line)
        if len("；".join(candidates)) >= limit:
            break
    summary = "；".join(candidates).strip()
    if not summary:
        citation_titles = list(dict.fromkeys(CITE_TITLE_RE.findall(body)))
        if citation_titles:
            summary = f"按来源策案引用的《{'、'.join(citation_titles)}》完成“{title}”相关要求。"
        else:
            summary = f"“{title}”的具体规则待策划补充。"
    return summary if len(summary) <= limit else summary[: limit - 1].rstrip("；，。 ") + "…"


def effective_requirement_summary(feature: dict, prior: dict, limit: int = 90) -> str:
    description = str(prior.get("requirement_description", "")).strip()
    summary = description.split("\n\n", 1)[0].strip() if description else feature["summary"]
    return summary if len(summary) <= limit else summary[: limit - 1].rstrip("；，。 ") + "…"


def parse_leaf_features(text: str) -> list[dict]:
    lines = text.splitlines()
    headings = []
    stack: list[dict] = []
    root_count = 0
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if not match:
            continue
        level = len(match.group(1))
        raw_title = clean_title(match.group(2))
        explicit_sequence, title = split_explicit_sequence(raw_title)
        while stack and stack[-1]["level"] >= level:
            stack.pop()
        if stack:
            stack[-1]["child_count"] += 1
            ordinal = stack[-1]["child_count"]
            derived_sequence = f"{stack[-1]['sequence']}.{ordinal}"
        else:
            root_count += 1
            derived_sequence = str(root_count)
        if explicit_sequence and explicit_sequence != derived_sequence:
            raise ValueError(
                f"heading sequence mismatch at line {index + 1}: "
                f"visible={explicit_sequence}, derived={derived_sequence}, title={title}"
            )
        sequence = explicit_sequence or derived_sequence
        path = [entry["title"] for entry in stack] + [title]
        heading = {
            "line": index,
            "level": level,
            "title": title,
            "path": path,
            "sequence": sequence,
            "has_child": False,
            "child_count": 0,
        }
        headings.append(heading)
        if stack:
            stack[-1]["has_child"] = True
        stack.append(heading)

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
            "sequence": heading["sequence"],
            "summary": requirement_summary(body, heading["title"]),
        })
    return result


def load_existing(path: str | None) -> dict:
    if not path:
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def normalize_planning_version(value: str) -> str:
    normalized = re.sub(r"\s+", "-", value.strip())
    normalized = re.sub(r"[^A-Za-z0-9._-]+", "-", normalized).strip("-._")
    if not normalized:
        raise SystemExit("planning version is empty after normalization")
    return normalized


def feature_artifact_dir(args: argparse.Namespace, feature: dict) -> Path:
    return Path(args.artifact_root) / feature["feature_id"]


def feature_artifact_paths(args: argparse.Namespace, feature: dict) -> dict[str, str]:
    root = feature_artifact_dir(args, feature)
    return {
        "feature_artifact_dir": str(root),
        "planner_confirmation_snapshot": str(root / "A-01-planner-confirmation-snapshot.md"),
        "decomposition": str(root / "A-02-feature-decomposition.md"),
        "runtime_sdd": str(root / "B-01-runtime-sdd.md"),
    }


def assign_ids(features: list[dict], document_code: str, existing: dict) -> None:
    old = {item.get("source_heading_path"): item for item in existing.get("features", [])}
    used = set()
    numbers = []
    for item in existing.get("features", []):
        value = item.get("base_feature_id") or item.get("feature_id", "")
        match = BASE_FEATURE_ID_RE.search(value)
        if match:
            base = match.group("base")
            used.add(base)
            number_match = re.search(r"-F(\d{3})$", base)
            if number_match:
                numbers.append(int(number_match.group(1)))
    next_number = max(numbers, default=0) + 1
    for feature in features:
        prior = old.get(feature["path"])
        base_id = ""
        if prior:
            base_id = prior.get("base_feature_id", "")
            if not base_id:
                match = BASE_FEATURE_ID_RE.search(prior.get("feature_id", ""))
                base_id = match.group("base") if match else ""
        if not base_id:
            while f"{document_code}-F{next_number:03d}" in used:
                next_number += 1
            base_id = f"{document_code}-F{next_number:03d}"
            used.add(base_id)
            next_number += 1
        feature["base_feature_id"] = base_id
        feature["feature_id"] = f"{feature['sequence']}-{base_id}"
        legacy = set(prior.get("legacy_feature_ids", []) if prior else [])
        if prior and prior.get("feature_id") and prior["feature_id"] != feature["feature_id"]:
            legacy.add(prior["feature_id"])
        legacy.add(base_id)
        feature["legacy_feature_ids"] = sorted(legacy)


def build_document(features: list[dict], args: argparse.Namespace, existing: dict) -> str:
    prior_document = existing.get("development_document", {})
    prior_by_path = {item.get("source_heading_path"): item for item in existing.get("features", [])}
    development_url = prior_document.get("url") or "待上传/待填写"
    development_revision = prior_document.get("revision", -1)
    last_sync_at = prior_document.get("last_sync_at") or "待同步"
    out = [
        f"# {args.title}", "", "## 文档定位", "",
        "| 字段 | 内容 |", "|---|---|",
        "| PCTR 模式 | B |",
        f"| 来源策案 | {args.source_url or '待填写'} |",
        f"| 来源 Revision | {args.source_revision} |",
        f"| 本开发文档 | {development_url} |",
        f"| 本文档 Revision | {development_revision} |",
        f"| 项目根目录 | `{args.project_root}` |",
        f"| 策案版本 | `{args.planning_version}` |",
        f"| PCTR 版本目录 | `{args.artifact_root}` |",
        f"| 文档编码 | `{args.document_code}` |",
        f"| 本地状态清单 | `{args.state_out}` |",
        f"| SDD 工件根目录 | `{args.sdd_root}` |",
        f"| 实施计划根目录 | `{args.plan_root}` |",
        f"| Bug 记录根目录 | `{args.bug_root}` |",
        f"| 最后同步时间 | {last_sync_at} |", "",
        "> 本文档严格保持来源策案的功能标题、层级序号和顺序。功能编码格式为“策案层级序号-原功能编码”；本地文件统一放在 `.PCTR/<策案版本>/<功能编码>/`，A- 文件为策划确认快照与唯一功能拆解，B- 文件为详细 SDD 工件。", "",
        "## 功能总表", "",
        "| 功能编码 | 策案标题 | 策案标题路径 | 功能需求说明 | 工时 |",
        "|---|---|---|---|---|",
    ]
    for feature in features:
        fid = feature["feature_id"]
        prior = prior_by_path.get(feature["path"], {})
        work_hours = esc(str(prior.get("work_hours", "")))
        summary = effective_requirement_summary(feature, prior)
        out.append(
            f"| `{fid}` | {esc(feature['title'])} | {esc(feature['path'])} | "
            f"{esc(summary)} | {work_hours} |"
        )
    for feature in features:
        prior = prior_by_path.get(feature["path"], {})
        requirement_description = str(prior.get("requirement_description", "")).strip()
        paths = feature_artifact_paths(args, feature)
        local_sdd = prior.get("sdd_local_path", "") or paths["runtime_sdd"]
        attachment_name = prior.get("sdd_attachment_name", "")
        attachment_url = prior.get("sdd_attachment_url", "")
        if attachment_name and attachment_url:
            attachment_line = f"[Markdown 附件：{attachment_name}]({attachment_url})"
        elif attachment_name:
            attachment_line = f"Markdown 附件：{attachment_name}（已登记）"
        else:
            attachment_line = "Markdown 附件：待在飞书本功能章节内上传本地 `.md` 文件"
        status = prior.get("sdd_status", "") or "待生成"
        sdd_version = prior.get("sdd_version", "") or "待登记"
        status_revision = f"{status} / {sdd_version}"
        confirmation = prior.get("sdd_confirmation_status", "pending")
        confirmed_mark = "x" if confirmation == "confirmed" else " "
        ambiguous_mark = "x" if confirmation == "ambiguous" else " "
        plan_path = prior.get("implementation_plan_path", "")
        bug_paths = prior.get("bug_record_paths", [])
        bug_rows = [f"| {index} |  |  | `{path}` |" for index, path in enumerate(bug_paths, start=1)]
        while len(bug_rows) < 2:
            bug_rows.append(f"| {len(bug_rows) + 1} |  |  |  |")
        out += [
            "", "---", "", f"## {feature['feature_id']} {feature['title']}", "",
            f"> 策案标题路径：{feature['path']}", "",
            "### 1. 功能需求说明", "", requirement_description, "",
            "### 2. SDD确认文档", "",
            "> 🍞 本地 SDD 工件：", "", "`路径：`", "", "```text", local_sdd, "```", "",
            attachment_line, "", f"> 🏕️ SDD 状态 / Revision：{status_revision}", "",
            "> ✍️ 确认状态：", ">", f"> - [{confirmed_mark}] 已确认", f"> - [{ambiguous_mark}] 存在歧义需要修改", "",
            "### 3. 实施计划工件的路径", "",
            "`本地路径：`", "", "```text", plan_path, "```", "",
            "### 4. 功能 Bug 修复记录文件路径", "",
            "| 序号 | BUG内容 | 造成原因 |  |", "|---|---|---|---|", *bug_rows, "",
            "### 5. 优化建议", "", "- 由 SDD、ACSDM 与代码检索补充；不得改写来源策案事实。",
        ]
    return "\n".join(out).rstrip() + "\n"


def build_state(features: list[dict], args: argparse.Namespace, existing: dict) -> dict:
    old = {item.get("source_heading_path"): item for item in existing.get("features", [])}
    items = []
    for feature in features:
        prior = old.get(feature["path"], {})
        fingerprint = hashlib.sha256((feature["path"] + "\n" + feature["body"]).encode("utf-8")).hexdigest()
        requirement_description = str(prior.get("requirement_description", "")).strip()
        detail_fingerprint = hashlib.sha256(requirement_description.encode("utf-8")).hexdigest()
        legacy_external = list(prior.get("legacy_external_sdd_urls", []))
        if prior.get("sdd_feishu_url") and prior["sdd_feishu_url"] not in legacy_external:
            legacy_external.append(prior["sdd_feishu_url"])
        paths = feature_artifact_paths(args, feature)
        planner_prior = prior.get("planner_confirmation", {}) if isinstance(prior.get("planner_confirmation"), dict) else {}
        sdd_generation_prior = prior.get("sdd_generation", {}) if isinstance(prior.get("sdd_generation"), dict) else {}
        program_prior = prior.get("program_confirmation", {}) if isinstance(prior.get("program_confirmation"), dict) else {}
        decomposition_path = paths["decomposition"]
        planner_confirmation_path = paths["planner_confirmation_snapshot"]
        runtime_sdd_path = paths["runtime_sdd"]
        items.append({
            "feature_id": feature["feature_id"],
            "base_feature_id": feature["base_feature_id"],
            "legacy_feature_ids": feature["legacy_feature_ids"],
            "planning_sequence": feature["sequence"],
            "source_heading": feature["title"],
            "source_heading_path": feature["path"],
            "source_fingerprint": fingerprint,
            "feature_artifact_dir": paths["feature_artifact_dir"],
            "artifact_paths": {
                "planner_confirmation_snapshot": planner_confirmation_path,
                "decomposition": decomposition_path,
                "runtime_sdd": runtime_sdd_path,
            },
            "requirement_summary": effective_requirement_summary(feature, prior),
            "requirement_description": requirement_description,
            "requirement_detail_fingerprint": detail_fingerprint,
            "source_snapshot_path": decomposition_path,
            "source_snapshot_hash": prior.get("source_snapshot_hash", ""),
            "planner_confirmation": {
                "status": planner_prior.get("status", "missing"),
                "local_path": planner_confirmation_path,
                "feishu_url": planner_prior.get("feishu_url", ""),
                "document_revision": planner_prior.get("document_revision", -1),
                "must_answer_ambiguities": planner_prior.get("must_answer_ambiguities", []),
                "confirmation_items": planner_prior.get("confirmation_items", []),
                "resolved_decisions": planner_prior.get("resolved_decisions", []),
            },
            "decomposition_path": decomposition_path,
            "decomposition_hash": prior.get("decomposition_hash", ""),
            "sdd_generation": {
                "status": sdd_generation_prior.get("status", "locked"),
                "input_decomposition_path": decomposition_path,
                "output_sdd_path": runtime_sdd_path,
                "generated_by": sdd_generation_prior.get("generated_by", ""),
                "generated_at": sdd_generation_prior.get("generated_at", ""),
            },
            "program_confirmation": {
                "status": program_prior.get("status", "pending"),
                "reviewer": program_prior.get("reviewer", ""),
                "confirmed_at": program_prior.get("confirmed_at", ""),
                "open_items": program_prior.get("open_items", []),
            },
            "work_hours": prior.get("work_hours", ""),
            "sdd_local_path": prior.get("sdd_local_path", ""),
            "sdd_attachment_name": prior.get("sdd_attachment_name", ""),
            "sdd_attachment_token": prior.get("sdd_attachment_token", ""),
            "sdd_attachment_url": prior.get("sdd_attachment_url", ""),
            "sdd_attachment_document_revision": prior.get("sdd_attachment_document_revision", -1),
            "sdd_version": prior.get("sdd_version", ""),
            "legacy_external_sdd_urls": legacy_external,
            "sdd_status": prior.get("sdd_status", ""),
            "sdd_confirmation_status": prior.get("sdd_confirmation_status", "pending"),
            "implementation_plan_path": prior.get("implementation_plan_path", ""),
            "bug_record_paths": prior.get("bug_record_paths", []),
            "last_sync_at": prior.get("last_sync_at", ""),
        })
    prior_document = existing.get("development_document", {})
    return {
        "schema_version": 3,
        "mode": "B",
        "planning_version": args.planning_version,
        "document_code": args.document_code,
        "artifact_root": args.artifact_root,
        "source": {"url": args.source_url, "revision": args.source_revision},
        "development_document": {
            "url": prior_document.get("url", ""),
            "revision": prior_document.get("revision", -1),
            "local_path": args.out,
            "last_sync_at": prior_document.get("last_sync_at", ""),
        },
        "features": items,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("--out")
    parser.add_argument("--state-out")
    parser.add_argument("--document-code", required=True)
    parser.add_argument("--planning-version", help="PCTR version folder name, for example M032v1.2")
    parser.add_argument("--title", default="SDD 工件开发文档")
    parser.add_argument("--source-url", default="")
    parser.add_argument("--source-revision", type=int, default=-1)
    parser.add_argument("--project-root", default="")
    parser.add_argument("--feishu-parent-url", default="", help=argparse.SUPPRESS)
    parser.add_argument("--sdd-root")
    parser.add_argument("--plan-root")
    parser.add_argument("--bug-root")
    parser.add_argument("--existing-state")
    args = parser.parse_args()
    args.document_code = re.sub(r"[^A-Z0-9]+", "-", args.document_code.upper()).strip("-")
    if not args.document_code:
        raise SystemExit("document code is empty after normalization")
    project_root = Path(args.project_root).resolve() if args.project_root else Path.cwd().resolve()
    args.project_root = str(project_root)
    args.planning_version = normalize_planning_version(args.planning_version or args.document_code)
    artifact_root = project_root / ".PCTR" / args.planning_version
    args.artifact_root = str(artifact_root)
    args.out = args.out or str(artifact_root / f"{args.planning_version}-PCTR-B-development-document.md")
    args.state_out = args.state_out or str(artifact_root / f"{args.planning_version}-PCTR-B-state.json")
    args.sdd_root = args.sdd_root or str(artifact_root)
    args.plan_root = args.plan_root or str(artifact_root / "_plans")
    args.bug_root = args.bug_root or str(artifact_root / "_bugs")
    docs_root = (project_root / "docs").resolve()
    for label, value in (
        ("artifact root", args.artifact_root),
        ("document", args.out),
        ("state", args.state_out),
        ("SDD root", args.sdd_root),
        ("plan root", args.plan_root),
        ("bug root", args.bug_root),
    ):
        candidate = Path(value)
        resolved = candidate.resolve() if candidate.is_absolute() else (project_root / candidate).resolve()
        if resolved == docs_root or docs_root in resolved.parents:
            raise SystemExit(f"{label} must not be written under the Orange-owned docs directory: {resolved}")
    source = Path(args.source).read_text(encoding="utf-8-sig")
    features = parse_leaf_features(source)
    if not features:
        raise SystemExit("no leaf/source feature headings found")
    existing = load_existing(args.existing_state)
    assign_ids(features, args.document_code, existing)
    Path(args.artifact_root).mkdir(parents=True, exist_ok=True)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.state_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.plan_root).mkdir(parents=True, exist_ok=True)
    Path(args.bug_root).mkdir(parents=True, exist_ok=True)
    for feature in features:
        feature_artifact_dir(args, feature).mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(build_document(features, args, existing), encoding="utf-8")
    Path(args.state_out).write_text(json.dumps(build_state(features, args, existing), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"created {args.out}; state={args.state_out}; features={len(features)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
