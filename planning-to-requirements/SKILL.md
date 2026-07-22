---
name: planning-to-requirements
description: Convert planning docs into PCTR-A paired requirements or PCTR-B single-doc workflows with lightweight planner confirmation, local decomposition, ACSDM evidence, OUF SDD handoff, implementation, acceptance, and bug lifecycle support.
---

# Planning to Requirements

## PJ032 Activation Gate

Before using this Skill in PJ032, read `<project root>/.codex/skill-gates.json`. Continue only when `pctr=true` and `pctr_mode` is `A` or `B`.

Exact standalone activation commands:

- `启用 PCTR` or `启用PCTR-A`: enable backward-compatible Mode A.
- `启用PCTR-B`: enable Mode B.

Never infer or switch modes from document shape, conversation wording, an SDD path, or a Feature ID. PCTR may coexist with ACSDM and Orange Unity Forge when each gate is independently enabled. Reject a missing/invalid `pctr_mode` instead of guessing.

When Orange and PCTR-B are both active, first use the read-only feature identity contract in `references/pctr-b-feature-lookup-interface.md`, then use the Markdown attachment/link-back contract in `references/pctr-b-handoff-interface.md`. While Orange is active and PCTR is disabled, the interface defines a narrow attachment fallback for an SDD that already contains an exact Feature ID obtained from an earlier active PCTR-B session. It does not activate PCTR-B or authorize lookup or any other PCTR behavior.

## Purpose

Manage the full lifecycle from planning source to confirmed requirements, technical planning, implementation handoff, planning acceptance, bug correction, and completion. Never let an Agent silently decide unresolved planning behavior. Keep PCTR-A and PCTR-B documents and state contracts separate.

## Artifact Ownership

PCTR's exclusive persistent artifact root is `<project root>/.PCTR/`:

- PCTR-A: `<project root>/.PCTR/A/<document-code>/`
- PCTR-B: `<project root>/.PCTR/B/<document-code>/`

Requirement documents, confirmation/acceptance documents, sidecars, implementation plans, and bug records must stay under the active mode's directory unless the user explicitly supplies another non-`docs/` target. Never create, regenerate, or migrate active PCTR artifacts into `<project root>/docs/`; that tree is reserved for Orange Unity Forge. Orange-owned working SDD/brief artifacts may remain under `<project root>/CodexTemp/OrangeUnityForge/` and are linked or attached through the documented handoff rather than becoming PCTR-owned files.

Treat legacy `docs/pctr/` files as migration sources only. Copy them into `.PCTR/A/` or `.PCTR/B/`, update internal local-path references, verify the copy, and preserve the legacy source until the user explicitly authorizes deletion.

## Mode Selection

Read `references/mode-routing.md` first.

- **PCTR-A**: use the existing planning source → requirement development document → planning confirmation/acceptance document chain. Preserve atomic decomposition, paired revisions, confirmation IDs, acceptance rounds, and multi-block interaction.
- **PCTR-B**: use planning source → one requirement development document. Preserve source heading order and exact titles; treat each leaf/small heading as one feature, or a large heading as the feature when it has no child heading. Put a concise planning-grounded description in the five-column feature table. Leave `1. 功能需求说明` empty for undeveloped features; for the current active feature, write only an authored functional description and its main summary points. Never copy source prose, images, tables, media URLs, or Feishu XML/HTML markup into that section. Keep each role-based SDD as a local Markdown file and attach that file inside the matching feature section; never create one Feishu SDD document per feature. Keep machine state in a local sidecar manifest rather than visible status columns.

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

PCTR-B creates and maintains one human-facing development document, lightweight per-feature planner confirmation files, local decomposition files, and one local machine-state manifest:

1. **Single SDD artifact development document**: one-click generation enumerates every non-empty feature from the complete planning outline in exact source order. Its feature table uses exactly `功能编码 / 策案标题 / 策案标题路径 / 功能需求说明 / 工时`. Every table description is concise and strips source markup/media. The matching `1. 功能需求说明` starts empty unless that feature is currently being designed or developed; an active feature contains only a short authored description and main functional points, not copied planning prose or media.
2. **Planner confirmation document**: one lightweight Markdown document per active feature before SDD generation. It lists only real planner-facing ambiguities and useful confirmation/improvement items. It does not include a document-level reply section; every ambiguity or confirmation item carries its own reply code block. Full functional understanding and breakdown stay in the local decomposition file.
3. **Local decomposition file**: the living PCTR-B input to OUF after planner decisions are synchronized.
4. **Sidecar state manifest**: preserves the planning sequence, base/legacy IDs, source fingerprints, planner-confirmation state, decomposition path, local SDD path, embedded attachment reference, confirmation state, plan path, bug paths, revisions, and sync times. It is not uploaded and is not a second human document.

## Core Workflow

Select exactly one mode from the gate and follow its reference. The following rules are shared:

1. Read and normalize the planning source, preserving headings, tables, media, deletion marks, and source revision in the source snapshot/fingerprints for traceability. Do not reproduce source prose or media in the PCTR-B human document.
2. Assign feature IDs according to the active mode. PCTR-A splits into atomic functions. PCTR-B preserves source feature boundaries and order without atomic over-decomposition and uses `<策案层级序号>-<原功能编码>`, for example `1.1-XK5A-SAVE-F003`. Preserve the original base code and legacy aliases in the sidecar for migration and lookup.
3. Retrieve ACSDM evidence where a project root is available. Separate planning facts, project rules, code facts, recommendations, and unresolved questions.
4. Score and pre-route each function to default ABC, enhanced ABC, or SDD.
5. Create the mode-specific requirement development document.
6. PCTR-A creates the paired planning confirmation/acceptance document. PCTR-B first creates a lightweight per-feature planner confirmation Markdown and local decomposition; only after planner confirmation may OUF generate a detailed role-based SDD Markdown.
7. Keep SDD generation locked until PCTR-B planner confirmation passes; keep formal plan or implementation locked until the active mode's SDD/program confirmation gate passes.
8. On confirmation, synchronize the authoritative planner decision, source revision, route, and local state manifest.
9. On `开始 <FEATURE-ID> 功能开发`, read the confirmed requirement, planner decision, ACSDM catalog, and code evidence; generate a detailed plan according to the selected route and set `technical_plan_status=pending-approval`. Do not modify code.
10. On `批准 <FEATURE-ID> 技术方案`, validate the route-appropriate plan and set `technical_plan_status=approved`. Do not modify code.
11. On `开始实施 <FEATURE-ID>`, implement only an approved plan and follow the ACSDM authorization/recording rules.
12. On `提交 <FEATURE-ID> 策划验收`, PCTR-A updates the paired acceptance document; PCTR-B records the submission and any later bug artifact path in the single development document and sidecar.
13. On acceptance failure, record the failed points and planner bug description, set the feature to bug-fix state, retrieve ACSDM/code evidence, and generate a first analysis. Do not mark complete.
14. On re-submission, preserve earlier rounds and create a new acceptance round.
15. Only after the explicit command `<FEATURE-ID> 策划已验收（任务完毕）` and successful validation may the requirement document set `development_status=completed`, `planning_acceptance_status=accepted`, and `final_feature_status=completed`, displayed as `功能已完成`.

## Confirmation Gate

PCTR-A keeps the existing confirmation requirements below. PCTR-B has two gates: first the lightweight planner confirmation document must resolve every must-answer planner ambiguity and update the decomposition; then the detailed local SDD Markdown must be reviewed by the programmer and synchronized/confirmed when an attachment is used. The planner confirmation document does not use a document-level reply section; every ambiguity or confirmation item must have its own reply code block immediately below it.

Before formal plan generation, require:

- all blocking confirmation items resolved;
- a planner confirmation summary;
- confirmation source document ID/revision in PCTR-A, or local SDD identity plus attachment reference and containing development-document revision in PCTR-B;
- explicit user synchronization/confirmation command;
- `planning_confirmation_status=confirmed` in PCTR-A, or `sdd_confirmation_status=confirmed` in PCTR-B.

Unconfirmed features may be inspected through ACSDM or code, but may not receive a final plan, implementation, or completion status.

## Command Semantics

- `生成策划确认文档`: create the paired confirmation/acceptance document.
- `生成 PCTR-B 功能需求开发文档`: read the complete planning outline and every selected feature body, derive the planning sequence, migrate IDs to `<序号>-<原编码>`, generate every feature in exact source order with concise table descriptions, leave undeveloped feature requirement sections empty, preserve any validated active-feature authored description, create the local document and sidecar, then import/create the one corresponding Feishu development document and register its URL/revision.
- `阅读这个功能生成策划确认文档`: for exactly one PCTR-B feature, save the source snapshot, ask ACSDM for related rule/history indexes when available, write the local decomposition, and render a lightweight planner confirmation Markdown. Do not upload to Feishu unless explicitly requested.
- `策划已确认`: parse each per-item reply code block from the current PCTR-B planner confirmation document, update the decomposition and sidecar, and unlock detailed SDD generation only when all must-answer planner ambiguities are resolved.
- `生成详细 SDD 工件`: after planner confirmation, pass the confirmed decomposition to Orange Unity Forge to generate one detailed role-based local SDD Markdown; keep it Draft until programmer review.
- `OUF → PCTR-B 功能编码查询`: internal read-only lookup used only when both suites are active; return one exact Feature ID and target receipt without changing state.
- `同步PCTR-B SDD <FEATURE-ID>`: locate and validate the uniquely matched local SDD Markdown. Attach the file directly inside the matching feature section only when the available Feishu tooling can deterministically insert and verify the attachment at that exact position; otherwise stop before external write, preserve the local path/code block, and ask the user to upload the file manually. Never create a separate Feishu SDD document.
- `登记PCTR-B Markdown附件 <FEATURE-ID>`: after automatic or manual insertion, record the attachment token/URL/name and the containing development-document revision, then leave confirmation pending.
- `<FEATURE-ID> SDD已确认` or `<FEATURE-ID> 程序已确认`: require the current local Markdown identity, confirmed decomposition, and no blocking SDD decision; when an attachment is used, require its matching attachment reference, select `已确认`, clear `存在歧义需要修改`, synchronize the containing document revision, and unlock plan generation or explicit implementation according to risk.
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

Confirmation precedes every final route. In PCTR-B, the lightweight planner confirmation document confirms product rules first; the role-based local SDD Markdown is generated later from the confirmed decomposition and must retrieve ACSDM evidence when ACSDM is enabled. The later implementation plan or checklist is a separate local artifact path, not a second SDD.

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
- After creating the PCTR-B Feishu development document, run `scripts/register_pctr_b_feishu_document.py` to register its URL/revision before Orange lookup is allowed.

## Common Failures

- Do not treat document editing as explicit planner confirmation.
- Do not generate a final ABC/SDD plan for an unconfirmed feature.
- Do not let acceptance failure overwrite earlier acceptance rounds.
- Do not mark code-complete as planning-accepted.
- Do not mark planning-accepted as feature-complete without the explicit completion command.
- Do not overwrite planner-entered confirmation or acceptance fields during synchronization.
- Do not discard the original base feature code when adding or changing the planning-sequence prefix; preserve it and all previous full IDs as sidecar aliases.
- Do not generate the PCTR-A paired confirmation document in PCTR-B.
- Do not add source-planning progress, planning-confirmation, development-status, or acceptance-status columns to the PCTR-B feature table.
- Do not generate only the currently discussed feature subset when creating/updating a PCTR-B development document; enumerate the complete planning outline.
- Do not leave the feature-table `功能需求说明` cell empty when planning content exists; it must contain a concise planning-grounded summary.
- Do not populate an undeveloped feature's `1. 功能需求说明` merely because source content exists. Leave it empty until the feature becomes current.
- Do not paste source planning prose, images, tables, media URLs, citations, or Feishu XML/HTML markup into a feature's `1. 功能需求说明`. For an active feature, write only a functional description and main summary points.
- Do not attach an SDD whose feature ID is missing, ambiguous, duplicated, or mismatched.
- Do not let Orange invent or copy a Feature ID from title-only matching; it must come from the registered PCTR-B lookup receipt.
- Do not create one Feishu SDD Docx per feature. Attach the local Markdown file inside the existing feature section or defer to manual upload.
- Do not treat the local implementation-plan path as an uploaded Feishu document; program upload remains manual unless the user explicitly requests it.
- Do not place new PCTR artifacts under `docs/` or use `docs/pctr/` as an active output root.
