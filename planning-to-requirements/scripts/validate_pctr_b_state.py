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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("document")
    parser.add_argument("state")
    args = parser.parse_args()
    text = Path(args.document).read_text(encoding="utf-8-sig")
    state = json.loads(Path(args.state).read_text(encoding="utf-8-sig"))
    errors = []
    if state.get("schema_version") != 2 or state.get("mode") != "B":
        errors.append("state schema/mode must be 2/B")
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
        has_attachment = bool(item.get("sdd_attachment_token") or item.get("sdd_attachment_url"))
        if status == "confirmed" and (
            not item.get("sdd_local_path")
            or not has_attachment
            or int(item.get("sdd_attachment_document_revision", -1)) < 0
        ):
            errors.append(f"{feature_id}: confirmed without local Markdown attachment identity/revision")
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
