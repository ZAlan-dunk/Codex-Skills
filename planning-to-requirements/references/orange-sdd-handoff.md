# Orange SDD to PCTR-B Handoff

## Boundary

Orange Unity Forge and PCTR may coexist when independently enabled. Prefer direct post-generation handoff in the same task. A completed Markdown artifact remains the stable boundary and also supports cross-turn fallback.

## Pre-Generation Feature Lookup

PCTR-B must create and register its local document/sidecar and Feishu development document before Orange generation. When both suites are active, Orange calls `pctr-b-feature-lookup-interface.md` with the source planning identity and exact heading path. Continue only when PCTR-B returns one exact lookup receipt.

Use the receipt, not a user-typed title or filename, as the authority for full/base Feature IDs, planning sequence, exact title, source heading path/revision, and development-document link. Zero/multiple matches or stale source identity stop before generation.

## Required SDD Identity

The role-based SDD must contain:

- exact PCTR Feature ID;
- exact PCTR base Feature ID and planning sequence;
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

## Markdown Attachment Contract

The manual PCTR-B path uses `同步PCTR-B SDD <FEATURE-ID>`. When both suites are active and Orange generated the SDD from a valid lookup receipt, Orange may perform the same attachment/link-back operation immediately after successful SDD validation.

The attachment workflow may:

1. read the matched local Markdown;
2. validate it;
3. insert the local `.md` file itself as an attachment directly inside the matching feature section when exact-position insertion can be verified;
4. update the PCTR-B development document with the local path, attachment reference, status/version, and confirmation blocks;
5. update the sidecar attachment identity, containing-document revision, and synchronization metadata.

Automatic Orange handoff must leave confirmation pending. Attachment does not equal planner confirmation.

If exact-position attachment or the required callout formatting cannot be verified, stop before external write and return a manual-upload handoff. Never create a separate Feishu SDD Docx and never append the file to an unrelated position.

## Confirmation Contract

Attachment does not equal confirmation.

- Draft or In Review SDDs may be attached, but plan generation stays locked.
- `SDD已确认` requires a current local Markdown identity, attachment reference, containing-document revision, and no blocking pending decision.
- `SDD存在歧义需要修改` records ambiguity and keeps the feature locked.
- A revised SDD replaces or adds a new file attachment snapshot inside the same feature section and advances the containing document revision; never silently overwrite planner-entered notes.

## Implementation Plan Contract

The implementation plan remains a local artifact path in PCTR-B. Do not auto-upload it. After successful development, program staff may upload it manually and update the path/link when explicitly requested.
