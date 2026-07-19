# {{document_title}}

## 文档状态

| 字段 | 内容 |
|---|---|
| 来源策划案 | {{source_url}} |
| 来源 Revision | {{revision}} |
| 策划确认与验收文档 | {{confirmation_url}} |
| 策划确认文档 Revision | {{confirmation_revision}} |
| 最后同步时间 | {{last_sync_at}} |
| ACSDM 状态 | {{acsdm_status}} |
| 输出风格 | {{style_profile}} |

## 全局约束

{{global_constraints}}

## 功能总表

| ID | 一级功能 | 原子功能 | 策划确认 | 路由 | 方案 | 开发 | 策划验收 | 最终状态 |
|---|---|---|---|---|---|---|---|---|
| {{feature_id}} | {{parent}} | {{title}} | 待确认 | {{route}} | 未生成 | 未开始 | 未进入 | 未开始 |

---

## {{feature_id}} {{feature_title}}

### 1. 功能定位与状态

```yaml
feature_id: {{feature_id}}
planning_confirmation_status: pending
technical_plan_status: not-created
development_status: not-started
planning_acceptance_status: not-entered
final_feature_status: not-started
confirmation_document_id: ""
confirmation_revision: -1
last_sync_at: ""
```

- 父功能：{{parent_feature}}
- 功能类型：{{discipline}}
- 预路由：{{route}}
- 复杂度：{{score}}/14
- 路由原因：{{route_reason}}

### 2. 来源追溯

{{source_trace}}

### 3. 需求目标

{{goal}}

### 4. 功能范围

{{scope}}

### 5. 非功能范围

{{non_scope}}

### 6. 前置条件、主流程与分支

{{flow}}

### 7. 状态、生命周期、数据与兼容

{{state_data_compatibility}}

### 8. UI、交互、表现、依赖与冲突

{{presentation_dependencies}}

### 9. 异常与边界

{{edge_cases}}

### 10. ACSDM 检索结果

{{acsdm_evidence}}

### 11. 待确认项

| 确认 ID | 问题 | 阻塞 | 状态 |
|---|---|---:|---|
| {{confirmation_id}} | {{question}} | 是 | 待确认 |

### 12. 策划确认同步

- 策划确认状态：待确认
- 最终确认摘要：
- 确认人：
- 确认时间：
- 策划确认文档：{{confirmation_url}}
- 确认 Revision：

### 13. 技术验收标准与测试矩阵

{{acceptance_and_tests}}

### 14. 技术方案与开发状态

- 技术方案状态：未生成
- 开发状态：未开始
- 实现版本/Commit：
- ACSDM 实现记录：

### 15. 策划验收状态

- 策划验收状态：未进入
- 当前验收轮次：0
- 失败验收点：
- 开放 Bug：
- 最终验收时间：

### 16. 可复制 Agent 任务

{{agent_task_block}}
