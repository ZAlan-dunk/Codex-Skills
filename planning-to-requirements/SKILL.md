---
name: planning-to-requirements
description: Convert Feishu Wiki/Docx planning documents, product proposals, game design plans, version plans, and requirement drafts into exhaustive development-ready requirement specifications and a paired planning-confirmation/acceptance document. Use when an Agent must preserve source order, split broad items into atomic functions, retrieve project rules through ACSDM, collect ambiguity for planners, synchronize confirmed decisions back by feature ID, route confirmed features to default ABC, enhanced ABC, or SDD, start development planning by feature ID, submit features for planning acceptance, process failed acceptance and bug loops, and mark accepted features complete.
---

# Planning to Requirements

## Purpose

Manage the full lifecycle from planning source to confirmed requirements, technical planning, implementation handoff, planning acceptance, bug correction, and completion. Never let an Agent silently decide unresolved planning behavior.

## Required Reading

Before creating or updating documents, read:

1. `references/workflow.md`
2. `references/feature-decomposition.md`
3. `references/output-schema.md`
4. `references/acsdm-integration.md`
5. `references/complexity-routing.md`
6. `references/feature-lifecycle.md`
7. `references/planning-confirmation-workflow.md`
8. `references/planning-acceptance-workflow.md`
9. `references/command-contract.md`
10. `references/quality-checklist.md`

Read `references/update-monitoring.md` for revision comparison, monitoring, incremental synchronization, or concurrent document edits.

## Documents

Create and maintain two paired documents:

1. **Requirement development document**: technical source of truth for detailed requirements, route, project evidence, plan/development state, and completion state.
2. **Planning confirmation and acceptance document**: human source of truth for planner decisions, ambiguity resolution, acceptance points, acceptance rounds, and bug descriptions.

Use stable feature IDs across both documents. Record document IDs, revisions, links, and last synchronization time.

## Core Workflow

1. Read and normalize the planning source, preserving headings, tables, media, deletion marks, and source revision.
2. Split level-one features into atomic functions with stable IDs.
3. Retrieve ACSDM evidence where a project root is available. Separate planning facts, project rules, code facts, recommendations, and unresolved questions.
4. Score and pre-route each function to default ABC, enhanced ABC, or SDD.
5. Create the requirement development document with detailed requirements and a locked task capsule.
6. Extract blocking and non-blocking planning questions and create the paired planning confirmation and acceptance document. Give every feature a short planner-readable implementation description.
7. Keep formal plan generation locked until all blocking questions are confirmed and the user explicitly issues a planning-confirmation synchronization command.
8. On confirmation, synchronize the final planner wording and source revision back to the requirement document, recalculate scope and route, regenerate the task capsule, and set `planning_confirmation_status=confirmed`.
9. On `开始 <FEATURE-ID> 功能开发`, read the confirmed requirement, planner decision, ACSDM catalog, and code evidence; generate a detailed plan according to the selected route. Do not modify code.
10. On `开始实施 <FEATURE-ID>`, implement only an approved plan and follow the ACSDM authorization/recording rules.
11. On `提交 <FEATURE-ID> 策划验收`, copy planner-readable acceptance points and implementation submission metadata into the acceptance section.
12. On acceptance failure, record the failed points and planner bug description, set the feature to bug-fix state, retrieve ACSDM/code evidence, and generate a first analysis. Do not mark complete.
13. On re-submission, preserve earlier rounds and create a new acceptance round.
14. Only after the explicit command `<FEATURE-ID> 策划已验收（任务完毕）` and successful validation may the requirement document be marked `功能已完成`.

## Confirmation Gate

Before formal ABC/SDD generation, require:

- all blocking confirmation items resolved;
- a planner confirmation summary;
- confirmation source document ID and revision;
- explicit user synchronization/confirmation command;
- `planning_confirmation_status=confirmed`.

Unconfirmed features may be inspected through ACSDM or code, but may not receive a final plan, implementation, or completion status.

## Command Semantics

- `生成策划确认文档`: create the paired confirmation/acceptance document.
- `同步策划确认 <FEATURE-ID>` or `<FEATURE-ID> 策划已确认`: validate blocking items, synchronize decisions, recalculate route, and unlock planning.
- `开始 <FEATURE-ID> 功能开发`: generate the detailed technical plan only.
- `开始实施 <FEATURE-ID>`: execute an approved plan.
- `提交 <FEATURE-ID> 策划验收`: enter planner acceptance and populate the current round.
- `<FEATURE-ID> 验收失败存在Bug：...`: create/update bug analysis and set bug-fix state.
- `<FEATURE-ID> 重新提交策划验收`: create a new acceptance round.
- `<FEATURE-ID> 策划已验收（任务完毕）`: validate all required acceptance points and mark complete.

Follow `references/command-contract.md`; do not infer a state-changing command from casual discussion.

## Route Rules

- Default ABC: small, local, low-risk work.
- Enhanced ABC: moderate work inside existing architecture requiring explicit state, files, regression, and rollback.
- SDD: hard triggers or high complexity such as migration, public framework changes, three or more modules, complex state machines, external SDKs, global locking/concurrency, or high-cost ambiguity.

Planning confirmation precedes every final route. SDD still requires ACSDM retrieval first.

## Acceptance Rules

- Technical verification, QA testing, and planning acceptance are distinct.
- Partial acceptance cannot complete a feature.
- Failed acceptance must preserve the failed round, bug description, analysis, fix record, and re-test result.
- Completion requires planner confirmation, an approved plan, implementation submission, all mandatory planning acceptance points passed, no open blocking bugs, and an explicit completion command.

## Ambiguity Policy

Classify unresolved items as `待策划确认`, `待技术确认`, `待美术确认`, `待音频确认`, or `待平台确认`. Mark each planning item as blocking or non-blocking. Never invent values, persistence rules, priorities, assets, APIs, or framework capabilities.

## Resources

Use templates in `assets/` and deterministic scripts in `scripts/`. Run the document and dual-document validators before delivery or completion-state changes.

## Common Failures

- Do not treat document editing as explicit planner confirmation.
- Do not generate a final ABC/SDD plan for an unconfirmed feature.
- Do not let acceptance failure overwrite earlier acceptance rounds.
- Do not mark code-complete as planning-accepted.
- Do not mark planning-accepted as feature-complete without the explicit completion command.
- Do not overwrite planner-entered confirmation or acceptance fields during synchronization.
- Do not renumber stable feature IDs; create child IDs when confirmed scope requires splitting.
