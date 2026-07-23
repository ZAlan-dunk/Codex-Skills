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
- OUF 可以保留自己的 Context Brief / SDD / Plan / Report / Evidence 产物；如当前 PCTR 流程需要，再额外导出一份 PCTR-bound Draft SDD Markdown；不实施代码；
- PCTR-bound SDD 如生成，必须保存为 `{{sdd_output_path}}`，也就是功能目录下的 `B-01-runtime-sdd.md`；OUF 自有产物仍保存到 OUF 默认目录；
- OUF 自有 Context Brief / SDD / Plan / Report / Evidence 不写入 PCTR 功能目录，只在完成后把路径交给 PCTR 登记；
- SDD 静态验证通过后，返回 `B-01-runtime-sdd.md` 路径和上述飞书开发文档的对应功能章节，用户/程序手动上传；随后 PCTR 登记附件与 OUF 产物路径；不得新建独立飞书 SDD 文档；确认状态保持 pending。

功能需求说明：
{{requirement_description}}

确认后的功能拆解文件内容由 OUF 读取：
{{decomposition_path}}

ACSDM / 代码证据摘要：
{{evidence_summary}}
```
