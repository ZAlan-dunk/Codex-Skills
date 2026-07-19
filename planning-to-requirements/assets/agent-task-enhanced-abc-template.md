# Enhanced A/B/C Agent Task Template

```text
你现在需要处理功能 {{feature_id}}「{{feature_title}}」。

【策划确认门禁】
当前状态：{{planning_confirmation_status}}
如果不是 confirmed，立即停止，不生成正式增强型 A/B/C，不修改代码。

【策划最终确认】
确认文档：{{confirmation_document}}
确认 Revision：{{confirmation_revision}}
确认摘要：{{confirmed_planning_summary}}

【实施模式】
使用增强型 ACSDM A/B/C。“开始功能开发”只生成方案；等待“开始实施 {{feature_id}}”后才改代码。

【ACSDM 检索】
{{acsdm_steps}}

【已确认需求、范围和非范围】
{{confirmed_requirement}}

【流程、状态、数据、兼容与生命周期】
{{flow_state_data}}

【异常、冲突、回归与回滚】
{{edges_conflicts_regression}}

【需要输出】
A. 主实现方案、调用链、状态流和分阶段顺序。
B. 文件、方法、配置、资源、测试与验证命令。
C. 歧义、风险、兼容、回滚和待校准项。
并附相关脚本表、时序/状态说明、测试矩阵和回滚说明。

【验收标准】
{{acceptance}}
```
