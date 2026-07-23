# PCTR-B → Orange SDD Handoff Request

```text
PCTR Feature ID: {{feature_id}}
PCTR Base Feature ID: {{base_feature_id}}
策案序号：{{planning_sequence}}
功能标题：{{feature_title}}
策案标题路径：{{source_heading_path}}
来源策案：{{source_url}}
来源 Revision：{{source_revision}}
PCTR-B 飞书开发文档：{{development_document_url}}
PCTR 功能目录：{{feature_artifact_dir}}
确认后的功能拆解：{{decomposition_path}}
SDD 输出路径：{{sdd_output_path}}

请先按项目门禁发送独立命令 `启用OUF`，再使用 brainstorming-unity 为该功能生成一份角色分区 Draft SDD。

要求：
- 先通过 PCTR-B 功能编码查询接口核对以上身份；不得按标题猜测编码；
- SDD 元数据必须写入 PCTR Feature ID、策案标题路径、来源 Revision、PCTR-B 飞书开发文档、确认后的功能拆解路径和 SDD 输出路径；
- 严格读取 `{{decomposition_path}}`，使用其中已确认的策划结论、歧义处理和功能拆解；
- 包含策划规则、程序设计、QA 验收、风险、回滚和待确认项；
- 只生成一份 PCTR-owned Draft SDD Markdown，不生成实施计划、不实施代码；
- SDD 必须保存为 `{{sdd_output_path}}`，也就是功能目录下的 `B-01-runtime-sdd.md`；不得另存为日期前缀文件；
- 如果 OUF 需要内部 Context Brief，只能作为临时内部过程或 Orange-owned 缓存，不能在 PCTR 功能目录里新增文件；
- SDD 静态验证通过后调用 PCTR-B Markdown 附件接口，把 `B-01-runtime-sdd.md` 直接放到上述飞书开发文档的对应功能章节内；若 IDE/CLI 无法可靠定位并验证附件位置，则停止自动写入，由用户手动上传；不得新建独立飞书 SDD 文档；确认状态保持 pending。

功能需求说明：
{{requirement_description}}

确认后的功能拆解文件内容由 OUF 读取：
{{decomposition_path}}

ACSDM / 代码证据摘要：
{{evidence_summary}}
```
