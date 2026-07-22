# PCTR-B Workflow

## 1. Resolve Inputs

Collect the complete planning source, source revision, project root, output target, document code, Feishu development-document URL, local SDD root, implementation-plan root, bug-record root, and sidecar path.

Default artifact roots when the user does not specify them:

- SDD handoff: `CodexTemp/OrangeUnityForge/specs/`
- PCTR-B local document/state: `<project root>/.PCTR/B/<document-code>/`
- implementation plans: `<project root>/.PCTR/B/<document-code>/plans/`
- bug records: `<project root>/.PCTR/B/<document-code>/bugs/`

The local development document, sidecar, plan, and bug records are persistent PCTR artifacts. Never place them under `docs/` or `CodexTemp/PCTR/`. The Orange SDD handoff root remains Orange-owned working space and is referenced from PCTR rather than moved into PCTR storage.

## 2. Preserve the Planning Heading Framework

Read the source outline and preserve heading text and order exactly.

Feature boundary rule:

1. A heading with child headings is a grouping heading.
2. Each leaf/small heading is one feature requirement.
3. If a large heading has no child heading, that large heading is one feature requirement.
4. Do not atomically split one selected source heading into multiple visible feature sections.
5. Keep tables, lists, media references, conditions, and unresolved wording in the normalized source snapshot and source fingerprint. Do not copy them into the human development document.

Assign a hierarchical planning sequence to every heading from sibling order, including grouping headings. The first leaf under the first top-level group is `1.1`; a leaf under the second child of that group may be `1.2.1`.

Assign or preserve a base ID such as `<DOC-CODE>-F001`, then expose the full ID as `<planning-sequence>-<base-id>`, for example `1.1-XK5A-SAVE-F003`. Preserve `base_feature_id` and prior full IDs in `legacy_feature_ids`. If source order changes, update the sequence prefix but never reassign the base code to a different source feature.

## 3. Create the Single SDD Artifact Development Document

Use `assets/pctr-b-development-document-template.md` and `assets/pctr-b-feature-template.md`.

Create:

- document location metadata;
- one five-column feature table using exactly `功能编码 / 策案标题 / 策案标题路径 / 功能需求说明 / 工时`;
- one feature section per selected source heading;
- one local sidecar manifest using `assets/pctr-b-state.example.json` as the schema example.

The table requirement cell is a concise planning-grounded summary with markup and media removed. The matching `1. 功能需求说明` body is empty for an undeveloped feature. When a feature becomes the current design/development target, author a short functional description plus main functional points from the complete source section. Never paste source paragraphs, tables, images, media URLs, citations, or Feishu XML/HTML markup into the body.

Then use the `lark-doc` Markdown creation/import workflow to create the single Feishu “SDD 工件开发文档” under the configured parent. After creation, run `scripts/register_pctr_b_feishu_document.py` to write its URL/token and revision into the local document and sidecar. No per-feature Feishu SDD parent/target is required.

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
2. Read the matched source planning section and record the source URL/revision.
3. Save the raw source snapshot to `.PCTR/B/<document-code>/snapshots/<FEATURE-ID>-source-snapshot.md`.
4. Ask ACSDM for related project rules, historical development docs, and code-evidence indexes when ACSDM is available. Keep only compact paths/headings/facts; do not paste full ACSDM bodies.
5. Write `.PCTR/B/<document-code>/decompositions/<FEATURE-ID>-planning-decomposition.md` with the full functional understanding, functional breakdown, evidence index, real ambiguities, planner-facing confirmation/improvement items, and current status.
6. Render `.PCTR/B/<document-code>/confirmations/<FEATURE-ID>-planner-confirmation.md` from `assets/pctr-b-planner-confirmation-template.md`. Upload to Feishu only when the user explicitly asks.
7. Update sidecar `planner_confirmation.status=pending`, paths, source revision, source snapshot hash, must-answer ambiguity IDs, and confirmation item IDs.

The confirmation document must place the ambiguity list and confirmation/improvement list near the top, followed only by one short feature-demand description. Full functional understanding, functional breakdown, and later verification details stay in the local decomposition file. It must not contain a document-level reply section. Every ambiguity and every planner-facing confirmation/improvement item must contain its own reply code block immediately below the item detail.

Do not fabricate ambiguities. If no must-answer ambiguity exists, write `本轮未发现需要策划确认的歧义点。` and keep only useful non-must-answer confirmation/improvement items.

On `策划已确认`, parse each per-item reply code block, update the decomposition with selected options and supplements, and set `planner_confirmation.status=confirmed` only when every must-answer ambiguity is answered. If any must-answer item is empty or invalid, set `needs_revision` and stop before SDD generation.

## 6. Generate the Role-Based SDD in a Separate Orange Phase

PCTR-B and Orange may coexist when both gates are enabled. If Orange is disabled, PCTR-B may still prepare the feature ID and SDD request but must not invoke Orange. Detailed SDD generation requires `planner_confirmation.status=confirmed` and a current decomposition file.

Preferred same-session sequence when both are enabled:

1. Run `生成 PCTR-B 功能需求开发文档`; create the local development document and sidecar, upload/create the single Feishu development document, and register its URL/revision.
2. Run `阅读这个功能生成策划确认文档` for the target feature.
3. After planner replies, run `策划已确认`; PCTR-B updates the decomposition and unlocks SDD only if must-answer planner ambiguities are resolved.
4. In a later Orange task, pass the source planning URL/revision, exact heading path, and confirmed decomposition path to `pctr-b-feature-lookup-interface.md`.
5. PCTR-B returns one lookup receipt containing the exact full/base Feature IDs, planning sequence, title, source identity, development-document link, sidecar path, and confirmed decomposition identity. The lookup is read-only.
6. Orange generates the Context Brief and one role-based Draft SDD whose metadata copies the exact lookup receipt fields and uses the confirmed decomposition as its product-rule source.
7. After static SDD validation, Orange calls the PCTR-B Markdown-attachment handoff interface.
8. The interface attaches the local `.md` file directly inside the matching feature section only when exact-position insertion can be verified. Otherwise it returns a manual-upload handoff and does not create another Feishu document. Confirmation remains pending.

If the PCTR-B development document, sidecar, Feishu document link, confirmed decomposition, planner confirmation, or source match is missing/ambiguous, stop before SDD generation. Never generate an unbound SDD and later guess its feature by title.

Fallback cross-task sequence when they are not enabled together:

1. Keep or export the PCTR-B feature ID, requirement description, and confirmed decomposition path.
2. Enable Orange Unity Forge in a later turn.
3. Generate one role-based Draft SDD whose metadata includes the exact PCTR feature ID and confirmed decomposition identity.
4. Review and revise the SDD.
5. Re-enable PCTR-B.
6. Run `同步PCTR-B SDD <FEATURE-ID>` to attempt exact-position attachment, or upload the `.md` manually and run `登记PCTR-B Markdown附件 <FEATURE-ID>`.

See `pctr-b-feature-lookup-interface.md` and `orange-sdd-handoff.md`.

## 7. Synchronize the Local Markdown Attachment

On the exact command `同步PCTR-B SDD <FEATURE-ID>`:

1. Read the feature and sidecar.
2. Find exactly one local SDD whose metadata feature ID matches.
3. Validate required role-based SDD headings, Draft/Approved status, source link, and feature ID.
4. Never create a Feishu Docx for the SDD. If the available Feishu workflow can insert the file attachment under the exact matching feature block and verify the resulting block, attach the local `.md` there.
5. If exact-position insertion or callout preservation is unreliable, stop before external write, keep the local path/code block, and return concise manual-upload instructions. After the user uploads it, use `登记PCTR-B Markdown附件 <FEATURE-ID>`.
6. Write the local path, attachment name/token/URL, containing development-document revision, SDD status/version, and sync time into the feature section and sidecar.
7. Leave both confirmation checkboxes unchecked unless the user separately issues a confirmation command or the current Feishu revision already contains a valid manually selected state and synchronization is explicitly requested.

If zero or multiple SDDs match, stop and report candidates. Do not match by title alone when a feature ID is available.

## 8. Confirm or Return the SDD

- `<FEATURE-ID> SDD已确认` or `<FEATURE-ID> 程序已确认`: require the current local Markdown identity, confirmed decomposition, and no must-answer SDD decision. If the SDD is attached in Feishu, require a matching attachment reference and containing development-document revision; set sidecar `sdd_status=Approved`, `sdd_confirmation_status=confirmed`, and `program_confirmation.status=confirmed`.
- `<FEATURE-ID> SDD存在歧义需要修改`: select only the ambiguity checkbox; record the issue; set `sdd_confirmation_status=ambiguous`; keep planning locked.

Exactly one checkbox may be selected after a decision. Both unchecked means pending. Both checked is invalid.

## 9. Generate the Implementation Plan

`开始 <FEATURE-ID> 功能开发` requires:

- `planner_confirmation.status=confirmed`;
- `sdd_confirmation_status=confirmed` or explicit programmer confirmation recorded for the current local SDD;
- current local SDD path; if the SDD was attached or synchronized to Feishu, the attachment reference and containing development-document revision must also match;
- matching source revision;
- ACSDM and code evidence;
- no unresolved must-answer decision.

Generate the route-appropriate implementation plan locally and write its path under `3. 实施计划工件的路径`. For small low-risk work where the user says `程序已确认，开始实施`, a short local implementation checklist may replace the full plan; cross-module, high-risk, save/protocol, architecture, SDK, or external-write work still requires a full plan and approval. Do not upload implementation artifacts automatically.

## 10. Implement, Accept, and Record Bugs

Plan approval and implementation commands retain their existing meanings. PCTR-B keeps visible lifecycle data minimal:

- implementation evidence stays in the plan/implementation artifacts and ACSDM when recording is requested;
- every acceptance failure creates or updates a bug record file;
- append bug paths under `4. 功能 Bug 修复记录文件路径` without deleting earlier records;
- keep detailed state and acceptance rounds in the sidecar and bug artifacts, not as feature-table columns.

## 11. Update Mode

When the planning source changes:

1. compare source revision and heading fingerprints;
2. preserve exact source order and existing base IDs;
3. add new features with new base IDs and sequence-prefixed full IDs;
4. update full ID prefixes when source sequence changes while preserving base codes and legacy aliases;
5. mark removed source headings in the sidecar as pending removal until confirmed;
6. preserve SDD attachment references, confirmation decisions, plan paths, bug paths, work-hour cells, and human edits;
7. stop on concurrent conflicting edits.

## 12. Validate

Run:

```powershell
python scripts/validate_pctr_b_document.py <document.md>
python scripts/validate_pctr_b_state.py <document.md> <state.json>
```

Do not claim synchronization complete when either validator fails.
