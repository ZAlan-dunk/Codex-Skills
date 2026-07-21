# PCTR-B → Orange SDD Handoff Request

```text
PCTR Feature ID: {{feature_id}}
功能标题：{{feature_title}}
策案标题路径：{{source_heading_path}}
来源策案：{{source_url}}
来源 Revision：{{source_revision}}
PCTR-B 飞书开发文档：{{development_document_url}}
飞书 SDD 目标：{{feishu_parent_url}}

请先按项目门禁发送独立命令 `启用OUF`，再使用 brainstorming-unity 为该功能生成一份角色分区 Draft SDD。

要求：
- 先通过 PCTR-B 功能编码查询接口核对以上身份；不得按标题猜测编码；
- SDD 元数据必须写入 PCTR Feature ID、策案标题路径、来源 Revision 和 PCTR-B 飞书开发文档；
- 严格使用来源标题和已整理的功能需求说明；
- 包含策划规则、程序设计、QA 验收、风险、回滚和待确认项；
- 同步生成 Context Brief 与 Draft SDD，不生成实施计划、不实施代码；
- 工件分别保存到 CodexTemp/OrangeUnityForge/briefs/ 与 CodexTemp/OrangeUnityForge/specs/；
- SDD 静态验证通过后自动调用 PCTR-B 上传接口，并回填上述飞书开发文档的对应功能；确认状态保持 pending；
- 文件名优先使用 YYYY-MM-DD-{{feature_id_lower}}-<slug>-sdd.md。

功能需求说明：
{{requirement_description}}

ACSDM / 代码证据摘要：
{{evidence_summary}}
```
