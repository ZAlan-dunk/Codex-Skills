# Planning Acceptance Bug Analysis Template

## {{bug_id}} {{feature_id}} 策划验收失败首次分析

### 1. 策划验收失败描述

{{planner_bug_description}}

### 2. 对应验收点

{{failed_acceptance_ids}}

### 3. 已确认需求与预期行为

{{confirmed_expected_behavior}}

### 4. 实际行为与复现步骤

{{actual_behavior_and_reproduction}}

### 5. 证据

- 构建/Commit：{{build_or_commit}}
- 日志/截图/录屏引用：{{evidence}}
- ACSDM 规则：{{acsdm_evidence}}

### 6. 首次根因假设

{{root_cause_hypotheses}}

### 7. 需要检查的代码

| 文件 | 方法/入口 | 检查内容 |
|---|---|---|
| {{file}} | {{method}} | {{check}} |

### 8. 修复方案

{{fix_plan}}

### 9. 回归测试

{{regression_tests}}

### 10. 状态

- 策划验收状态：验收失败
- 开发状态：Bug修复中
- 最终功能状态：处理中
- 下一步授权：`开始修复 {{feature_id}} {{bug_id}}`
