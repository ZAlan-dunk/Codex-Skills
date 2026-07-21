# Orange SDD to PCTR-B Handoff

## Boundary

Orange Unity Forge and PCTR may coexist when independently enabled. Prefer direct post-generation handoff in the same task. A completed Markdown artifact remains the stable boundary and also supports cross-turn fallback.

## Pre-Generation Feature Lookup

PCTR-B must create and register its local document/sidecar and Feishu development document before Orange generation. When both suites are active, Orange calls `pctr-b-feature-lookup-interface.md` with the source planning identity and exact heading path. Continue only when PCTR-B returns one exact lookup receipt.

Use the receipt, not a user-typed title or filename, as the authority for Feature ID, exact title, source heading path/revision, development-document link, and Feishu SDD target. Zero/multiple matches or stale source identity stop before generation.

## Required SDD Identity

The role-based SDD must contain:

- exact PCTR Feature ID;
- exact feature title;
- exact source planning heading path;
- source planning URL/token and revision;
- PCTR-B Feishu development-document URL/token;
- SDD status (`Draft`, `In Review`, or `Approved`);
- SDD template version;
- role sections for planner, program, QA, risk, rollback, and pending decisions.

Preferred filename:

```text
YYYY-MM-DD-<feature-id-lowercase>-<slug>-sdd.md
```

Identity comes from metadata, not filename-only matching.

## Upload Contract

The manual PCTR-B path uses `同步PCTR-B SDD <FEATURE-ID>`. When both suites are active and Orange generated the SDD from a valid lookup receipt, Orange automatically performs the same upload/link-back operation immediately after successful SDD validation.

The upload workflow may:

1. read the matched local Markdown;
2. validate it;
3. create a Feishu Docx using the `lark-doc` Markdown creation/import path;
4. place it under the configured Feishu feature/document parent when available;
5. update the PCTR-B development document with the local path and Feishu URL;
6. update the sidecar revision and synchronization metadata.

Automatic Orange handoff must leave confirmation pending. Upload does not equal planner confirmation.

If the target Feishu parent is missing or ambiguous, stop before upload and request the location. Do not upload to an arbitrary personal root.

## Confirmation Contract

Upload does not equal confirmation.

- Draft or In Review SDDs may be uploaded, but plan generation stays locked.
- `SDD已确认` requires a current uploaded revision and no blocking pending decision.
- `SDD存在歧义需要修改` records ambiguity and keeps the feature locked.
- A revised SDD creates a new Feishu revision or replaces the generated body according to the active lark-doc update workflow; never silently overwrite planner-entered notes.

## Implementation Plan Contract

The implementation plan remains a local artifact path in PCTR-B. Do not auto-upload it. After successful development, program staff may upload it manually and update the path/link when explicitly requested.
