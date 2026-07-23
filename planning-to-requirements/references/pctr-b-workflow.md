# PCTR-B Workflow

## 1. Resolve Inputs

Collect the planning source identity, source revision, project root, planning version (for example `M032v1.2`), document code/base code, Feishu development-document URL, implementation-plan root, bug-record root, and sidecar path. For ongoing feature work, prefer the feature-level Feishu heading/block locator from the sidecar over rereading the whole planning document.

Default artifact roots when the user does not specify them:

- PCTR root: `<project root>/.PCTR/` (create it on first enabled PCTR action if missing)
- PCTR-B planning-version root: `<project root>/.PCTR/<planning-version>/`, for example `<project root>/.PCTR/M032v1.2/`
- feature artifacts: `<project root>/.PCTR/<planning-version>/<FEATURE-ID>/`
- OUF artifacts: `<project root>/docs/forge-artifacts/` remains OUF-owned and is linked, not copied
- implementation plans: `<project root>/.PCTR/<planning-version>/_plans/`
- bug records: `<project root>/.PCTR/<planning-version>/_bugs/`

The local development document, sidecar, feature folders, plan, and bug records are persistent PCTR artifacts. Never place them under `docs/`, `CodexTemp/PCTR/`, or `CodexTemp/OrangeUnityForge/`. OUF-owned artifacts stay under `docs/forge-artifacts/` and are recorded by path/hash in the PCTR sidecar. A PCTR-bound detailed SDD, when produced, is the feature-local `B-01-runtime-sdd.md`.

## 2. Preserve the Planning Heading Framework

Read the source outline and preserve heading text and order exactly.

Feature boundary rule:

1. A heading with child headings is a grouping heading.
2. Each leaf/small heading is one feature requirement.
3. If a large heading has no child heading, that large heading is one feature requirement.
4. Do not atomically split one selected source heading into multiple visible feature sections.
5. Keep tables, lists, media references, conditions, and unresolved wording in the normalized source snapshot and source fingerprint. Do not copy them into the human development document.

Assign a hierarchical planning sequence to every heading from sibling order, including grouping headings. The first leaf under the first top-level group is `1.1`; a leaf under the second child of that group may be `1.2.1`.

Assign or preserve a base ID such as `<DOC-CODE>-F001`, then expose the full ID as `<planning-sequence>-<base-id>`, for example `1.2.1-XK5A-SAVE-F004`. Preserve `base_feature_id` and prior full IDs in `legacy_feature_ids`. If source order changes, update the sequence prefix but never reassign the base code to a different source feature. Create each feature folder with this full ID as its exact folder name.

## 3. Create the Single SDD Artifact Development Document

Use `assets/pctr-b-development-document-template.md` and `assets/pctr-b-feature-template.md`.

Create:

- document location metadata;
- one five-column feature table using exactly `功能编码 / 策案标题 / 策案标题路径 / 功能需求说明 / 工时`;
- one feature section per selected source heading;
- one local sidecar manifest using `assets/pctr-b-state.example.json` as the schema example;
- one feature folder per feature in exact source order under `.PCTR/<planning-version>/`, named by full Feature ID.

The table requirement cell is a concise planning-grounded summary with markup and media removed. The matching `1. 功能需求说明` body is empty for an undeveloped feature. When a feature becomes the current design/development target, author a short functional description plus main functional points from the complete source section. Never paste source paragraphs, tables, images, media URLs, citations, or Feishu XML/HTML markup into the body.

Then give the local Markdown path to the user/program for manual Feishu creation or upload as the single “SDD 工件开发文档”. After the Feishu document exists, run `scripts/register_pctr_b_feishu_document.py` to write its URL/token and revision into the local document and sidecar. No per-feature Feishu SDD parent/target is required.

```powershell
python scripts/register_pctr_b_feishu_document.py <document.md> <state.json> `
  --feishu-url <development-document-url> `
  --revision <revision> `
  --out-document <document.md> `
  --out-state <state.json>
```

Do not create a planning-confirmation/acceptance document.

## 4. Write Table Summaries and Active-Feature Descriptions

For each feature:

1. Put a short planning-grounded summary in the feature table. Strip labels without content, raw URLs, Markdown images, HTML/XML tags, table markup, and media metadata.
2. Leave `1. 功能需求说明` empty while the feature is not the current design/development target.
3. For the current feature only, write one concise functional description followed by a small set of main functional points. Summarize; do not reproduce the source wording paragraph by paragraph.
4. Never place source images, tables, media links, citation tags, Feishu block markup, deletion markup, or copied source body text in the feature section.
5. Keep full source facts traceable through the source URL, revision, exact heading path, normalized source snapshot, and fingerprint. Separate unknowns from confirmed facts and never insert ACSDM/code recommendations into the requirement description.

Generate every feature from the complete planning outline in exact source order. A leaf/small heading is one feature; a large heading without children is one feature. Ignore truly empty headings only after confirming they contain no text, table, list, media, or child content. Put ACSDM/code recommendations only in `5. 优化建议` or the later role-based SDD.

Store the authored active-feature text in sidecar `requirement_description` so deterministic regeneration preserves it. Store `requirement_detail_fingerprint` as the fingerprint of the rendered section body, including the empty body for undeveloped features.

## 5. Generate the Lightweight Planner Confirmation Document

On `阅读这个功能生成策划确认文档`, PCTR-B creates the planner-facing confirmation artifact before any Orange SDD is generated.

Required sequence:

1. Resolve exactly one feature from the sidecar/development document. If the feature is ambiguous, stop.
2. Use sidecar `feishu_blocks` when available to read only the matched source planning section; otherwise read the smallest exported/source Markdown section that contains the exact heading path. Record source URL/revision and a feature-level hash.
3. Resolve the feature folder `.PCTR/<planning-version>/<FEATURE-ID>/`; create it if missing.
4. Ask ACSDM for related project rules, historical development docs, OUF link-index rows, and code-evidence indexes when ACSDM is available. Keep only compact paths/headings/facts; do not paste full ACSDM or OUF bodies.
5. Write or update exactly one decomposition file: `.PCTR/<planning-version>/<FEATURE-ID>/A-02-feature-decomposition.md`. Put the source snapshot/fingerprint, full functional understanding, functional breakdown, evidence index, real ambiguities, planner-facing confirmation/improvement items, and current status in this same file. Do not create another decomposition or source-snapshot Markdown file.
6. Render the planner-facing confirmation snapshot to `.PCTR/<planning-version>/<FEATURE-ID>/A-01-planner-confirmation-snapshot.md` from `assets/pctr-b-planner-confirmation-template.md`. Every ambiguity and confirmation/improvement item must contain two to six meaningful lettered preselection options, a separate recommended option code, a separate recommendation reason, and its own two-line reply block.
7. Do not automatically upload A-01. Return the local A-01 path and the exact target heading in the registered single Feishu development document. The user/program manually uploads the native `.md` file immediately below the matched feature's `2. SDD确认文档` heading, then runs the registration command with attachment token/URL/block and containing-document revision. Never create/import a separate Docx/Wiki document.
8. Update sidecar `planner_confirmation.status=pending`, feature artifact folder, A-01/A-02/B-01 paths, `feishu_blocks`, source revision, source snapshot hash, must-answer ambiguity IDs, confirmation item IDs, and sync time. Attachment name/token/block/URL and containing development-document revision are filled only after manual upload registration. Active `planner_confirmation.feishu_url` or any equivalent separate-document URL is forbidden.

The confirmation document must place the ambiguity list and confirmation/improvement list near the top, followed only by one short feature-demand description. Full functional understanding, functional breakdown, and later verification details stay in the local decomposition file. It must not contain a document-level reply section. Every ambiguity and every planner-facing confirmation/improvement item must contain its own lettered preselection list and reply code block immediately below the item detail. Use consecutive uppercase codes beginning with `A`; do not invent filler options. Write `推荐选择：<代码>` and `推荐原因：<原因>` as separate fields. Do not use a generic “其他” option as the only custom path: the planner may leave `选择：` empty and put an original rule in `补充：`.

Do not fabricate ambiguities. If no must-answer ambiguity exists, write `本轮未发现需要策划确认的歧义点。` and keep only useful non-must-answer confirmation/improvement items.

On `策划已确认`, parse each per-item reply code block and apply these rules:

1. `选择：` contains exactly one listed option code: valid; use `补充：` as an optional qualification.
2. `选择：` is empty and `补充：` is non-empty: valid custom planner solution; record it as `custom` and treat the supplement as the authoritative rule.
3. Both fields are empty: unanswered. A must-answer item blocks confirmation; an optional item remains unresolved/out of scope and must not be interpreted as accepting the recommendation.
4. `选择：` contains an unknown or multiple code where the item is not explicitly multi-select: invalid and requires revision, even when a supplement exists.

Update the decomposition with selected options and supplements, and set `planner_confirmation.status=confirmed` only when every must-answer ambiguity is validly answered. If any must-answer item is empty or invalid, set `needs_revision` and stop before SDD generation.

When the user issues `开始 <FEATURE-ID> 功能开发` while `planner_confirmation.status` is `missing`, `pending`, or `needs_revision`, enter this section instead of generating a plan or modifying code. Generate/update A-01 and A-02, provide the exact manual-upload target for A-01, and keep SDD generation, planning, and implementation locked until planner replies are synchronized.

## 6. Generate the Role-Based SDD in a Separate Orange Phase

PCTR-B and Orange may coexist when both gates are enabled. If Orange is disabled, PCTR-B may still prepare the feature ID and SDD request but must not invoke Orange. Detailed SDD generation requires `planner_confirmation.status=confirmed` and a current decomposition file.

Preferred same-session sequence when both are enabled:

1. Run `生成 PCTR-B 功能需求开发文档`; create the local development document and sidecar, upload/create the single Feishu development document, and register its URL/revision.
2. Run `阅读这个功能生成策划确认文档` for the target feature.
3. After planner replies, run `策划已确认`; PCTR-B updates the decomposition and unlocks SDD only if must-answer planner ambiguities are resolved.
4. In a later Orange task, pass the source planning URL/revision, exact heading path, and confirmed `A-02-feature-decomposition.md` to `pctr-b-feature-lookup-interface.md`. Provide the expected `B-01-runtime-sdd.md` path only when a PCTR-bound SDD snapshot is requested.
5. PCTR-B returns one lookup receipt containing the exact full/base Feature IDs, planning sequence, title, source identity, development-document link, sidecar path, feature artifact folder, confirmed decomposition identity, and B-01 output identity. The lookup is read-only.
6. Orange may generate its normal OUF artifacts under `docs/forge-artifacts/` and, when requested by the active workflow, also generate or export a PCTR-bound Draft SDD at `.PCTR/<planning-version>/<FEATURE-ID>/B-01-runtime-sdd.md`. Its metadata copies the exact lookup receipt fields and uses the confirmed `A-02-feature-decomposition.md` as its product-rule source.
7. Once the Draft SDD is structurally complete, Orange may immediately generate a linked implementation plan for joint review. The plan must be marked `Draft / pending-approval`, cite the exact Draft SDD path/hash, carry unresolved technical review decisions forward, and must not authorize code, Unity assets, or plan execution.
8. After static validation, register the OUF artifact paths/hashes in the PCTR sidecar using `register_pctr_b_ouf_artifact.py`.
9. If a PCTR-bound `B-01-runtime-sdd.md` exists, PCTR returns the local path and exact target feature heading for manual Feishu upload. After upload, `登记PCTR-B Markdown附件 <FEATURE-ID>` records attachment identity. Confirmation remains pending. Local review-plan generation does not require attachment registration.

If the PCTR-B development document, sidecar, Feishu document link, confirmed decomposition, planner confirmation, or source match is missing/ambiguous, stop before SDD generation. Never generate an unbound SDD and later guess its feature by title.

Fallback cross-task sequence when they are not enabled together:

1. Keep or export the PCTR-B feature ID, requirement description, confirmed `A-02-feature-decomposition.md` path, and expected `B-01-runtime-sdd.md` path.
2. Enable Orange Unity Forge in a later turn.
3. Generate one role-based Draft SDD at the expected `B-01-runtime-sdd.md` path. Its metadata must include the exact PCTR feature ID and confirmed decomposition identity.
4. Generate the linked `Draft / pending-approval` implementation plan and review/revise it together with the SDD.
5. Re-enable PCTR-B.
6. Register OUF artifact paths in PCTR, then upload any required `.md` manually and run `登记PCTR-B Markdown附件 <FEATURE-ID>`.

See `pctr-b-feature-lookup-interface.md` and `orange-sdd-handoff.md`.

## 7. Synchronize the Local Markdown Attachment

On the exact command `同步PCTR-B SDD <FEATURE-ID>`:

1. Read the feature and sidecar.
2. Find exactly one local SDD whose metadata feature ID matches.
3. Validate required role-based SDD headings, Draft/Approved status, source link, and feature ID.
4. Never create a Feishu Docx for the SDD. Do not automatically upload by default; return the exact matching feature block and local `.md` path for manual upload.
5. After the user/program uploads it, use `登记PCTR-B Markdown附件 <FEATURE-ID>`.
6. Write the local path, attachment name/token/URL, containing development-document revision, SDD status/version, and sync time into the feature section and sidecar.
7. Leave both confirmation checkboxes unchecked unless the user separately issues a confirmation command or the current Feishu revision already contains a valid manually selected state and synchronization is explicitly requested.

If zero or multiple SDDs match, stop and report candidates. Do not match by title alone when a feature ID is available.

## 8. Confirm or Return the Joint Review Package

- `<FEATURE-ID> SDD已确认` or `<FEATURE-ID> 程序已确认`: require the current local Markdown identity, confirmed decomposition, and no must-answer SDD decision. If the SDD is attached in Feishu, require a matching attachment reference and containing development-document revision; set sidecar `sdd_status=Approved`, `sdd_confirmation_status=confirmed`, and `program_confirmation.status=confirmed`. A linked plan may still remain pending approval.
- `<FEATURE-ID> 程序已确认，开始实施`: require the current local SDD and plan identities/hashes, confirmed decomposition, no blocking SDD or plan decision, and explicit implementation authority. Atomically set `sdd_status=Approved`, `sdd_confirmation_status=confirmed`, `program_confirmation.status=confirmed`, and `technical_plan_status=approved`, then enter implementation. Any stale identity or unresolved blocking decision stops the command before state or code changes.
- `<FEATURE-ID> SDD存在歧义需要修改`: select only the ambiguity checkbox; record the issue; set `sdd_confirmation_status=ambiguous`; keep plan approval and implementation locked. The existing review plan may be revised with the SDD but remains pending.

Exactly one checkbox may be selected after a decision. Both unchecked means pending. Both checked is invalid.

## 9. Generate the Implementation Plan

Generating the joint-review implementation plan through `开始 <FEATURE-ID> 功能开发` requires:

- `planner_confirmation.status=confirmed`;
- current local SDD path; if the SDD was attached or synchronized to Feishu, the attachment reference and containing development-document revision must also match;
- matching source revision;
- ACSDM and code evidence;
- no unresolved must-answer planner decision.

Generate the route-appropriate implementation plan locally, mark it `Draft / pending-approval`, cite the current Draft SDD identity, and write its path under `3. 实施计划工件的路径`. Copy unresolved technical/program review decisions into the plan as blocking review items; do not invent resolutions. The Draft SDD and pending plan are reviewed together. For small low-risk work, a short local implementation checklist may replace the full plan only when the user explicitly asks; cross-module, high-risk, save/protocol, architecture, SDK, or external-write work still requires a full plan. Do not upload implementation artifacts automatically.

Plan approval and implementation require the current SDD and plan identities, no blocking review item, `sdd_status=Approved`, `sdd_confirmation_status=confirmed`, and `technical_plan_status=approved`. These states may be set separately through the compatible commands or atomically through `<FEATURE-ID> 程序已确认，开始实施`.

## 10. Implement, Accept, and Record Bugs

Plan approval and implementation commands retain their existing meanings. PCTR-B keeps visible lifecycle data minimal:

- implementation evidence stays in the plan/implementation artifacts and ACSDM when recording is requested;
- every acceptance failure creates or updates a bug record file;
- append bug paths under `4. 功能 Bug 修复记录文件路径` without deleting earlier records;
- keep detailed state and acceptance rounds in the sidecar and bug artifacts, not as feature-table columns.

## 11. Feature-Level Feishu Read and OUF Link Update

Use this whenever the task is about one current feature:

1. Resolve the feature in the sidecar by full Feature ID, base Feature ID, or exact heading path.
2. If `feishu_blocks.planning_heading_block_id` and `planning_content_block_ids` are known, read only those blocks/that heading section from Feishu or from a current Markdown export.
3. Compute a feature-level content hash. If revision/hash did not change, reuse current A-01/A-02 and avoid regenerating confirmation content.
4. If the feature section changed, update only this feature folder and sidecar entry. Do not reread or regenerate unrelated features.
5. Run or refresh ACSDM's OUF link index when OUF artifacts changed, then register the matched OUF artifact paths in this feature's sidecar.

Sidecar fields used here: `feishu_blocks`, `source_fingerprint`, `source_snapshot_hash`, `ouf_artifacts`, and `last_sync_at`.

## 12. Update Mode

When the planning source changes:

1. compare source revision and heading fingerprints;
2. preserve exact source order and existing base IDs;
3. add new features with new base IDs and sequence-prefixed full IDs;
4. update full ID prefixes when source sequence changes while preserving base codes and legacy aliases;
5. mark removed source headings in the sidecar as pending removal until confirmed;
6. preserve SDD attachment references, confirmation decisions, plan paths, bug paths, work-hour cells, and human edits;
7. stop on concurrent conflicting edits.

## 13. Validate

Run:

```powershell
python scripts/validate_pctr_b_document.py <document.md>
python scripts/validate_pctr_b_state.py <document.md> <state.json>
```

Do not claim synchronization complete when either validator fails.
