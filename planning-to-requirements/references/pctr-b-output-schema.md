# PCTR-B Output Schema

## Human Document

PCTR-B creates exactly one Feishu-facing development document containing:

1. title;
2. `文档定位`;
3. `功能总表`;
4. feature sections in exact source order.

Do not create one Feishu planner-confirmation or SDD document per feature. Each A-01 planner confirmation and any PCTR-bound B-01 role-based SDD remains a local Markdown file. Upload to Feishu is manual by default; PCTR records the attachment identity after upload.

### Document Location

Record:

- PCTR mode (`B`);
- source planning link/token and revision;
- this document link/token and revision;
- project root;
- document code;
- local sidecar path;
- SDD, plan, and bug artifact roots;
- last synchronization time.

The local development document and sidecar must live under `<project root>/.PCTR/<planning-version>/`, for example `.PCTR/M032v1.2/`. Every feature must have one direct child folder named by its full Feature ID, for example `.PCTR/M032v1.2/1.2.1-XK5A-SAVE-F004/`. `docs/` and `CodexTemp/PCTR/` are not valid PCTR output roots.

### Feature ID

Use `<策案层级序号>-<原功能编码>`, for example `1.1-XK5A-SAVE-F003`.

- Derive the hierarchical sequence from source-outline sibling order, including grouping headings.
- Preserve the original code as `base_feature_id` and every previous full ID in `legacy_feature_ids`.
- A source reorder may change the full sequence-prefixed ID, but the base code must never be reassigned.

### Feature Table

Use exactly these columns, matching the current Feishu baseline:

| 功能编码 | 策案标题 | 策案标题路径 | 功能需求说明 | 工时 |
|---|---|---|---|---|

`功能需求说明` is a concise planning-grounded summary. It must not contain source images, media URLs, HTML/XML tags, Markdown tables, or copied long-form source text. Leave `工时` blank unless a human provides it.

Forbidden columns:

- 源策划进度
- 策划确认
- 开发状态
- 验收状态
- any renamed equivalent whose main purpose is lifecycle status
- SDD 确认文档
- 实施计划工件路径
- Bug 修复记录文件路径
- 优化建议

### Feature Section

Each feature uses the exact source title in the heading and exactly these numbered second-level contents beneath it:

1. `功能需求说明`
2. `SDD确认文档`
3. `实施计划工件的路径`
4. `功能 Bug 修复记录文件路径`
5. `优化建议`

On initial one-click generation, leave the body under `1. 功能需求说明` empty. An undeveloped feature may remain empty. When the feature becomes the current design/development target, write only:

1. one concise functional description;
2. a short `主要功能点` list.

Do not copy source paragraphs, images, tables, media URLs, citations, deletion markup, or Feishu XML/HTML blocks into this section. Do not insert ACSDM/code recommendations into this section. Preserve full source traceability through source identity, revision, heading path, normalized source snapshot, and fingerprints instead.

Under SDD confirmation, match the Feishu `XK5A-SAVE-F001 关卡存档` block pattern:

````markdown
> 🍞 本地 SDD 工件：

`路径：`

```text
<local-markdown-path>
```

<用户/程序在此处手动上传本地 Markdown 文件附件；PCTR随后登记附件身份>

> 🏕️ SDD 状态 / Revision：

> ✍️ 确认状态：
>
> - [ ] 已确认
> - [ ] 存在歧义需要修改
````

When planner confirmation exists, insert this block immediately after the `2. SDD确认文档` heading and before the detailed SDD block:

````markdown
**策划确认 Markdown 附件（A-01，待策划逐项回复）：**

<attach `.PCTR/<planning-version>/<FEATURE-ID>/A-01-planner-confirmation-snapshot.md` here as a native file block>
````

The A-01 file block must be inside the exact matched feature section. Upload is manual by default. A separate Docx/Wiki URL is invalid.

The two checkboxes are mutually exclusive.

`3. 实施计划工件的路径` uses a plain-text code block. `4. 功能 Bug 修复记录文件路径` uses a four-column Bug table with at least two initially empty numbered rows. The Feishu version uses orange callouts for the three highlighted SDD blocks. PCTR should output the local path and exact target heading; the user/program uploads or formats the Feishu attachment manually, then PCTR registers the result.

## Planner Confirmation and Decomposition

PCTR-B uses a lightweight per-feature planner confirmation document before OUF SDD generation. It is not the same as the role-based SDD.

Default paths:

```text
.PCTR/<planning-version>/
.PCTR/<planning-version>/<FEATURE-ID>/A-01-planner-confirmation-snapshot.md
.PCTR/<planning-version>/<FEATURE-ID>/A-02-feature-decomposition.md
.PCTR/<planning-version>/<FEATURE-ID>/B-01-runtime-sdd.md
```

OUF-owned artifacts are not stored in this feature folder unless the active workflow explicitly exports a PCTR-bound B-01 snapshot. OUF native Context Brief / SDD / Plan / Report / Evidence files stay under `docs/forge-artifacts/` and are linked in the sidecar.

The `A-` prefix is reserved for planner-facing confirmation and the single living decomposition file. A feature folder must contain exactly two `A-*.md` artifacts. Do not create `snapshots/`, `decompositions/`, or `confirmations/` subfolders for PCTR-B feature artifacts. Put source snapshot/fingerprint content inside `A-02-feature-decomposition.md` instead of creating another Markdown file.

The planner confirmation document must contain:

1. a top ambiguity list;
2. a top planner-facing confirmation/improvement list;
3. one short feature-demand description;
4. detail sections for every ambiguity and confirmation/improvement item;
5. two to six meaningful lettered preselection options under every reply-bearing item, using consecutive uppercase codes beginning with `A`;
6. a separate `推荐选择：<代码>` and `推荐原因：<原因>` under every reply-bearing item;
7. one reply code block immediately under each item detail, using exactly two fields: `选择：` and `补充：`;
8. compact evidence index marked as planner-optional.

Reply validity:

- one listed option code in `选择：`: valid;
- empty `选择：` plus non-empty `补充：`: valid custom planner solution, stored as `custom`, with the supplement as the authoritative rule;
- both fields empty: unanswered; it blocks only a `must_answer` item, and never means the recommendation was accepted;
- unknown or multiple option codes for a single-select item: invalid and requires revision;
- a valid listed code plus `补充：`: the supplement narrows or qualifies the selected option and must be preserved verbatim.

Full functional understanding and functional breakdown must stay in the local decomposition file, not in the planner confirmation document.

Forbidden in the planner confirmation document:

- a document-level reply section;
- a reply-bearing item with no concrete lettered preselection list;
- a combined recommendation sentence that does not identify both the recommended code and a separate reason;
- a generic “其他” option used as a substitute for the supported empty-selection/non-empty-supplement custom reply;
- fabricated ambiguity points;
- long ACSDM body copies;
- source planning prose copied paragraph by paragraph;
- implementation code drafts or long class/file lists unless they are necessary evidence;
- full functional understanding or full functional breakdown sections.

Allowed item statuses: `must_answer`, `optional`, `resolved`, `needs_revision`.

## Sidecar Manifest

The sidecar is machine state, not a second human document. Store:

```json
{
  "schema_version": 3,
  "mode": "B",
  "planning_version": "M032v1.2",
  "document_code": "XK5A-SAVE",
  "artifact_root": "C:/Project/.PCTR/M032v1.2",
  "source": {
    "url": "",
    "revision": -1
  },
  "development_document": {
    "url": "",
    "revision": -1,
    "local_path": "C:/Project/.PCTR/M032v1.2/M032v1.2-PCTR-B-development-document.md",
    "last_sync_at": ""
  },
  "features": [
    {
      "feature_id": "1.2.1-XK5A-SAVE-F004",
      "base_feature_id": "XK5A-SAVE-F004",
      "legacy_feature_ids": [
        "XK5A-SAVE-F004"
      ],
      "planning_sequence": "1.2.1",
      "source_heading": "Feature title",
      "source_heading_path": "Parent / Feature title",
      "source_fingerprint": "",
      "feature_artifact_dir": "C:/Project/.PCTR/M032v1.2/1.2.1-XK5A-SAVE-F004",
      "artifact_paths": {
        "planner_confirmation_snapshot": "C:/Project/.PCTR/M032v1.2/1.2.1-XK5A-SAVE-F004/A-01-planner-confirmation-snapshot.md",
        "decomposition": "C:/Project/.PCTR/M032v1.2/1.2.1-XK5A-SAVE-F004/A-02-feature-decomposition.md",
        "runtime_sdd": "C:/Project/.PCTR/M032v1.2/1.2.1-XK5A-SAVE-F004/B-01-runtime-sdd.md"
      },
      "requirement_summary": "",
      "requirement_description": "",
      "requirement_detail_fingerprint": "",
      "source_snapshot_path": "C:/Project/.PCTR/M032v1.2/1.2.1-XK5A-SAVE-F004/A-02-feature-decomposition.md",
      "source_snapshot_hash": "",
      "feishu_blocks": {
        "planning_heading_block_id": "",
        "planning_content_block_ids": [],
        "development_feature_heading_block_id": "",
        "development_sdd_heading_block_id": "",
        "last_planning_revision_checked": -1,
        "last_development_revision_checked": -1
      },
      "planner_confirmation": {
        "status": "missing",
        "local_path": "C:/Project/.PCTR/M032v1.2/1.2.1-XK5A-SAVE-F004/A-01-planner-confirmation-snapshot.md",
        "attachment_name": "",
        "attachment_token": "",
        "attachment_block_id": "",
        "attachment_feature_id": "",
        "attachment_heading_block_id": "",
        "attachment_url": "",
        "attachment_document_revision": -1,
        "must_answer_ambiguities": [],
        "confirmation_items": [],
        "resolved_decisions": []
      },
      "decomposition_path": "C:/Project/.PCTR/M032v1.2/1.2.1-XK5A-SAVE-F004/A-02-feature-decomposition.md",
      "decomposition_hash": "",
      "ouf_artifacts": {
        "artifact_root": "docs/forge-artifacts",
        "context_briefs": [],
        "sdds": [],
        "plans": [],
        "reports": [],
        "evidence": [],
        "logs": [],
        "other": [],
        "last_linked_at": "",
        "linked_by": "ACSDM OUF Link Index"
      },
      "sdd_generation": {
        "status": "locked",
        "input_decomposition_path": "C:/Project/.PCTR/M032v1.2/1.2.1-XK5A-SAVE-F004/A-02-feature-decomposition.md",
        "output_sdd_path": "C:/Project/.PCTR/M032v1.2/1.2.1-XK5A-SAVE-F004/B-01-runtime-sdd.md",
        "generated_by": "",
        "generated_at": ""
      },
      "program_confirmation": {
        "status": "pending",
        "reviewer": "",
        "confirmed_at": "",
        "open_items": []
      },
      "sdd_local_path": "",
      "sdd_attachment_name": "",
      "sdd_attachment_token": "",
      "sdd_attachment_url": "",
      "sdd_attachment_document_revision": -1,
      "sdd_version": "",
      "sdd_status": "",
      "sdd_confirmation_status": "pending",
      "implementation_plan_path": "",
      "bug_record_paths": [],
      "last_sync_at": ""
    }
  ]
}
```

Allowed `planner_confirmation.status`: `missing`, `pending`, `confirmed`, `needs_revision`. Allowed `sdd_generation.status`: `locked`, `ready`, `draft`, `approved`. Allowed `program_confirmation.status`: `pending`, `confirmed`, `needs_revision`.

For any planner-confirmation status other than `missing`, `attachment_name` may remain empty until manual upload registration. After registration, it must equal `A-01-planner-confirmation-snapshot.md`; `attachment_token`/`attachment_block_id`/`attachment_url` identify the native Markdown file block; `attachment_feature_id` must equal the containing feature; `attachment_heading_block_id` must identify that feature's exact `2. SDD确认文档` heading; and `attachment_document_revision` must be non-negative. `feishu_url`, `document_url`, or any equivalent per-feature planner-confirmation document field is forbidden.

Allowed `sdd_confirmation_status`: `pending`, `confirmed`, `ambiguous`.

`sdd_confirmation_status=confirmed` requires `sdd_status=Approved`, a non-empty current local SDD path, and explicit programmer/user approval. A Feishu SDD attachment is optional for local joint approval and implementation. If any SDD attachment field is registered, `sdd_attachment_name` must equal `B-01-runtime-sdd.md`, a token or URL must be present, and the containing development-document revision must be non-negative and current.

## Source Authority

- Planning source: feature title/order and planning facts.
- Single development document: concise table summaries, optional active-feature description/main points, confirmation surface, attachment placement, and artifact navigation.
- Local `A-02-feature-decomposition.md`: the unique product-rule context package for one feature.
- Local `B-01-runtime-sdd.md`: optional PCTR-bound detailed role-based SDD snapshot for one feature; it is generated from the confirmed `A-02-feature-decomposition.md` when the workflow needs that file.
- OUF `docs/forge-artifacts/`: OUF-owned Context Brief / SDD / Plan / Report / Evidence files; PCTR links them by path/hash and does not copy or restrict them.
- Sidecar: machine synchronization, aliases, Feishu block locators, OUF artifact links, attachment identity, and gate state.
- ACSDM: project rules, code evidence, OUF link index, and optional implementation/bug/completion records.
