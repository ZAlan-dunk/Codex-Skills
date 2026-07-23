#!/usr/bin/env python3
"""Validate PCTR-B document/sidecar identity and confirmation state."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

FEATURE_RE = re.compile(r"^##\s+(\d+(?:\.\d+)*-[A-Z][A-Z0-9-]*-F\d{3})\s+(.+)$", re.M)
BASE_RE = re.compile(r"^[A-Z][A-Z0-9-]*-F\d{3}$")
ALLOWED = {"pending", "confirmed", "ambiguous"}
PLANNER_ALLOWED = {"missing", "pending", "confirmed", "needs_revision"}
PLANNER_ITEM_RE = re.compile(r"^###\s+([A-Z0-9][A-Z0-9_.-]*-(?:A|C)\d+)\b.*$", re.M)
PLANNER_OPTION_RE = re.compile(r"^-\s+([A-Z])[:：]\s*(\S.*)$", re.M)
PLANNER_RECOMMENDATION_RE = re.compile(r"^推荐选择[:：]\s*([A-Z])(?:\s|[:：（(]|$)", re.M)
PLANNER_REASON_RE = re.compile(r"^推荐原因[:：]\s*(\S.*)$", re.M)
PLANNER_REPLY_RE = re.compile(
    r"```text\s*\r?\n选择[:：]([^\r\n]*)\r?\n补充[:：]([^\r\n]*)\r?\n```",
    re.M,
)


def checked(body: str, label: str) -> bool:
    match = re.search(rf"^\s*>?\s*- \[([ xX])\] {re.escape(label)}\s*$", body, re.M)
    return bool(match and match.group(1).lower() == "x")


def requirement_description(body: str) -> str:
    match = re.search(
        r"^### 1\. 功能需求说明\s*$([\s\S]*?)(?=^### 2\. SDD确认文档\s*$)",
        body,
        re.M,
    )
    return match.group(1).strip() if match else ""


def validate_planner_confirmation(
    path: Path,
    planner: dict,
    feature_id: str,
    errors: list[str],
) -> None:
    text = path.read_text(encoding="utf-8-sig")
    matches = list(PLANNER_ITEM_RE.finditer(text))
    actual_ids = [match.group(1) for match in matches]
    expected_ids = list(planner.get("must_answer_ambiguities", [])) + list(
        planner.get("confirmation_items", [])
    )
    if actual_ids != expected_ids:
        errors.append(f"{feature_id}: planner confirmation item order/IDs differ from sidecar")

    must_answer = set(planner.get("must_answer_ambiguities", []))
    planner_status = planner.get("status", "missing")
    for index, match in enumerate(matches):
        item_id = match.group(1)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end():end]
        options = PLANNER_OPTION_RE.findall(body)
        option_codes = [code for code, _ in options]
        if not 2 <= len(options) <= 6:
            errors.append(f"{feature_id}/{item_id}: planner item must have 2-6 options")
        expected_codes = [chr(ord("A") + offset) for offset in range(len(option_codes))]
        if option_codes != expected_codes:
            errors.append(f"{feature_id}/{item_id}: option codes must be consecutive from A")

        recommendation = PLANNER_RECOMMENDATION_RE.search(body)
        if not recommendation or recommendation.group(1) not in option_codes:
            errors.append(f"{feature_id}/{item_id}: recommended choice must name a listed option")
        if not PLANNER_REASON_RE.search(body):
            errors.append(f"{feature_id}/{item_id}: recommendation reason is missing")

        reply = PLANNER_REPLY_RE.search(body)
        if not reply:
            errors.append(f"{feature_id}/{item_id}: exact two-line reply block is missing")
            continue
        choice = reply.group(1).strip().upper()
        supplement = reply.group(2).strip()
        if choice and choice not in option_codes:
            errors.append(f"{feature_id}/{item_id}: reply selection is not one listed option code")
        unanswered = not choice and not supplement
        if planner_status == "confirmed" and item_id in must_answer and unanswered:
            errors.append(f"{feature_id}/{item_id}: confirmed planner state has unanswered must-answer item")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("document")
    parser.add_argument("state")
    args = parser.parse_args()
    text = Path(args.document).read_text(encoding="utf-8-sig")
    state = json.loads(Path(args.state).read_text(encoding="utf-8-sig"))
    errors = []
    if state.get("schema_version") not in (2, 3) or state.get("mode") != "B":
        errors.append("state schema/mode must be 2/B or 3/B")
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
        sequence = item.get("planning_sequence", "")
        base_id = item.get("base_feature_id", "")
        if not re.fullmatch(r"\d+(?:\.\d+)*", sequence):
            errors.append(f"{feature_id}: invalid planning sequence")
        if not BASE_RE.fullmatch(base_id):
            errors.append(f"{feature_id}: invalid base feature ID")
        if feature_id != f"{sequence}-{base_id}":
            errors.append(f"{feature_id}: full ID does not equal sequence-base ID")
        aliases = item.get("legacy_feature_ids", [])
        if not isinstance(aliases, list) or base_id not in aliases:
            errors.append(f"{feature_id}: legacy aliases must include base feature ID")
        if state.get("schema_version") == 3:
            planning_version = state.get("planning_version", "")
            artifact_root = Path(str(state.get("artifact_root", "")))
            feature_dir = Path(str(item.get("feature_artifact_dir", "")))
            paths = item.get("artifact_paths") or {}
            expected_dir = artifact_root / feature_id
            artifact_parts = artifact_root.parts
            if not planning_version or len(artifact_parts) < 2 or artifact_parts[-2:] != (".PCTR", planning_version):
                errors.append(f"{feature_id}: invalid PCTR v3 planning_version/artifact_root")
            if feature_dir != expected_dir or feature_dir.name != feature_id:
                errors.append(f"{feature_id}: feature_artifact_dir must be .PCTR/<planning-version>/<feature_id>")
            expected_files = {
                "planner_confirmation_snapshot": feature_dir / "A-01-planner-confirmation-snapshot.md",
                "decomposition": feature_dir / "A-02-feature-decomposition.md",
                "runtime_sdd": feature_dir / "B-01-runtime-sdd.md",
            }
            for key, expected_path in expected_files.items():
                if Path(str(paths.get(key, ""))) != expected_path:
                    errors.append(f"{feature_id}: artifact_paths.{key} must be {expected_path}")
            if Path(str((item.get("planner_confirmation") or {}).get("local_path", ""))) != expected_files["planner_confirmation_snapshot"]:
                errors.append(f"{feature_id}: planner confirmation path must be A-01")
            planner = item.get("planner_confirmation") or {}
            if planner.get("feishu_url") or planner.get("document_url"):
                errors.append(f"{feature_id}: separate Feishu planner-confirmation document is forbidden")
            planner_status = planner.get("status", "missing")
            if planner_status not in PLANNER_ALLOWED:
                errors.append(f"{feature_id}: invalid planner confirmation status {planner_status}")
            if planner_status != "missing":
                if planner.get("attachment_name") != "A-01-planner-confirmation-snapshot.md":
                    errors.append(f"{feature_id}: planner confirmation attachment must be A-01-planner-confirmation-snapshot.md")
                if not planner.get("attachment_token") or not planner.get("attachment_block_id"):
                    errors.append(f"{feature_id}: planner confirmation attachment token/block identity missing")
                if planner.get("attachment_feature_id") != feature_id:
                    errors.append(f"{feature_id}: planner confirmation attachment feature identity differs")
                if not planner.get("attachment_heading_block_id"):
                    errors.append(f"{feature_id}: planner confirmation target SDD heading block is missing")
                if int(planner.get("attachment_document_revision", -1)) < 0:
                    errors.append(f"{feature_id}: planner confirmation containing-document revision missing")
                if not expected_files["planner_confirmation_snapshot"].is_file():
                    errors.append(f"{feature_id}: local A-01 planner confirmation file is missing")
                else:
                    validate_planner_confirmation(
                        expected_files["planner_confirmation_snapshot"],
                        planner,
                        feature_id,
                        errors,
                    )
            if Path(str(item.get("decomposition_path", ""))) != expected_files["decomposition"]:
                errors.append(f"{feature_id}: decomposition_path must be A-02")
            if Path(str((item.get("sdd_generation") or {}).get("output_sdd_path", ""))) != expected_files["runtime_sdd"]:
                errors.append(f"{feature_id}: SDD output path must be B-01")
            if item.get("sdd_local_path") and Path(str(item.get("sdd_local_path"))) != expected_files["runtime_sdd"]:
                errors.append(f"{feature_id}: sdd_local_path must be the B-01 runtime SDD path")
        if not item.get("requirement_summary") or not item.get("requirement_detail_fingerprint"):
            errors.append(f"{feature_id}: requirement summary/detail fingerprint missing")
        document_description = requirement_description(body)
        state_description = str(item.get("requirement_description", "")).strip()
        if document_description != state_description:
            errors.append(f"{feature_id}: requirement description differs between document and sidecar")
        expected_fingerprint = hashlib.sha256(document_description.encode("utf-8")).hexdigest()
        if item.get("requirement_detail_fingerprint") != expected_fingerprint:
            errors.append(f"{feature_id}: requirement detail fingerprint differs")
        status = item.get("sdd_confirmation_status")
        if status not in ALLOWED:
            errors.append(f"{feature_id}: invalid confirmation status {status}")
            continue
        yes = checked(body, "已确认")
        no = checked(body, "存在歧义需要修改")
        expected = {"pending": (False, False), "confirmed": (True, False), "ambiguous": (False, True)}[status]
        if (yes, no) != expected:
            errors.append(f"{feature_id}: checkbox state does not match sidecar status")
        attachment_name = str(item.get("sdd_attachment_name", "")).strip()
        attachment_token = str(item.get("sdd_attachment_token", "")).strip()
        attachment_url = str(item.get("sdd_attachment_url", "")).strip()
        attachment_revision = int(item.get("sdd_attachment_document_revision", -1))
        has_attachment_metadata = bool(
            attachment_name
            or attachment_token
            or attachment_url
            or attachment_revision >= 0
        )
        if has_attachment_metadata:
            if attachment_name != "B-01-runtime-sdd.md":
                errors.append(f"{feature_id}: SDD attachment name must be B-01-runtime-sdd.md")
            if not attachment_token and not attachment_url:
                errors.append(f"{feature_id}: SDD attachment token or URL is missing")
            if attachment_revision < 0:
                errors.append(f"{feature_id}: SDD containing-document revision is missing")
        if status == "confirmed" and not item.get("sdd_local_path"):
            errors.append(f"{feature_id}: confirmed without current local Markdown identity")
        if status == "confirmed" and item.get("sdd_status") != "Approved":
            errors.append(f"{feature_id}: confirmed SDD status must be Approved")
        if status == "confirmed" and not item.get("sdd_version"):
            errors.append(f"{feature_id}: confirmed SDD version is missing")
    if errors:
        print("INVALID")
        for error in errors:
            print("-", error)
        return 1
    print(f"VALID: PCTR-B document/state features={len(document_items)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
