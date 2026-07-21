# ACSDM Read Interface Contract

## Trigger

Open this interface only for the exact standalone command:

```text
调用ACSDM的接口，阅读相关文档
```

Do not infer the command from mentions of ACSDM, documents, project history, rules, or another Skill's recommendation.

## Scope

This is a one-response read-only bridge for Orange Unity Forge or another active primary Skill. Full ACSDM may remain disabled. Do not change `.codex/skill-gates.json`.

Use the active task's feature, module, Bug, or review topic as the retrieval query. If no topic exists, ask only for the feature/topic and stop.

## Allowed Retrieval

1. Read `.ACSDM/0000ACSDMRootIndex.md`.
2. Match the active topic to one or more modules using `retrieval-policy.md`.
3. Read `00Rule/0000Index.md` first when the topic involves project rules, framework behavior, Lua/C#, UI, popups, Excel, architecture, testing, or verification.
4. Read only the matching module index files.
5. Read only directly relevant catalog documents selected from those indexes.
6. Inspect only source paths, methods, and line ranges explicitly referenced by the selected catalog documents when needed to explain the current implementation.
7. Reuse unchanged documents only within the same active task response; the interface closes when the response ends.

## Required Output

```markdown
## ACSDM 只读检索结果
- 当前主 Skill：
- 检索主题：
- 根索引：
- 规则索引：适用路径 / 不适用
- 模块索引：
- 相关文档：
- 相关脚本、方法与行号：
- 推荐阅读顺序：
- 当前项目理解：
- 缺失、过期或冲突证据：
- 接口状态：本次响应后关闭；完整 ACSDM 仍为启用/禁用
```

Keep the understanding concise and document-grounded. Clearly separate catalog facts from source-code observations.

## Forbidden Behavior

- Do not initialize, repair, migrate, regenerate, or validate ACSDM.
- Do not run `scripts/acsdm-*.ps1`.
- Do not create, edit, rename, move, or delete `.ACSDM` files or indexes.
- Do not create A/B/C plans, implementation plans, SDDs, approvals, or authorization gates.
- Do not modify project source, configuration, assets, tests, or documentation.
- Do not activate or operate PCTR lifecycle commands.
- Do not record implementation, Bug, acceptance, or completion state.
- Do not recursively read the full catalog or unrelated modules.
- Do not change any Skill enable/disable state.

If the requested action exceeds retrieval, stop at the paths and findings. State which full Skill would be needed and show its exact enable command; do not enable it automatically.
