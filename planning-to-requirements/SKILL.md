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

PCTR's exclusive persistent artifact root is `<project root>/.PCTR/`. On the first enabled PCTR action, create this folder if it does not exist.

- PCTR-A keeps the backward-compatible root `<project root>/.PCTR/A/<document-code>/`.
- PCTR-B uses the planning-version root `<project root>/.PCTR/<planning-version>/`, for example `<project root>/.PCTR/M032v1.2/`.
- Inside a PCTR-B planning-version root, create one direct child folder per feature in exact planning order. The folder name must be the full Feature ID, for example `1.2.1-XK5A-SAVE-F004`.
- A PCTR-B feature folder contains feature-local Markdown artifacts: `A-01-planner-confirmation-snapshot.md`, `A-02-feature-decomposition.md`, and later the PCTR-bound `B-01-runtime-sdd.md` when such a local SDD snapshot is generated. Do not create multiple decomposition Markdown files.
- OUF remains the owner of `docs/forge-artifacts/`. PCTR may register OUF Context Brief / SDD / Plan / Report / Evidence paths in the sidecar, but must not move, rename, delete, or restrict OUF outputs.

Requirement documents, confirmation/acceptance documents, sidecars, implementation plans, and bug records must stay under the active PCTR directory unless the user explicitly supplies another non-`docs/` target. Never create, regenerate, or migrate active PCTR artifacts into `<project root>/docs/`; that tree is reserved for Orange Unity Forge.

Treat legacy `docs/pctr/`, `.PCTR/B/<document-code>/`, and `CodexTemp/PCTR/` files as migration sources only. Copy them into the active `.PCTR/` layout, update internal local-path references, verify the copy, and preserve the legacy source until the user explicitly authorizes deletion.

## Mode Selection

Read `references/mode-routing.md` first.

- **PCTR-A**: use the existing planning source → requirement development document → planning confirmation/acceptance document chain. Preserve atomic decomposition, paired revisions, confirmation IDs, acceptance rounds, and multi-block interaction.
- **PCTR-B**: use planning source → one requirement development document. Preserve source heading order and exact titles; treat each leaf/small heading as one feature, or a large heading as the feature when it has no child heading. Put a concise planning-grounded description in the five-column feature table. Leave `1. 功能需求说明` empty for undeveloped features; for the current active feature, write only an authored functional description and its main summary points. Never copy source prose, images, tables, media URLs, or Feishu XML/HTML markup into that section. PCTR-B creates one local human development document and registers the corresponding Feishu development document after the user/program has created or uploaded it. Attachments are manual by default: PCTR outputs local Markdown paths and then records the uploaded attachment identity. Keep machine state in a local sidecar manifest rather than visible status columns.

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
2. **Planner confirmation snapshot**: `A-01-planner-confirmation-snapshot.md` in the feature folder. It lists only real planner-facing ambiguities and useful confirmation/improvement items. It does not include a document-level reply section; every ambiguity or confirmation item carries its own lettered preselection list, separate recommended choice and reason, and its own two-line reply code block. A planner may either select one listed code or leave `选择：` empty and write a custom rule in `补充：`. Full functional understanding and breakdown stay in `A-02-feature-decomposition.md`. After generation, upload the native `.md` file itself and place its attachment immediately below the matching feature's `2. SDD确认文档` heading in the single Feishu development document. Do not create or import it as a separate Feishu document.
3. **Local decomposition file**: `A-02-feature-decomposition.md`, the only living PCTR-B decomposition file for that feature and the direct input to OUF after planner decisions are synchronized.
4. **Detailed SDD artifact**: `B-01-runtime-sdd.md`, generated after confirmation from `A-02-feature-decomposition.md` and handed to OUF/program review for direct execution.
5. **Sidecar state manifest**: preserves the planning version, planning sequence, base/legacy IDs, feature artifact folder, source fingerprints, planner-confirmation state, decomposition path, local SDD path, embedded attachment reference, confirmation state, plan path, bug paths, revisions, and sync times. It is not uploaded and is not a second human document.

## Core Workflow

Select exactly one mode from the gate and follow its reference. The following rules are shared:

1. Read and normalize the planning source, preserving headings, tables, media, deletion marks, and source revision in the source snapshot/fingerprints for traceability. Do not reproduce source prose or media in the PCTR-B human document.
2. Assign feature IDs according to the active mode. PCTR-A splits into atomic functions. PCTR-B preserves source feature boundaries and order without atomic over-decomposition and uses `<策案层级序号>-<原功能编码>`, for example `1.1-XK5A-SAVE-F003`. Preserve the original base code and legacy aliases in the sidecar for migration and lookup.
3. Retrieve ACSDM evidence where a project root is available. Separate planning facts, project rules, code facts, recommendations, and unresolved questions.
4. Score and pre-route each function to default ABC, enhanced ABC, or SDD.
5. Create the mode-specific requirement development document.
6. PCTR-A creates the paired planning confirmation/acceptance document. PCTR-B first creates a lightweight per-feature planner confirmation Markdown and the single local decomposition/context package. PCTR reports the exact Feishu target; the user/program manually uploads the A-01 Markdown and PCTR records the attachment. Only after planner confirmation may OUF generate detailed development artifacts.
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

PCTR-A keeps the existing confirmation requirements below. PCTR-B has two gates: first the lightweight planner confirmation document must resolve every must-answer planner ambiguity and update the decomposition; then the detailed local SDD Markdown must be reviewed by the programmer and synchronized/confirmed when an attachment is used. The planner confirmation document does not use a document-level reply section. Every ambiguity or confirmation item must list two to six meaningful lettered preselection options, then state `推荐选择：<代码>` and `推荐原因：<原因>` separately, followed immediately by a reply code block containing only `选择：` and `补充：`; the item identity comes from the heading above the block. A listed option code is valid, and an empty `选择：` plus non-empty `补充：` is a valid planner-authored custom solution. Both fields empty means unanswered; an unknown option code is invalid. Optional items may remain unanswered without blocking confirmation, but silence must never be treated as acceptance of the recommendation.

Before formal plan generation, require:

- all blocking confirmation items resolved;
- a planner confirmation summary;
- confirmation source document ID/revision in PCTR-A, or local SDD identity plus attachment reference and containing development-document revision in PCTR-B;
- explicit user synchronization/confirmation command;
- `planning_confirmation_status=confirmed` in PCTR-A, or `sdd_confirmation_status=confirmed` in PCTR-B.

Unconfirmed features may be inspected through ACSDM or code, but may not receive a final plan, implementation, or completion status.

## Command Semantics

- `生成策划确认文档`: create the paired confirmation/acceptance document.
- `生成 PCTR-B 功能需求开发文档`: read the complete planning outline and every selected feature body, derive the planning sequence, migrate IDs to `<序号>-<原编码>`, generate every feature in exact source order with concise table descriptions, leave undeveloped feature requirement sections empty, preserve any validated active-feature authored description, and create the local document plus sidecar under `.PCTR/<planning-version>/`. Feishu creation/upload is manual; after the user/program creates the corresponding Feishu development document, run the registration script to record its URL/revision.
- `阅读这个功能生成策划确认文档`: for exactly one PCTR-B feature, read only the matched planning section when block/heading identity is available, ask ACSDM for related rule/history/OUF-link indexes when available, write the single local `A-02-feature-decomposition.md`, and render `A-01-planner-confirmation-snapshot.md`. Return the exact target feature heading for manual Feishu upload; after upload, register the A-01 attachment identity. Never create a separate Feishu document.
- `策划已确认`: parse each per-item reply code block from the current PCTR-B planner confirmation document. Accept either one listed option code or an empty `选择：` with a non-empty custom `补充：`; reject unknown codes and unresolved must-answer items. Update the decomposition and sidecar, and unlock detailed SDD generation only when all must-answer planner ambiguities are resolved. Unanswered optional items remain out of scope and are not implicit approval of the recommended choice.
- `生成详细 SDD 工件`: after planner confirmation, pass the confirmed `A-02-feature-decomposition.md` to Orange Unity Forge. Do not restrict OUF's own `docs/forge-artifacts/` outputs. Register the resulting OUF artifacts in the PCTR sidecar; if a PCTR-bound `B-01-runtime-sdd.md` is produced, keep it Draft until programmer review.
- `OUF → PCTR-B 功能编码查询`: internal read-only lookup used only when both suites are active; return one exact Feature ID and target receipt without changing state.
- `同步PCTR-B SDD <FEATURE-ID>`: locate and validate the uniquely matched local `B-01-runtime-sdd.md` when present, then return the exact target feature heading and local path for manual Feishu upload. Do not automatically upload or create a separate Feishu SDD document unless the user explicitly requests an API-based insertion and exact-position verification is available.
- `登记PCTR-B Markdown附件 <FEATURE-ID>`: after manual insertion, record the attachment token/URL/name and the containing development-document revision, then leave confirmation pending.
- `登记PCTR-B OUF产物 <FEATURE-ID>`: record OUF artifact paths/hashes/types from `docs/forge-artifacts/` in the sidecar so PCTR and ACSDM can find them without copying OUF documents.
- `<FEATURE-ID> SDD已确认` or `<FEATURE-ID> 程序已确认`: require the current local Markdown identity, confirmed decomposition, and no blocking SDD decision; when an attachment is used, require its matching attachment reference, select `已确认`, clear `存在歧义需要修改`, synchronize the containing document revision, and unlock plan generation or explicit implementation according to risk.
- `<FEATURE-ID> SDD存在歧义需要修改`: select the ambiguity checkbox, clear `已确认`, record the issue, and keep planning locked.
- `同步策划确认 <FEATURE-ID>` or `<FEATURE-ID> 策划已确认`: validate blocking items, synchronize decisions, recalculate route, and unlock planning.
- `开始 <FEATURE-ID> 功能开发`: if planner confirmation is missing or pending, enter the PCTR-B confirmation gate instead of planning or implementation: generate/update A-01 and A-02, attach A-01 in the matching feature section, keep SDD/plan/implementation locked, and report the pending planner replies. Only after the required confirmation gates pass does this command generate the detailed technical plan.
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

For every PCTR-B planner-facing reply item, derive concrete preselection choices from the real decision space rather than using vague `同意/不同意` options. Use consecutive uppercase codes beginning with `A`; include only meaningful alternatives. Keep the recommended code and its reason separate. Do not add a generic “其他” choice merely to force selection: a planner's custom scheme is represented by leaving `选择：` empty and writing the authoritative rule in `补充：`.

## Token and Time Control

- Do not reread a complete Feishu planning document when the sidecar has a valid `feishu_blocks` locator for the current feature. Read only the matched heading/block section, then compare its feature-level hash/revision.
- Do not duplicate OUF development logs into PCTR or ACSDM. PCTR registers OUF artifact paths/hashes; ACSDM reads the OUF link index and opens only selected original files.
- Feishu Markdown uploads are manual by default. PCTR generates local files and exact target headings, then updates state after the user/program reports the uploaded attachment identity.
- `A-02-feature-decomposition.md` remains the unique product-rule context package for the feature. It is the handoff input for OUF and later implementation, while OUF's own files remain in `docs/forge-artifacts/`.

## Resources

Use templates in `assets/` and deterministic scripts in `scripts/`.

For the preferred coexisting Orange handoff, resolve the feature through `references/pctr-b-feature-lookup-interface.md` before generation and use `references/pctr-b-handoff-interface.md` after validation to return manual-upload targets or register verified attachments. Use `assets/pctr-b-orange-sdd-request-template.md` only for cross-task/manual handoff.

- PCTR-A: run the existing requirement, confirmation, and dual-document validators.
- PCTR-B: run `scripts/validate_pctr_b_document.py` against the single document and `scripts/validate_pctr_b_state.py` against the sidecar manifest before delivery or state changes.
- After the user/program creates the PCTR-B Feishu development document, run `scripts/register_pctr_b_feishu_document.py` to register its URL/revision before Orange lookup is allowed.
- Use `scripts/extract_feishu_feature_section.py` when only one exported Feishu/planning Markdown section should be read.
- Use `scripts/register_pctr_b_ouf_artifact.py` to register OUF artifact paths/hashes in the sidecar without copying OUF files.

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
- Do not create one Feishu SDD Docx per feature. Output the local Markdown path and use manual upload/registration by default.
- Do not create one Feishu planner-confirmation Docx/Wiki per feature. A generated A-01 must be uploaded manually as the native `.md` attachment immediately below the matching `2. SDD确认文档` heading; a separate-document URL in planner-confirmation state is invalid.
- Do not render a PCTR-B planner reply item without concrete lettered options, a separate recommended option code, and a separate recommendation reason.
- Do not reject a planner-authored custom solution merely because `选择：` is empty when `补充：` contains the rule; do not treat both fields empty as confirmation or treat an unanswered optional item as acceptance of the recommendation.
- Do not treat the local implementation-plan path as an uploaded Feishu document; program upload remains manual unless the user explicitly requests it.
- Do not place new PCTR artifacts under `docs/` or use `docs/pctr/` as an active output root.
