# ACSDM Document Template

Use this template for new ACSDM Markdown documents. The YAML block supports scriptable retrieval; the Markdown body must remain readable for developers.

```markdown
---
acsdm_id: "0201"
title: "EditorTool01"
module: "02LevelEditor"
type: "方案 | 规则 | 实现记录 | 审查 | 日志 | 索引 | 旧版参考"
created_at: "2026-07-05T00:00:00+08:00"
updated_at: "2026-07-05T00:00:00+08:00"
keywords:
  - "关卡编辑器"
pctr_feature_id: "GUIDE-REMINDER-001"
confirmed_requirement_revision: ""
planning_confirmation_source: ""
planning_acceptance_status: "not-entered"
related_bug_ids: []
related_scripts:
  - path: "Assets/.../Example.cs"
    purpose: "脚本职责说明"
    methods:
      - name: "MethodName"
        lines: "120-160"
---

# 0201 EditorTool01

## 1. 用途

说明本文档解决什么问题，什么时候应该读它。

## 2. 背景与约束

记录项目规则、设计前提、历史原因、兼容要求。

## 3. 相关脚本索引

| 脚本 | 职责 | 方法/入口 | 行数 |
|---|---|---|---|
| `Assets/.../Example.cs` | ... | `MethodName` | `120-160` |

## 4. 方案或规则正文

写清楚规则、方案、流程或实现说明。优先使用短段落和表格，便于人读，也便于 Agent 检索。

## 5. 实现记录

### 2026-07-05 HH:mm

- 需求摘要：...
- 方案编号：A1/B1/C1...
- 实际改动：...
- 验证结果：...

## 6. 审查点

- 是否符合 `00Rule`：...
- 是否存在兼容风险：...
- 是否需要补充测试或回滚说明：...

## 7. 变更日志

| 时间 | 变更 | 作者/Agent | 验证 |
|---|---|---|---|
| 2026-07-05 HH:mm | ... | ... | ... |
```

## 8. PCTR 功能生命周期

- 功能 ID：...
- 策划确认状态：...
- 确认需求 Revision：...
- 策划确认来源：...
- 技术方案路由：标准 ABC / 增强 ABC / SDD
- 技术方案状态：...
- 开发状态：...
- 策划验收状态：...
- 验收轮次：...
- 关联 Bug：...
- 最终功能状态：...
## Developer Readability Rules

- Put the most useful summary in the first screen.
- Keep script paths and method names in tables.
- Use concrete line ranges when known.
- Avoid giant pasted code blocks unless the document is specifically a code reference.
- Keep historical notes, but mark old or superseded behavior clearly.
