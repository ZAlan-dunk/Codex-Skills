# PCTR-B Output Schema

## Human Document

PCTR-B creates exactly one Feishu-facing development document containing:

1. title;
2. `文档定位`;
3. `功能总表`;
4. feature sections in exact source order.

Do not create one Feishu SDD document per feature. Each role-based SDD remains a local Markdown file and is attached inside the matching feature section of this one document.

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

The local development document and sidecar must live under `<project root>/.PCTR/B/<document-code>/`; plan and bug roots must be descendants of the same directory. `docs/` is not a valid PCTR output root. `CodexTemp/OrangeUnityForge/` may appear only as the external Orange-owned SDD/brief handoff location.

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

<在此处直接插入本地 Markdown 文件附件；自动插入不可靠时由用户手动上传>

> 🏕️ SDD 状态 / Revision：

> ✍️ 确认状态：
>
> - [ ] 已确认
> - [ ] 存在歧义需要修改
````

The two checkboxes are mutually exclusive.

`3. 实施计划工件的路径` uses a plain-text code block. `4. 功能 Bug 修复记录文件路径` uses a four-column Bug table with at least two initially empty numbered rows. The Feishu version uses orange callouts for the three highlighted SDD blocks. If exact styling or exact-position attachment cannot be verified through the current IDE/CLI path, stop before the write and let the user upload/format manually.

## Sidecar Manifest

The sidecar is machine state, not a second human document. Store:

```json
{
  "schema_version": 2,
  "mode": "B",
  "document_code": "EXAMPLE",
  "source": {"url": "", "revision": -1},
  "development_document": {"url": "", "revision": -1, "local_path": ""},
  "features": [
    {
      "feature_id": "1.1-EXAMPLE-F001",
      "base_feature_id": "EXAMPLE-F001",
      "legacy_feature_ids": ["EXAMPLE-F001"],
      "planning_sequence": "1.1",
      "source_heading": "",
      "source_heading_path": "",
      "source_fingerprint": "",
      "requirement_summary": "",
      "requirement_description": "",
      "requirement_detail_fingerprint": "",
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

Allowed `sdd_confirmation_status`: `pending`, `confirmed`, `ambiguous`.

`sdd_confirmation_status=confirmed` requires `sdd_status=Approved`, a non-empty local SDD path, an attachment token or URL, and a non-negative containing development-document revision.

## Source Authority

- Planning source: feature title/order and planning facts.
- Single development document: concise table summaries, optional active-feature description/main points, confirmation surface, attachment placement, and artifact navigation.
- Local role-based SDD Markdown attachment: planner/program/QA confirmation content for one feature.
- Sidecar: machine synchronization, aliases, attachment identity, and gate state.
- ACSDM: project rules, code evidence, and optional implementation/bug/completion records.
