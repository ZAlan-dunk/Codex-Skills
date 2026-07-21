# ACSDM Retrieval Policy

## Strict External Read Interface

The exact standalone command `调用ACSDM的接口，阅读相关文档` opens a one-response read-only retrieval exception even when full ACSDM is disabled. Follow `orange-read-interface.md`. Do not apply Planning and Authorization, PCTR lifecycle, Recording, initialization, repair, or script workflows in this mode.

## Core Retrieval Rule

Always retrieve in this order:

1. Project-local catalog root: `<project root>/.ACSDM`.
2. Root index: `.ACSDM/0000ACSDMRootIndex.md`.
3. Matching module index: `.ACSDM/<module>/xx00Index.md`.
4. Only directly relevant Markdown documents.
5. Project scripts and line ranges referenced by those documents.

Never read every Markdown document in the catalog unless the user explicitly asks for a full audit and accepts the context cost.

External document folders are reference or migration sources only. Do not treat them as the live catalog root.

## Explicit Document Triggers

Read relevant docs when the user says any of these:

```text
查阅相关文档、阅读相关文档、检索相关文档、查文档、看文档、根据文档、参考文档、按文档、项目文档、知识库
```

## Rule-First Triggers

Read `00Rule` before implementation when the request includes any of these:

```text
规范、规则、项目规则、框架、自研框架、通用规则、按规范、按照规范、参照规则、参照项目框架规则、Lua、lua、C#、csharp、交互、导表、Excel、UI框架、弹窗、道具弹窗、架构、项目架构
```

If the matched feature also belongs to another module, read `00Rule` first, then the feature module index.

## Module Keywords

| Module | Keywords |
|---|---|
| `00Rule` | 规则、规范、框架、Lua、C#、导表、Excel、UI框架、弹窗、道具弹窗、架构 |
| `01ProjectOverview` | 项目总览、玩法、游戏规则、主干脚本、快速了解、功能列表、项目概览 |
| `02LevelEditor` | 关卡编辑器、编辑器工具、像素图、难度、数独算法、Editor |
| `03LevelLoading` | 关卡加载、地图加载、颜色方块、预览图、加载链路、加载优化 |
| `04PlayerInput` | 输入、拖拽、DragFill、交互、填充、手势、点击 |
| `05PropSystem` | 道具、回退、消除错误、道具解锁、道具弹窗、Prop |
| `06Review` | 审查、review、检查清单、风险、验收、复查 |
| `07ADMD` | 广告、埋点、AD、打点、Analytics、统计、数据上报 |

## Folder Alias Fallback

Prefer the standard folders under `.ACSDM`. If a legacy project already has aliases inside `.ACSDM`, scan folder names before asking the user. Prefer obvious aliases, then ask only when multiple candidates are plausible.

| Standard module | Common aliases or patterns |
|---|---|
| `00Rule` | `00ProjectRule`, folders containing `Rule`, `规则`, or `规范` |
| `01ProjectOverview` | folders containing `Overview`, `Project`, `总览`, or `概览` |
| `02LevelEditor` | folders containing `LevelEditor`, `Editor`, or `编辑器` |
| `03LevelLoading` | folders containing `LevelLoading`, `LevelLoad`, `加载` |
| `04PlayerInput` | folders containing `PlayerInput`, `Input`, `DragFill`, `输入`, `拖拽` |
| `05PropSystem` | folders containing `Prop`, `道具` |
| `06Review` | folders containing `Review`, `审查`, `检查` |
| `07ADMD` | folders containing `AD`, `ADMD`, `Analytics`, `广告`, `埋点` |

When an alias is used, mention it briefly in the working notes and prefer updating the root index compatibility table if the user authorizes catalog edits.

## Context Reuse

If the same conversation already loaded a relevant module index or document and the user continues the same task, reuse that context. If the user changes module, asks a new feature, or the remembered context is stale or uncertain, read the index again.

## Automatic Retrieval vs Asking

Automatically retrieve ACSDM indexes when:

- the user explicitly requests project documentation;
- a rule-first trigger appears;
- a module keyword confidently matches a broad feature or review;
- a PCTR lifecycle command requires project evidence.

Ask before reading when no module matches, multiple modules are plausible, the only likely source is an external folder, access requires new approval, or the user explicitly asks not to inspect docs. For tiny, explicit tasks, proceed without ACSDM retrieval when no project-specific rule or history is relevant.

## Planning and Authorization

Before editing project files or catalog documents, classify the request:

- Direct task: small, explicit, low risk. Execute normally.
- Broad task: new feature, cross-file change, unclear module, unclear rule, or long request with multiple requirements. Present A/B/C sections and wait for authorization.

Authorization phrases include:

```text
开始实施、允许、可以执行、开始吧、按方案做、确认执行、开始实施并记录
```

Read-only retrieval and repair proposals may happen before authorization. Creating or repairing catalog files is an edit.

`开始实施` authorizes the approved project implementation but does not request ACSDM recording by itself.

`开始实施并记录` means update the most relevant existing record, or create a new numbered Markdown document when none exists, then update indexes.
## PCTR Feature-ID and Lifecycle Triggers

Recognize stable IDs such as `GUIDE-REMINDER-001` and these explicit commands:

```text
开始 FEATURE-ID 功能开发
开始实施 FEATURE-ID
开始实施并记录 FEATURE-ID
提交 FEATURE-ID 策划验收
FEATURE-ID 验收失败存在Bug
开始修复 FEATURE-ID BUG-ID
FEATURE-ID 重新提交策划验收
FEATURE-ID 策划已验收（任务完毕）
FEATURE-ID 策划已验收（任务完毕）并记录
同步PCTR-B SDD FEATURE-ID
FEATURE-ID SDD已确认
FEATURE-ID SDD存在歧义需要修改
```

Before PCTR retrieval, read `.codex/skill-gates.json` and branch on `pctr_mode`. Do not apply PCTR-A paired-document assumptions to a PCTR-B feature.

### Retrieval for Start Development

1. Read the matching PCTR requirement feature section.
2. PCTR-A: verify planning confirmation is `confirmed` and read the synchronized planner summary/revision.
3. PCTR-B: verify SDD confirmation is `confirmed`; read the local/Feishu SDD, current revision, sidecar, and implementation-plan target path.
4. Retrieve root index, `00Rule` where applicable, matching module indexes, related documents, and code locations.
5. Produce default ABC, enhanced ABC, or SDD evidence according to the PCTR route. For PCTR-B, the confirmed role-based SDD already owns design; generate implementation planning evidence instead of a duplicate SDD.
6. Do not edit code for `开始功能开发`.

### Retrieval for Acceptance Failure

1. Read failed planning acceptance point IDs and planner bug description.
2. Read the confirmed requirement and approved plan.
3. Read the relevant implementation record and prior bug/acceptance rounds.
4. Retrieve project rules and code evidence.
5. Produce expected-vs-actual, reproduction, evidence, hypotheses, likely code locations, fix plan, risks, and regression tests.
6. Wait for explicit bug-fix implementation authorization.

### Recording

- `策划已验收（任务完毕）` does not automatically create an ACSDM document.
- `策划已验收（任务完毕）并记录` updates the most relevant record or creates one only under the existing recording rules.
- Preserve feature IDs, bug IDs, acceptance rounds, confirmation revisions, and completion evidence.
