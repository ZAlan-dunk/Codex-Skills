#!/usr/bin/env python3
"""Register OUF artifacts against one PCTR-B feature sidecar entry."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

TYPE_BUCKET = {
    "context-brief": "context_briefs",
    "sdd": "sdds",
    "plan": "plans",
    "report": "reports",
    "evidence": "evidence",
    "log": "logs",
    "bug-report": "evidence",
    "verification": "evidence",
    "other": "other",
}

FEATURE_RE = re.compile(r"\d+(?:\.\d+)*-[A-Z][A-Z0-9-]*-F\d{3}")
BASE_RE = re.compile(r"(?<![A-Z0-9-])([A-Z][A-Z0-9-]*-F\d{3})(?![A-Z0-9-])")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def infer_title(path: Path, text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def infer_type(path: Path) -> str:
    lower = str(path).replace("\\", "/").lower()
    if "brief" in lower or "context" in lower:
        return "context-brief"
    if "spec" in lower or "sdd" in lower:
        return "sdd"
    if "plan" in lower:
        return "plan"
    if "report" in lower:
        return "report"
    if "bug" in lower or "fix" in lower:
        return "bug-report"
    if "verify" in lower or "verification" in lower or "test" in lower or "qa" in lower:
        return "verification"
    if "evidence" in lower:
        return "evidence"
    if "log" in lower or "journal" in lower:
        return "log"
    return "other"


def resolve_feature(state: dict, requested: str) -> dict:
    matches = []
    for entry in state.get("features", []):
        identities = {entry.get("feature_id", ""), entry.get("base_feature_id", ""), *entry.get("legacy_feature_ids", [])}
        if requested in identities:
            matches.append(entry)
    if len(matches) != 1:
        raise SystemExit(f"feature identity matched {len(matches)} entries: {requested}")
    return matches[0]


def artifact_entry(path: Path, artifact_type: str, title: str, status: str, source: str) -> dict:
    text = read_text(path) if path.is_file() else ""
    return {
        "type": artifact_type,
        "path": str(path),
        "title": title or infer_title(path, text),
        "status": status,
        "hash": sha256(path) if path.is_file() else "",
        "created_at": datetime.fromtimestamp(path.stat().st_ctime, timezone.utc).isoformat() if path.is_file() else "",
        "updated_at": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat() if path.is_file() else "",
        "source": source,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("state")
    parser.add_argument("--feature", required=True)
    parser.add_argument("--artifact", action="append", required=True, help="OUF artifact path; repeatable")
    parser.add_argument("--type", choices=sorted(TYPE_BUCKET), default="", help="override artifact type for all --artifact paths")
    parser.add_argument("--title", default="")
    parser.add_argument("--status", default="Draft")
    parser.add_argument("--artifact-root", default="docs/forge-artifacts")
    parser.add_argument("--source", default="OUF")
    parser.add_argument("--out-state", required=True)
    args = parser.parse_args()

    state_path = Path(args.state)
    state = json.loads(state_path.read_text(encoding="utf-8-sig"))
    if state.get("schema_version") not in (2, 3) or state.get("mode") != "B":
        raise SystemExit("state schema/mode is not PCTR-B")
    feature = resolve_feature(state, args.feature)
    store = feature.setdefault("ouf_artifacts", {
        "artifact_root": args.artifact_root,
        "context_briefs": [],
        "sdds": [],
        "plans": [],
        "reports": [],
        "evidence": [],
        "logs": [],
        "other": [],
        "last_linked_at": "",
        "linked_by": "ACSDM OUF Link Index",
    })
    store.setdefault("artifact_root", args.artifact_root)
    for bucket in TYPE_BUCKET.values():
        store.setdefault(bucket, [])

    now = datetime.now(timezone.utc).isoformat()
    for raw in args.artifact:
        path = Path(raw)
        if not path.is_file():
            raise SystemExit(f"artifact not found: {path}")
        text = read_text(path)
        identities = {feature.get("feature_id", ""), feature.get("base_feature_id", ""), *feature.get("legacy_feature_ids", [])}
        file_identity_text = str(path) + "\n" + text
        found_full = set(FEATURE_RE.findall(file_identity_text))
        found_base = set(BASE_RE.findall(file_identity_text))
        if identities.isdisjoint(found_full | found_base):
            raise SystemExit(f"artifact does not mention the selected feature identity: {path}")
        artifact_type = args.type or infer_type(path)
        entry = artifact_entry(path, artifact_type, args.title, args.status, args.source)
        bucket = TYPE_BUCKET[artifact_type]
        existing = [item for item in store[bucket] if item.get("path") != str(path)]
        existing.append(entry)
        store[bucket] = existing

    store["last_linked_at"] = now
    store["linked_by"] = "register_pctr_b_ouf_artifact.py / ACSDM OUF Link Index"
    feature["last_sync_at"] = now
    Path(args.out_state).write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"registered {len(args.artifact)} OUF artifact(s) for {feature['feature_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
