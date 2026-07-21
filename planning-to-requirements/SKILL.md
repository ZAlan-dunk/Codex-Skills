---
name: planning-to-requirements
description: Convert Feishu Wiki/Docx planning documents and game-design plans into development-ready requirements through one of two strict modes. PCTR-A preserves the legacy paired requirement plus planning-confirmation/acceptance workflow with atomic decomposition and multi-block interaction. PCTR-B preserves the planning document heading order, creates one concise development document, attaches one role-based SDD confirmation document per feature, records local implementation-plan and bug-fix artifact paths, and synchronizes approved SDDs to Feishu. Use for planning-source conversion, stable feature IDs, ACSDM-backed evidence, SDD handoff, plan/implementation gates, acceptance, and bug lifecycle work.
---

# Planning to Requirements

## PJ032 Activation Gate

Before using this Skill in PJ032, read `<project root>/.codex/skill-gates.json`. Continue only when `pctr=true` and `pctr_mode` is `A` or `B`.

Exact standalone activation commands:

- `启用 PCTR` or `启用PCTR-A`: enable backward-compatible Mode A.
- `启用PCTR-B`: enable Mode B.

Never infer or switch modes from document shape, conversation wording, an SDD path, or a Feature ID. PCTR may coexist with ACSDM and Orange Unity Forge when each gate is independently enabled. Reject a missing/invalid `pctr_mode` instead of guessing.

When Orange and PCTR-B are both active, first use the read-only feature identity contract in `references/pctr-b-feature-lookup-interface.md`, then use the upload/link-back contract in `references/pctr-b-handoff-interface.md`. While Orange is active and PCTR is disabled, the upload interface defines a narrow fallback for an SDD that already contains an exact Feature ID obtained from an earlier active PCTR-B session. It does not activate PCTR-B or authorize lookup or any other PCTR behavior.

## Purpose

Manage the full lifecycle from planning source to confirmed requirements, technical planning, implementation handoff, planning acceptance, bug correction, and completion. Never let an Agent silently decide unresolved planning behavior. Keep PCTR-A and PCTR-B documents and state contracts separate.

## Mode Selection

Read `references/mode-routing.md` first.

- **PCTR-A**: use the existing planning source → requirement development document → planning confirmation/acceptance document chain. Preserve atomic decomposition, paired revisions, confirmation IDs, acceptance rounds, and multi-block interaction.
- **PCTR-B**: use planning source → one concise requirement development document. Preserve source heading order and exact titles; treat each leaf/small heading as one feature, or a large heading as the feature when it has no child heading. Attach one uploaded role-based SDD per feature. Keep machine state in a local sidecar manifest rather than visible status columns.

Do not convert an existing document between modes in place. Generate a new document and preserve the old document as a superseded source when migration is explicitly requested.

## Required Reading

Before creating or updating documents, always read:

1. `references/mode-routing.md`
2. `references/acsdm-integration.md`
3. `references/complexity-routing.md`
4. `references/feature-lifecycle.md`
5. `references/command-contract.md`
6. `references/quality-checklist.md`

For PCTR-A, additionally read:

1. `references/workflow.md`
2. `references/feature-decomposition.md`
3. `references/output-schema.md`
4. `references/planning-confirmation-workflow.md`
5. `references/planning-acceptance-workflow.md`

For PCTR-B, additionally read:

1. `references/pctr-b-workflow.md`
2. `references/pctr-b-output-schema.md`
3. `references/pctr-b-feature-lookup-interface.md` when Orange needs the exact feature identity
4. `references/orange-sdd-handoff.md`
5. `references/pctr-b-handoff-interface.md` when Orange requests automatic post-generation upload

Read `references/update-monitoring.md` for revision comparison, monitoring, incremental synchronization, or concurrent document edits.

## Documents

PCTR-A creates and maintains two paired documents:

1. **Requirement development document**: technical source of truth for detailed requirements, route, project evidence, plan/development state, and completion state.
2. **Planning confirmation and acceptance document**: human source of truth for planner decisions, ambiguity resolution, acceptance points, acceptance rounds, and bug descriptions.

Use stable feature IDs across both documents. Record document IDs, revisions, links, and last synchronization time.

PCTR-B creates and maintains one human-facing development document plus one local machine-state manifest:

1. **Single SDD artifact development document**: one-click generation enumerates every non-empty feature from the complete planning outline in exact source order, contains document location, a compact feature table, and exactly five subsections per feature. The initial `1. 功能需求说明` body stays empty; detailed requirements belong to the source planning document and later role-based SDD.
2. **Sidecar state manifest**: preserves stable IDs, source fingerprints, SDD/Feishu links, confirmation state, plan path, bug paths, revisions, and sync times. It is not uploaded and is not a second human document.

## Core Workflow

Select exactly one mode from the gate and follow its reference. The following rules are shared:

1. Read and normalize the planning source, preserving headings, tables, media, deletion marks, and source revision.
2. Assign stable feature IDs according to the active mode. PCTR-A splits into atomic functions. PCTR-B preserves source feature boundaries and order without atomic over-decomposition.
3. Retrieve ACSDM evidence where a project root is available. Separate planning facts, project rules, code facts, recommendations, and unresolved questions.
4. Score and pre-route each function to default ABC, enhanced ABC, or SDD.
5. Create the mode-specific requirement development document.
6. PCTR-A creates the paired planning confirmation/acceptance document. PCTR-B uses the uploaded role-based SDD and its mutually exclusive confirmation checkboxes as the planning confirmation surface.
7. Keep formal plan generation locked until the active mode's confirmation gate passes.
8. On confirmation, synchronize the authoritative planner decision, source revision, route, and local state manifest.
9. On `开始 <FEATURE-ID> 功能开发`, read the confirmed requirement, planner decision, ACSDM catalog, and code evidence; generate a detailed plan according to the selected route and set `technical_plan_status=pending-approval`. Do not modify code.
10. On `批准 <FEATURE-ID> 技术方案`, validate the route-appropriate plan and set `technical_plan_status=approved`. Do not modify code.
11. On `开始实施 <FEATURE-ID>`, implement only an approved plan and follow the ACSDM authorization/recording rules.
12. On `提交 <FEATURE-ID> 策划验收`, PCTR-A updates the paired acceptance document; PCTR-B records the submission and any later bug artifact path in the single development document and sidecar.
13. On acceptance failure, record the failed points and planner bug description, set the feature to bug-fix state, retrieve ACSDM/code evidence, and generate a first analysis. Do not mark complete.
14. On re-submission, preserve earlier rounds and create a new acceptance round.
15. Only after the explicit command `<FEATURE-ID> 策划已验收（任务完毕）` and successful validation may the requirement document set `development_status=completed`, `planning_acceptance_status=accepted`, and `final_feature_status=completed`, displayed as `功能已完成`.

## Confirmation Gate

PCTR-A keeps the existing confirmation requirements below. PCTR-B requires an uploaded SDD link/path and exactly one selected checkbox; only `已确认` unlocks planning. `存在歧义需要修改` blocks planning and requires a revised SDD upload/synchronization.

Before formal plan generation, require:

- all blocking confirmation items resolved;
- a planner confirmation summary;
- confirmation source document ID/revision in PCTR-A, or SDD Feishu link/revision in PCTR-B;
- explicit user synchronization/confirmation command;
- `planning_confirmation_status=confirmed` in PCTR-A, or `sdd_confirmation_status=confirmed` in PCTR-B.

Unconfirmed features may be inspected through ACSDM or code, but may not receive a final plan, implementation, or completion status.

## Command Semantics

- `生成策划确认文档`: create the paired confirmation/acceptance document.
- `生成 PCTR-B 功能需求开发文档`: read the complete planning outline, generate every feature in exact source order with empty requirement-description bodies, create the local document and sidecar, import/create the corresponding Feishu development document, and register its URL/revision plus one unambiguous SDD parent/target.
- `OUF → PCTR-B 功能编码查询`: internal read-only lookup used only when both suites are active; return one exact Feature ID and target receipt without changing state.
- `同步PCTR-B SDD <FEATURE-ID>`: locate the uniquely matched local SDD, validate it, upload it to Feishu, and write the local/Feishu references into the feature section. External upload occurs only under this explicit command.
- `<FEATURE-ID> SDD已确认`: select `已确认`, clear `存在歧义需要修改`, synchronize the SDD revision, and unlock plan generation.
- `<FEATURE-ID> SDD存在歧义需要修改`: select the ambiguity checkbox, clear `已确认`, record the issue, and keep planning locked.
- `同步策划确认 <FEATURE-ID>` or `<FEATURE-ID> 策划已确认`: validate blocking items, synchronize decisions, recalculate route, and unlock planning.
- `开始 <FEATURE-ID> 功能开发`: generate the detailed technical plan only.
- `批准 <FEATURE-ID> 技术方案`: approve the validated route-specific plan and unlock implementation; do not modify code.
- `开始实施 <FEATURE-ID>`: execute an approved plan.
- `提交 <FEATURE-ID> 策划验收`: enter planner acceptance and populate the current round.
- `<FEATURE-ID> 验收失败存在Bug：...`: create/update bug analysis and set bug-fix state.
- `<FEATURE-ID> 重新提交策划验收`: create a new acceptance round.
- `<FEATURE-ID> 策划已验收（任务完毕）`: validate all required acceptance points and mark complete.

Follow `references/command-contract.md`; do not infer a state-changing command from casual discussion or from a manually edited checkbox until synchronization validates the current Feishu revision.

## Route Rules

- Default ABC: small, local, low-risk work.
- Enhanced ABC: moderate work inside existing architecture requiring explicit state, files, regression, and rollback.
- SDD: hard triggers or high complexity such as migration, public framework changes, three or more modules, complex state machines, external SDKs, global locking/concurrency, or high-cost ambiguity.

Confirmation precedes every final route. In PCTR-B, the role-based SDD is the confirmation document and must retrieve ACSDM evidence when ACSDM is enabled. The later implementation plan is a separate local artifact path, not a second SDD.

## Acceptance Rules

- Technical verification, QA testing, and planning acceptance are distinct even when PCTR-B hides lifecycle columns from the human document.
- Partial acceptance cannot complete a feature.
- Failed acceptance must preserve the failed round, bug description, analysis, fix record, and re-test result.
- Completion requires planner confirmation, an approved plan, implementation submission, all mandatory planning acceptance points passed, no open blocking bugs, and an explicit completion command.

## Ambiguity Policy

Classify unresolved items as `待策划确认`, `待技术确认`, `待美术确认`, `待音频确认`, or `待平台确认`. Mark each planning item as blocking or non-blocking. Never invent values, persistence rules, priorities, assets, APIs, or framework capabilities.

## Resources

Use templates in `assets/` and deterministic scripts in `scripts/`.

For the preferred coexisting Orange handoff, resolve the feature through `references/pctr-b-feature-lookup-interface.md` before generation and upload through `references/pctr-b-handoff-interface.md` after validation. Use `assets/pctr-b-orange-sdd-request-template.md` only for cross-task/manual handoff.

- PCTR-A: run the existing requirement, confirmation, and dual-document validators.
- PCTR-B: run `scripts/validate_pctr_b_document.py` against the single document and `scripts/validate_pctr_b_state.py` against the sidecar manifest before delivery or state changes.
- After creating the PCTR-B Feishu development document, run `scripts/register_pctr_b_feishu_document.py` to register its URL/revision and SDD target before Orange lookup is allowed.

## Common Failures

- Do not treat document editing as explicit planner confirmation.
- Do not generate a final ABC/SDD plan for an unconfirmed feature.
- Do not let acceptance failure overwrite earlier acceptance rounds.
- Do not mark code-complete as planning-accepted.
- Do not mark planning-accepted as feature-complete without the explicit completion command.
- Do not overwrite planner-entered confirmation or acceptance fields during synchronization.
- Do not renumber stable feature IDs; create child IDs when confirmed scope requires splitting.
- Do not generate the PCTR-A paired confirmation document in PCTR-B.
- Do not add source-planning progress, planning-confirmation, development-status, or acceptance-status columns to the PCTR-B feature table.
- Do not generate only the currently discussed feature subset when creating/updating a PCTR-B development document; enumerate the complete planning outline.
- Do not auto-fill `1. 功能需求说明`; leave it empty until a human explicitly requests content.
- Do not upload an SDD whose feature ID is missing, ambiguous, duplicated, or mismatched.
- Do not let Orange invent or copy a Feature ID from title-only matching; it must come from the registered PCTR-B lookup receipt.
- Do not treat the local implementation-plan path as an uploaded Feishu document; program upload remains manual unless the user explicitly requests it.
