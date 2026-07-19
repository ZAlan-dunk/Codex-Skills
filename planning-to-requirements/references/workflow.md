# Workflow

## Phase 1: Resolve Inputs

Collect the planning source, project root, requirement output target, planning-confirmation output target, style profile, existing document links, and operating mode. Continue with labeled limitations when optional inputs are absent.

## Phase 2: Read and Normalize

Read outline then full content as needed. Preserve headings, source sequence, nested conditions, tables, media references, deletion marks, semantic color notes, document ID, and revision. Treat placeholders and examples as unresolved rather than final values.

## Phase 3: Build the Feature Tree

Create level-one, child, and atomic functions. Assign stable IDs. Record dependencies and source mappings. Never renumber existing IDs during update mode.

## Phase 4: Retrieve ACSDM

Read the project-local root index, `00Rule` for rule-first triggers, matching module indexes, directly relevant documents, and referenced code locations. Label evidence categories and missing evidence.

## Phase 5: Generate Requirement Development Document

Use `references/output-schema.md` and `assets/detailed-feature-document-template.md`. Pre-route complexity, but keep the formal task capsule locked while planning confirmation is pending.

## Phase 6: Generate Planning Confirmation and Acceptance Document

Use `references/planning-confirmation-workflow.md` and the templates in `assets/`.

For every active feature:

- write a short planner-readable implementation description;
- mirror all planning ambiguity and agent-uncertain behavior;
- classify questions as blocking or non-blocking;
- include a planner response area and final confirmation summary;
- include planner-readable acceptance points and an empty acceptance history.

Write mutual document links and revisions in both documents.

## Phase 7: Synchronize Planning Confirmation

Only react to explicit commands defined in `references/command-contract.md`.

On synchronization:

1. Read the current confirmation document and revision.
2. Locate the feature ID.
3. Validate all blocking questions.
4. Preserve original planning text and conflict history.
5. Write the final planner conclusion into the requirement document.
6. Mark resolved questions, recalculate scope/complexity/route, and regenerate the task capsule.
7. Set the confirmation status to `confirmed` and planning status to `pending-plan`.
8. Record both revisions and synchronization time.

If confirmed scope changes identity, preserve the old ID and create child IDs rather than changing its meaning.

## Phase 8: Start Development Planning by Feature ID

`开始 <FEATURE-ID> 功能开发` means plan only.

1. Validate `planning_confirmation_status=confirmed`.
2. Read the confirmed requirement and planner summary.
3. Retrieve ACSDM and inspect referenced code.
4. Generate default ABC, enhanced ABC, or SDD artifacts according to the route.
5. Set the plan state appropriately.
6. Do not edit code until `开始实施 <FEATURE-ID>` or an equivalent explicit authorization.

## Phase 9: Implement and Submit Acceptance

After approved implementation and technical verification, `提交 <FEATURE-ID> 策划验收` must:

- collect implementation version/commit/build and known limitations;
- populate the planner-readable acceptance checklist;
- create acceptance round 1 or the next round;
- set development state to `submitted-for-planning-acceptance`;
- set planning acceptance state to `pending`.

## Phase 10: Acceptance Failure and Bug Loop

On `<FEATURE-ID> 验收失败存在Bug：...`:

1. Preserve the failed acceptance round.
2. Record failed point IDs and planner description.
3. Set acceptance state to `failed`, development state to `bug-fixing`, and final state to `in-progress`.
4. Read requirements, confirmed decisions, ACSDM records, implementation evidence, logs, and relevant code.
5. Produce first analysis: expected vs actual, reproduction, evidence, hypotheses, likely files, fix proposal, risk, and regression tests.
6. Wait for authorization before modifying code.

On re-submission, append a new acceptance round; never overwrite the failed round.

## Phase 11: Complete

On `<FEATURE-ID> 策划已验收（任务完毕）`:

- verify all mandatory acceptance points passed;
- verify no blocking bugs remain;
- verify the feature was confirmed, planned, implemented, and submitted;
- update the confirmation document to accepted;
- update the requirement document to `功能已完成`;
- record completion time and accepted revision;
- update ACSDM only when the user requests recording.

## Phase 12: Validate

Run:

```powershell
python scripts/validate_feature_document.py <requirements.md>
python scripts/validate_planning_confirmation.py <confirmation.md>
python scripts/validate_dual_document_state.py <requirements.md> <confirmation.md>
```

Fix state, ID, confirmation, acceptance, or task-capsule errors before delivery.
