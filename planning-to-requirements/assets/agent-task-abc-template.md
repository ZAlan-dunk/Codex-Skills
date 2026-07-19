# Standard A/B/C Agent Task Template

```text
你现在需要处理功能 {{feature_id}}「{{feature_title}}」。

【策划确认门禁】
当前状态：{{planning_confirmation_status}}
如果不是 confirmed，立即停止；只允许补充检索和待确认问题，不生成正式方案，不修改代码。

【策划最终确认】
确认文档：{{confirmation_document}}
确认 Revision：{{confirmation_revision}}
确认摘要：{{confirmed_planning_summary}}

【实施模式】
使用标准 ACSDM A/B/C，不创建 SDD。“开始功能开发”只生成方案；等待“开始实施 {{feature_id}}”后才改代码。

【必须先执行的 ACSDM 检索】
1. 读取项目 .ACSDM 根索引。
2. 按关键词 {{keywords}} 匹配模块。
3. 涉及规则/框架时先读 00Rule。
4. 读取直接相关文档和代码位置。
5. 未找到的内容标记为未找到。

【已确认需求】
{{planning_facts}}

【范围】
{{scope}}

【非范围与禁止假设】
{{non_scope_and_prohibitions}}

【需要输出】
A. 推荐实现方案与调用链。
B. 文件、方法、配置、资源和测试。
C. 风险、边界、回归和剩余待确认项。

【验收标准】
{{acceptance}}
```
