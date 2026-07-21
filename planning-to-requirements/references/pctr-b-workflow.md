# PCTR-B Workflow

## 1. Resolve Inputs

Collect the planning source, source revision, project root, output target, document code, Feishu development-document URL, Feishu SDD parent/folder location, local SDD root, implementation-plan root, bug-record root, and sidecar path.

Default artifact roots when the user does not specify them:

- SDD handoff: `CodexTemp/OrangeUnityForge/specs/`
- PCTR-B local document/state: `CodexTemp/PCTR/B/`
- implementation plans: `CodexTemp/PCTR/B/plans/`
- bug records: `CodexTemp/PCTR/B/bugs/`

## 2. Preserve the Planning Heading Framework

Read the source outline and preserve heading text and order exactly.

Feature boundary rule:

1. A heading with child headings is a grouping heading.
2. Each leaf/small heading is one feature requirement.
3. If a large heading has no child heading, that large heading is one feature requirement.
4. Do not atomically split one selected source heading into multiple visible feature sections.
5. Keep tables, lists, media references, conditions, and unresolved wording under the selected source heading.

Assign stable IDs such as `<DOC-CODE>-F001`. Preserve existing IDs across source revisions. New inserted features receive the next unused ID; document order follows the source even when numeric IDs no longer sort sequentially.

## 3. Create the Single SDD Artifact Development Document

Use `assets/pctr-b-development-document-template.md` and `assets/pctr-b-feature-template.md`.

Create:

- document location metadata;
- one compact feature table without progress/status columns;
- one feature section per selected source heading;
- one local sidecar manifest using `assets/pctr-b-state.example.json` as the schema example.

Then use the `lark-doc` Markdown creation/import workflow to create the Feishu “SDD 工件开发文档” under the configured parent. After creation, run `scripts/register_pctr_b_feishu_document.py` to write its URL/token, revision, and one unambiguous per-feature SDD parent/target into the local document and sidecar. If the parent or target is missing/ambiguous, stop before external write and do not report the PCTR-B setup complete.

```powershell
python scripts/register_pctr_b_feishu_document.py <document.md> <state.json> `
  --feishu-url <development-document-url> `
  --revision <revision> `
  --sdd-parent-url <sdd-parent-or-target-url> `
  --out-document <document.md> `
  --out-state <state.json>
```

Do not create a planning-confirmation/acceptance document.

## 4. Reserve Empty Requirement Descriptions

For each feature, create the `1. 功能需求说明` heading and leave its body empty. Do not copy, summarize, or infer the planning正文 into this section during one-click document generation. The planning source remains the authority and the sidecar fingerprint tracks source changes.

Generate every feature from the complete planning outline in exact source order. A leaf/small heading is one feature; a large heading without children is one feature. Ignore empty headings. Put ACSDM/code recommendations and unresolved issues only in `5. 优化建议` or the later role-based SDD; never write them into the empty requirement-description section automatically.

## 5. Generate the Role-Based SDD in a Separate Orange Phase

PCTR-B and Orange may coexist when both gates are enabled. If Orange is disabled, PCTR-B may still prepare the feature ID and SDD request but must not invoke Orange.

Preferred same-session sequence when both are enabled:

1. Run `生成 PCTR-B 功能需求开发文档`; create the local development document and sidecar, upload/create the Feishu development document, and register its URL plus one unambiguous SDD parent/target.
2. In a later Orange task, pass the source planning URL/revision and exact heading path to `pctr-b-feature-lookup-interface.md`.
3. PCTR-B returns one lookup receipt containing the exact Feature ID, title, source identity, development-document link, sidecar path, and Feishu SDD target. The lookup is read-only.
4. Orange generates the Context Brief and one role-based Draft SDD whose metadata copies the exact lookup receipt fields.
5. After static SDD validation, Orange automatically calls the PCTR-B upload handoff interface.
6. The interface uploads the SDD and links it to the matching feature in the Feishu development document with confirmation still pending.

If the PCTR-B development document, sidecar, Feishu document link, source match, or target is missing/ambiguous, stop before SDD generation. Never generate an unbound SDD and later guess its feature by title.

Fallback cross-task sequence when they are not enabled together:

1. Keep or export the PCTR-B feature ID and requirement description.
2. Enable Orange Unity Forge in a later turn.
3. Generate one role-based Draft SDD whose metadata includes the exact PCTR feature ID.
4. Review and revise the SDD.
5. Re-enable PCTR-B.
6. Run `同步PCTR-B SDD <FEATURE-ID>` or use the narrow upload fallback when configured.

See `pctr-b-feature-lookup-interface.md` and `orange-sdd-handoff.md`.

## 6. Synchronize and Upload the SDD

On the exact command `同步PCTR-B SDD <FEATURE-ID>`:

1. Read the feature and sidecar.
2. Find exactly one local SDD whose metadata feature ID matches.
3. Validate required role-based SDD headings, Draft/Approved status, source link, and feature ID.
4. Use the `lark-doc` workflow to create/upload a Feishu Docx from Markdown.
5. Write the local path, Feishu URL/token, SDD revision/status, and sync time into the feature section and sidecar.
6. Leave both confirmation checkboxes unchecked unless the user separately issues a confirmation command or the current Feishu revision already contains a valid manually selected state and synchronization is explicitly requested.

If zero or multiple SDDs match, stop and report candidates. Do not match by title alone when a feature ID is available.

## 7. Confirm or Return the SDD

- `<FEATURE-ID> SDD已确认`: require an uploaded Feishu SDD, current revision, and no blocking pending decision; set the SDD status to `Approved`, select only `已确认`, and set sidecar `sdd_status=Approved`, `sdd_confirmation_status=confirmed`.
- `<FEATURE-ID> SDD存在歧义需要修改`: select only the ambiguity checkbox; record the issue; set `sdd_confirmation_status=ambiguous`; keep planning locked.

Exactly one checkbox may be selected after a decision. Both unchecked means pending. Both checked is invalid.

## 8. Generate the Implementation Plan

`开始 <FEATURE-ID> 功能开发` requires:

- `sdd_confirmation_status=confirmed`;
- current SDD Feishu URL/revision;
- matching source revision;
- ACSDM and code evidence;
- no unresolved blocking decision.

Generate the route-appropriate implementation plan locally and write its path under `3. 实施计划工件的路径`. Do not upload it automatically. Program upload remains manual unless explicitly requested.

## 9. Implement, Accept, and Record Bugs

Plan approval and implementation commands retain their existing meanings. PCTR-B keeps visible lifecycle data minimal:

- implementation evidence stays in the plan/implementation artifacts and ACSDM when recording is requested;
- every acceptance failure creates or updates a bug record file;
- append bug paths under `4. 功能 Bug 修复记录文件路径` without deleting earlier records;
- keep detailed state and acceptance rounds in the sidecar and bug artifacts, not as feature-table columns.

## 10. Update Mode

When the planning source changes:

1. compare source revision and heading fingerprints;
2. preserve exact order and existing IDs;
3. add new features with new IDs;
4. mark removed source headings in the sidecar as pending removal until confirmed;
5. preserve SDD links, confirmation decisions, plan paths, bug paths, and human edits;
6. stop on concurrent conflicting edits.

## 11. Validate

Run:

```powershell
python scripts/validate_pctr_b_document.py <document.md>
python scripts/validate_pctr_b_state.py <document.md> <state.json>
```

Do not claim synchronization complete when either validator fails.
