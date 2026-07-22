# ACSDM Index Schema

## Catalog Root

The catalog root is always:

```text
<project root>/.ACSDM
```

Do not store only a pointer file in `.ACSDM`. The folders and indexes below live directly inside `.ACSDM`.

This is ACSDM's exclusive persistent root. New ACSDM content must not be written to `<project root>/docs/`, which is reserved for Orange Unity Forge. Links to PCTR artifacts should use `.PCTR/A/...` or `.PCTR/B/...`; old `docs/...` links may remain only as labeled historical evidence.

## Standard Modules

ACSDM creates eight generic modules by default. Project-specific modules can be added later, but these eight are the baseline.

| Folder | Purpose | Index |
|---|---|---|
| `00Rule` | Project architecture, project rules, self-developed framework rules, Lua/C# interaction, and global conventions that differ from normal practice. | `0000Index.md` |
| `01ProjectOverview` | Game/project overview, gameplay rules, major systems, trunk scripts, and quick navigation. | `0100Index.md` |
| `02LevelEditor` | Level editor, editor tools, generation notes, editor workflow, and editor logs. | `0200Index.md` |
| `03LevelLoading` | Level loading chain, map loading, block loading, preview loading, and loading optimization. | `0300Index.md` |
| `04PlayerInput` | User input, drag/fill, gestures, interaction flow, and input fixes. | `0400Index.md` |
| `05PropSystem` | Props/items, unlock rules, rollback props, error-removal props, and prop popups. | `0500Index.md` |
| `06Review` | Feature review, checklists, acceptance notes, risks, and implementation audits. | `0600Index.md` |
| `07ADMD` | Advertising, analytics, event tracking, ad SDK integration, and data reporting. | `0700Index.md` |

## Naming Rules

Use two-level numeric naming:

```text
<module-number><document-number><DocumentTopic>.md
```

Rules:

- The module number is the first two digits of the folder name.
- `00` is reserved for the module index.
- New documents start at `xx01` and increment by one.
- Keep the title readable for developers. Chinese, English, and digits are allowed.
- Examples: `0200Index.md`, `0201EditorTool01.md`, `0302LevelPreviewLoading.md`.

## Load Marker

A project is considered initialized when these exist:

```text
.ACSDM/
  0000ACSDMRootIndex.md
  00Rule/0000Index.md
  01ProjectOverview/0100Index.md
  02LevelEditor/0200Index.md
  03LevelLoading/0300Index.md
  04PlayerInput/0400Index.md
  05PropSystem/0500Index.md
  06Review/0600Index.md
  07ADMD/0700Index.md
```

No `acsdm-state.json` is required.

## Root Index

Root index name:

```text
0000ACSDMRootIndex.md
```

Required sections:

```markdown
# 0000 ACSDM Root Index

## 命名规范

## 检索方法

## 模块总览

| 模块 | 用途 | 索引文件 | 关键词 | 文档数量 | 更新时间 |
|---|---|---|---|---:|---|

## 模块映射兼容表

## 最近更新
```

`模块映射兼容表` is where project-specific aliases belong if a legacy folder is intentionally kept.

## Module Index

Each module index must include this scanning table:

| Field | Meaning |
|---|---|
| `md 文件名` | Markdown file name. |
| `加入时间` | First time the document was added to the index. |
| `最新修改时间` | Latest file or index update time. |
| `用途` | What the document is for. |
| `涉及脚本名称` | Related C#, Lua, config, or editor script paths/names. |
| `脚本简要功能说明` | Short responsibility summary for each related script. |
| `涉及方法名称` | Related classes, methods, functions, or entry points. |
| `涉及行数` | Related line numbers or ranges. |
| `检索关键词` | Words a user may use to find this document. |
| `记录类型` | Rule, plan, implementation log, review, index, or legacy reference. |

Index files should start with:

```markdown
## 命名规范

本目录使用 `<模块编号><文档编号><文档主题>.md` 命名。
`xx00Index.md` 为本目录索引，新增文档从 `xx01` 递增。
检索时先读根索引，再读本模块索引，最后只读取与任务直接相关的 md 文档。

## 检索方法

1. 先通过关键词定位模块。
2. 读取本索引的用途、脚本、方法、行号字段。
3. 只打开与当前需求直接相关的 md 文档。
4. 不进行全目录正文读取。
```
