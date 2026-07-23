# {{feature_title}} 策划确认文档

> 功能编码：`{{feature_id}}`
>
> 策案标题路径：{{source_heading_path}}
>
> 来源策案：{{source_url}}，Revision `{{source_revision}}`
>
> 策划确认快照：`{{planner_confirmation_snapshot_path}}`
>
> 功能拆解文件：`{{decomposition_path}}`（唯一 A-02 文件，包含来源快照和拆解内容）
>
> 文档用途：只确认策划规则、真实歧义和需要补充的内容。完整功能理解与功能拆解保存在本地功能拆解文件，不放在本文档中。

## 0. 本次需要策划关注的内容

> 填写方式：请在每条歧义点 / 待确认点下方自己的代码框里填写。代码框内只保留两行：`选择：` 和 `补充：`，不要重复填写条目编号。

### 0.1 歧义点清单

> 只列真实歧义。策案已经写清楚、不会影响两种不同实现的内容，不要为了形式写成歧义。

| 编号 | 需要确认的问题 | 推荐选项 |
|---|---|---|
{{ambiguity_rows}}

### 0.2 待确认点 / 完善建议清单

> 只列确实会影响体验、资源、协作或后续实现的信息。

| 编号 | 建议确认或补充的内容 | 推荐处理 |
|---|---|---|
{{confirmation_rows}}

## 1. 功能需求简单描述

{{feature_brief}}

## 2. 歧义点详情

{{ambiguity_details}}

## 3. 待确认点 / 完善建议详情

{{confirmation_details}}

## 4. 证据来源（策划无须关注）

> 这一节只给 PCTR-B / OUF / 程序追溯来源使用，策划确认时可以不看。

- 来源策案：{{source_url}}，Revision `{{source_revision}}`
- 来源快照：已写入功能拆解文件 `{{decomposition_path}}`
- 功能拆解文件：`{{decomposition_path}}`
- ACSDM / 历史开发文档索引：
{{evidence_index}}

## 5. 确认后的处理方式

策划确认后：

1. PCTR-B 按条目标题编号定位，读取每条歧义点 / 待确认点下方的回复代码框。
2. PCTR-B 更新本地功能拆解文件，并记录已选选项、补充说明和仍未回答的内容。
3. 若需要回答的内容仍为空，PCTR-B 会列出未填写项并等待补充。
4. 若需要回答的内容均已填写，PCTR-B 将已确认的功能拆解交给 OUF 生成详细 SDD。
5. OUF 生成的 SDD 面向程序、QA、Tech Lead；不再重新制造策划歧义。
