# PCTR-B Output Schema

## Human Document

The Feishu-facing development document contains only:

1. title;
2. `文档定位`;
3. `功能总表`;
4. feature sections in exact source order.

### Document Location

Record:

- PCTR mode (`B`);
- source planning link/token and revision;
- this document link/token and revision;
- Feishu parent/folder used for automatic SDD creation;
- project root;
- document code;
- local sidecar path;
- SDD, plan, and bug artifact roots;
- last synchronization time.

### Feature Table

Use exactly these columns unless the user explicitly adds a non-status column:

| 功能编码 | 策案标题 | 策案标题路径 | 功能需求说明 | SDD 确认文档 | 实施计划工件路径 | Bug 修复记录文件路径 | 优化建议 |
|---|---|---|---|---|---|---|---|

Forbidden columns:

- 源策划进度
- 策划确认
- 开发状态
- 验收状态
- any renamed equivalent whose main purpose is lifecycle status

### Feature Section

Each feature uses the exact source title in the heading and exactly these numbered second-level contents beneath it:

1. `功能需求说明`
2. `SDD确认文档`
3. `实施计划工件的路径`
4. `功能 Bug 修复记录文件路径`
5. `优化建议`

On initial one-click generation, the body under `1. 功能需求说明` must be empty. Do not auto-copy or summarize the planning正文. The source URL/revision, exact heading path, and sidecar fingerprint preserve traceability until a human explicitly fills that section.

Under SDD confirmation, include:

```markdown
- 本地 SDD 工件：
- 飞书 SDD 文档：
- SDD 状态 / Revision：
- 确认状态：
  - [ ] 已确认
  - [ ] 存在歧义需要修改
```

The two checkboxes are mutually exclusive.

## Sidecar Manifest

The sidecar is machine state, not a second human document. Store:

```json
{
  "schema_version": 1,
  "mode": "B",
  "document_code": "EXAMPLE",
  "source": {"url": "", "revision": -1},
  "development_document": {"url": "", "revision": -1, "local_path": "", "feishu_parent_url": ""},
  "features": [
    {
      "feature_id": "EXAMPLE-F001",
      "source_heading": "",
      "source_heading_path": "",
      "source_fingerprint": "",
      "sdd_local_path": "",
      "sdd_feishu_url": "",
      "sdd_revision": -1,
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

`sdd_confirmation_status=confirmed` requires `sdd_status=Approved`.

## Source Authority

- Planning source: feature title/order and planning facts.
- Uploaded role-based SDD: planner/program/QA confirmation content for one feature.
- Single development document: human index and artifact navigation.
- Sidecar: machine synchronization and gate state.
- ACSDM: project rules, code evidence, and optional implementation/bug/completion records.
