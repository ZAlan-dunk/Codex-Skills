---
name: acsdm-project-catalog
description: Use when working in a project that should keep its ACSDM Markdown knowledge catalog directly under the project root .ACSDM folder, or when a request mentions project rules, conventions, related docs, review, implementation records, PCTR feature IDs, planning-confirmed requirements, starting feature development, implementation, planning acceptance submission, acceptance-failed bugs, re-submission, completion recording, or commands like 查阅相关文档, 开始 FEATURE-ID 功能开发, 开始实施, 验收失败存在Bug, 策划已验收（任务完毕）并记录.
---

# ACSDM Project Catalog

## Overview

Use ACSDM to manage a project-local directory-style Markdown knowledge catalog. The catalog root is always `<project root>/.ACSDM`.

Core principle: the project-local `.ACSDM` folder is the source of truth. Read indexes first, read only task-relevant documents, and do not modify project files or catalog documents until the user's intent is clear and authorized.

## Quick Workflow

1. Check `<project root>/.ACSDM`.
2. If `.ACSDM` is missing, report it. Initialize only when the user explicitly requests initialization or authorizes catalog edits; never initialize it silently during an unrelated task.
3. If `.ACSDM` exists, read `.ACSDM/0000ACSDMRootIndex.md` first. If the root index is missing, inspect folder and Markdown filenames only, report the repair need, and create it only after explicit authorization.
4. After reading the root index, verify the standard folders and module indexes. Repair only authorized missing structure.
5. Match the request to modules using `references/retrieval-policy.md`.
6. Read the selected module index, then only the Markdown files directly relevant to the task.
7. If the request mentions rules, conventions, framework behavior, Lua/C# interaction, UI framework, popups, Excel import/export, or “按照规范”, read `00Rule` before implementation work.
8. For larger or ambiguous requests, present A/B/C review sections and wait for explicit authorization before editing files.
9. After authorized implementation, update ACSDM only when the user also requests recording. Prefer an existing relevant document; create a new one only when the user says “开始实施并记录” or otherwise confirms creation.

Do not use an external folder as the live catalog root. External document folders can be scanned or migrated only when the user explicitly asks and approval allows access.

## Planning Gate

Small requests can proceed directly when they are low-risk and specific: read one document, find one method, change one explicit field, or answer a narrow question.

For a new feature, cross-file change, unclear module, unclear rule, or a request longer than about 30 Chinese characters that is not obviously tiny, present:

```markdown
## A. 实现方案

A1. ...

## B. 需要改动的部分

B1. ...

## C. 歧义点与待校准

C1. ...
```

Do not edit project files or ACSDM documents until the user says an explicit authorization phrase such as `开始实施`, `允许`, `可以执行`, `开始吧`, or `按方案做`.

Reading indexes, reporting missing structure, and preparing a proposed repair are read-only. Creating or repairing `.ACSDM`, its folders, or its indexes counts as an edit and requires the same authorization gate unless initialization/repair was the user's explicit request.

## Recording Rules

When the user says `开始实施`, implement the approved project change. Do not update ACSDM merely because implementation started.

When the user says `开始实施并记录`, update the most relevant existing ACSDM document and its module index. If no relevant document exists, create a new Markdown document using the next two-digit sequence number, then update the module index and root index.

If no module matches, ask whether to create a new module or which existing module should receive the record.

Every implementation record should include the request summary, final A/B/C decisions, changed files, related scripts, methods, line numbers, verification commands/results, risks, rollback notes, and timestamp.

## Resources

Read these references only when needed:

- `references/retrieval-policy.md`: trigger words, module matching, context reuse, and rule-first behavior.
- `references/index-schema.md`: standard folders, root index, and module index fields.
- `references/document-template.md`: human-readable Markdown document template with YAML metadata.
- `references/usage-guide.md`: installation, project initialization, testing, sharing, and modification instructions.

Use these scripts when deterministic filesystem operations are helpful:

- `scripts/acsdm-init.ps1`: initialize or repair project-local `.ACSDM`, create standard folders/indexes, and exclude `.ACSDM/` locally from git when possible.
- `scripts/acsdm-scan.ps1`: scan folder and Markdown filenames without reading document bodies.
- `scripts/acsdm-update-index.ps1`: regenerate root and module indexes from filenames and timestamps.

## PCTR Feature Lifecycle Integration

When a request uses a PCTR feature ID or lifecycle command:

1. Read the PCTR requirement feature section and verify the stable feature ID.
2. For plan generation, require `planning_confirmation_status=confirmed` and read the synchronized planner summary.
3. Read the ACSDM root index, then `00Rule` for rule-first triggers, matching module indexes, directly relevant documents, and referenced code.
4. `开始 <FEATURE-ID> 功能开发` means generate a route-appropriate detailed plan only; do not edit code.
5. `开始实施 <FEATURE-ID>` requires an approved plan and explicit implementation authorization.
6. For `<FEATURE-ID> 验收失败存在Bug`, read the failed planner acceptance IDs, planner description, confirmed requirement, implementation record, relevant rules, logs, and code; produce first analysis before edits.
7. Preserve acceptance rounds and bug IDs. Do not mark completion after failed or partial acceptance.
8. `<FEATURE-ID> 策划已验收（任务完毕）` synchronizes status only. Create/update an ACSDM record only when the command includes `并记录` or the user separately requests recording.

Every PCTR-linked implementation record should include the feature ID, confirmed requirement revision, planning confirmation source, route, approved plan, changed files/methods/lines, verification evidence, planning acceptance rounds, bugs, rollback, and final acceptance result.
## Common Mistakes

- Do not store only a JSON pointer in `.ACSDM`; `.ACSDM` itself must contain the catalog folders and indexes.
- Do not use an external notes folder as the live catalog root unless the user explicitly requests a one-off scan or migration.
- Do not read every Markdown document in the catalog to “understand the project”. Read indexes first.
- Do not write `.ACSDM/` to project `.gitignore` unless the user explicitly asks. Prefer `.git/info/exclude` when the project is a valid git repository.
- Do not create new ACSDM documents for every task. Update existing relevant documents unless the user asks to record a new document.
- Do not bypass the A/B/C planning gate for broad feature requests.
