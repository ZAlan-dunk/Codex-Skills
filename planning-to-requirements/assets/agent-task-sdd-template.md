# SDD Agent Task Template

```text
请为功能 {{feature_id}}「{{feature_title}}」创建 SDD 工件。

【策划确认门禁】
当前状态：{{planning_confirmation_status}}
如果不是 confirmed，立即停止，不创建正式 SDD，不修改代码。

【策划最终确认】
确认文档：{{confirmation_document}}
确认 Revision：{{confirmation_revision}}
确认摘要：{{confirmed_planning_summary}}

【SDD 路由原因】
{{sdd_reasons}}

【必须先读取 ACSDM】
{{acsdm_steps}}

【已确认需求、范围和非范围】
{{confirmed_requirement}}

【关键状态、数据、兼容、异常和回滚】
{{design_constraints}}

【SDD 必须定义】
- requirements：术语、需求、非范围、验收；
- design：状态机、时序、职责、接口、数据、生命周期、并发与锁；
- tasks：可验证的实施步骤；
- test-plan：单元、集成、边界、清理、回归和策划验收映射；
- evidence/source mapping：策划确认、ACSDM 和源码证据；
- unresolved decisions：剩余非阻塞决策。

当前只创建规格；在 SDD 审核通过且收到“开始实施 {{feature_id}}”之前不要修改代码。
```
