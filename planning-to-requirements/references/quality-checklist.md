# Quality Checklist

## Source and Decomposition

- [ ] Every source heading is represented or explicitly out of scope.
- [ ] Original order, tables, media captions, deletion marks, and placeholders are preserved.
- [ ] Broad items are split into independently testable functions with stable IDs.

## Requirement Document

- [ ] Every active feature has source trace, goal, scope, non-scope, flow, lifecycle, edge cases, evidence, acceptance, and route.
- [ ] Every unresolved planning item has owner and blocking status.
- [ ] Every task capsule contains the planning confirmation gate.
- [ ] State fields use valid values from `feature-lifecycle.md`.

## PCTR-B Single Document

- [ ] Source heading text and order are preserved exactly.
- [ ] Leaf/small headings are features; a large heading is a feature only when it has no child heading.
- [ ] One-click generation covers every non-empty feature heading in the complete planning outline.
- [ ] Every initial `1. 功能需求说明` body is empty; no planning正文 was automatically copied or summarized.
- [ ] The feature table contains no planning-progress, confirmation, development-status, or acceptance-status columns.
- [ ] Every feature contains exactly the five required numbered sections.
- [ ] Every SDD has one matching PCTR feature ID and at most one selected confirmation checkbox.
- [ ] Orange-generated SDD identity came from one fresh PCTR-B lookup receipt, not title-only matching.
- [ ] The SDD metadata source heading path/revision and Feishu development-document target match the registered sidecar.
- [ ] Confirmed SDDs have a current Feishu URL and revision.
- [ ] Implementation plans remain local paths unless explicit upload is requested.
- [ ] Bug record paths are append-only.
- [ ] Document order and sidecar feature order match.

## Planning Confirmation Document

- [ ] Every active feature appears in the summary and detailed section.
- [ ] Every feature has a short planner-readable implementation description.
- [ ] Every planning ambiguity or agent-uncertain behavior is mirrored.
- [ ] Confirmation IDs are unique.
- [ ] Blocking items cannot remain pending when the feature is confirmed.
- [ ] Final planner summary, confirmer, time, document ID, and revision exist for confirmed features.
- [ ] Every feature has planner-readable acceptance items.

## Synchronization

- [ ] Feature IDs match across both documents.
- [ ] Planner-entered responses and acceptance results are preserved.
- [ ] Original planning text and conflict history remain traceable.
- [ ] Both document revisions and last synchronization time are recorded.
- [ ] Route is recalculated after scope-changing confirmation.
- [ ] Revision conflicts produce a conflict report rather than overwrite.

## Planning and Implementation Gates

- [ ] PCTR-A unconfirmed features cannot generate final ABC/SDD.
- [ ] PCTR-B features cannot generate an implementation plan until the uploaded role-based SDD is confirmed.
- [ ] `开始功能开发` generates a plan only and ends at `technical_plan_status=pending-approval`.
- [ ] `批准 FEATURE-ID 技术方案` is required to reach `technical_plan_status=approved`.
- [ ] Code edits require both an approved plan and `开始实施` or equivalent implementation authorization.
- [ ] SDD still retrieves ACSDM first.

## Acceptance and Bugs

- [ ] Submission creates a new acceptance round.
- [ ] Failed rounds are preserved.
- [ ] Bug descriptions map to failed acceptance IDs.
- [ ] Bug analysis precedes edits.
- [ ] Re-submission creates a new round.
- [ ] Partial/failed acceptance cannot complete a feature.
- [ ] Completion requires all mandatory points passed, no blocking bugs, and explicit completion command.

## Claims

- [ ] Planning facts, planner decisions, ACSDM rules, code facts, recommendations, and unknowns are separated.
- [ ] No fabricated project path, method, field, API, framework, or planner decision is presented as fact.
