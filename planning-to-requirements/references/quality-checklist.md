# Quality Checklist

## Source and Decomposition

- [ ] Every source heading is represented or explicitly out of scope.
- [ ] Original order, tables, media captions, deletion marks, and placeholders are preserved.
- [ ] Broad items are split into independently testable functions with stable IDs.

## Requirement Document

- [ ] Every active feature has source trace, goal, scope, non-scope, flow, lifecycle, edge cases, evidence, acceptance, and route.
- [ ] Every unresolved planning item has owner and required-decision status.
- [ ] Every task capsule contains the planning confirmation gate.
- [ ] State fields use valid values from `feature-lifecycle.md`.

## PCTR-B Single Document

- [ ] The local development document and sidecar are under `.PCTR/<planning-version>/`; plan and bug roots are beneath the same directory.
- [ ] No active PCTR path points to `docs/`, `CodexTemp/PCTR/`, or PCTR-B SDD output under `CodexTemp/OrangeUnityForge/`.
- [ ] Source heading text and order are preserved exactly.
- [ ] Leaf/small headings are features; a large heading is a feature only when it has no child heading.
- [ ] One-click generation covers every non-empty feature heading in the complete planning outline.
- [ ] Every feature ID begins with its hierarchical planning sequence, for example `1.2.1-XK5A-SAVE-F004`; the sidecar preserves the base code and legacy aliases.
- [ ] The feature table uses exactly `功能编码 / 策案标题 / 策案标题路径 / 功能需求说明 / 工时`.
- [ ] Every table requirement description is a short planning-grounded summary with no source image, media URL, HTML/XML tag, Markdown table, or copied long-form source body.
- [ ] Every undeveloped feature leaves `1. 功能需求说明` empty.
- [ ] Every current design/development feature uses `1. 功能需求说明` only for a concise functional description and main functional points.
- [ ] No `1. 功能需求说明` contains source images, tables, media links, citations, Feishu XML/HTML markup, deletion markup, or pasted source paragraphs.
- [ ] The feature table contains no planning-progress, confirmation, development-status, or acceptance-status columns.
- [ ] Every feature contains exactly the five required numbered sections.
- [ ] Every feature has one exact folder `.PCTR/<planning-version>/<FEATURE-ID>/`, created in source order, and every SDD has one matching PCTR feature ID and at most one selected confirmation checkbox.
- [ ] Orange-generated SDD identity and output path came from one fresh PCTR-B lookup receipt, not title-only matching.
- [ ] The SDD metadata source heading path/revision and Feishu development-document identity match the registered sidecar.
- [ ] Every PCTR-B feature folder has only two `A-*.md` artifacts: `A-01-planner-confirmation-snapshot.md` and `A-02-feature-decomposition.md`; no duplicate decomposition file exists.
- [ ] Every non-missing A-01 planner confirmation is uploaded as the native `.md` file immediately below the matching feature's `2. SDD确认文档` heading in the single Feishu development document.
- [ ] No per-feature planner-confirmation Docx/Wiki was created, and sidecar planner-confirmation state contains no active separate-document URL.
- [ ] Every A-01 reply-bearing item has two to six meaningful consecutive lettered options, a `推荐选择` code that exists in that list, and a separate non-empty `推荐原因`.
- [ ] A listed code is accepted; an empty selection plus non-empty supplement is accepted as a custom planner rule; an unknown code is rejected; both fields empty blocks only must-answer items and never implies acceptance of the recommendation.
- [ ] Every detailed SDD remains the feature-local `B-01-runtime-sdd.md`; no per-feature Feishu SDD Docx was created.
- [ ] Every confirmed SDD has a current attachment reference and containing development-document revision.
- [ ] The Feishu feature section matches the required structural pattern: path quote, optional concise requirement section, three highlighted SDD blocks, path code block, Markdown attachment, implementation-plan code block, Bug table, optimization section, and divider.
- [ ] Implementation plans remain local paths unless explicit upload is requested.
- [ ] Bug record paths are append-only.
- [ ] Document order and sidecar feature order match.

## Planning Confirmation Document

- [ ] PCTR-A paired documents and mapping state are under `.PCTR/A/<document-code>/`, not `docs/pctr/`.
- [ ] Every active feature appears in the summary and detailed section.
- [ ] Every feature has a short planner-readable implementation description.
- [ ] Every planning ambiguity or agent-uncertain behavior is mirrored.
- [ ] Confirmation IDs are unique.
- [ ] Required decision items cannot remain pending when the feature is confirmed.
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
- [ ] PCTR-B features cannot generate a detailed OUF SDD until lightweight planner confirmation is confirmed.
- [ ] PCTR-B features cannot generate an implementation plan or implementation checklist until the detailed local SDD is confirmed by program review.
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
- [ ] Completion requires all mandatory points passed, no unresolved bugs, and explicit completion command.

## Claims

- [ ] Planning facts, planner decisions, ACSDM rules, code facts, recommendations, and unknowns are separated.
- [ ] No fabricated project path, method, field, API, framework, or planner decision is presented as fact.
