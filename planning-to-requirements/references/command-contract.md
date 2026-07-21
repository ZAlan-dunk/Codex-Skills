# Command Contract

State-changing actions require explicit commands. Do not infer them from discussion or document edits.

| Command | Effect | Code changes? |
|---|---|---:|
| `生成策划确认文档` | Create paired planner document | No |
| `生成 PCTR-B 功能需求开发文档` | Create the local Mode-B development document and sidecar, import/create its Feishu document, and register URL/revision/SDD target | Feishu document only |
| `同步PCTR-B SDD <FEATURE-ID>` | Validate and upload the matched SDD, then synchronize its link | Feishu document only |
| `<FEATURE-ID> SDD已确认` | Confirm the uploaded SDD and unlock plan generation | No |
| `<FEATURE-ID> SDD存在歧义需要修改` | Return the SDD for revision and keep planning locked | No |
| `同步策划确认 <FEATURE-ID>` | Validate and synchronize planner decisions | No |
| `<FEATURE-ID> 策划已确认` | Same as synchronization after validation | No |
| `开始 <FEATURE-ID> 功能开发` | Generate detailed route-specific plan | No |
| `批准 <FEATURE-ID> 技术方案` | Validate and approve the generated plan | No |
| `开始实施 <FEATURE-ID>` | Implement an approved plan | Yes |
| `开始实施并记录 <FEATURE-ID>` | Implement and update/create ACSDM record | Yes |
| `提交 <FEATURE-ID> 策划验收` | Create next planning acceptance round | No |
| `<FEATURE-ID> 验收失败存在Bug：<描述>` | Record failure and produce first analysis | No |
| `开始修复 <FEATURE-ID> <BUG-ID>` | Implement an approved bug-fix plan | Yes |
| `<FEATURE-ID> 重新提交策划验收` | Append a new acceptance round | No |
| `<FEATURE-ID> 策划已验收（任务完毕）` | Validate and mark complete | No |
| `<FEATURE-ID> 策划已验收（任务完毕）并记录` | Mark complete and update ACSDM record | ACSDM only |

## Required Rejections

Reject or stop when:

- feature ID is missing or ambiguous;
- PCTR-B development-document generation lacks an unambiguous Feishu parent or SDD target;
- Orange feature lookup has zero/multiple feature matches or stale source identity;
- formal plan is requested before planner confirmation;
- PCTR-B SDD synchronization has zero or multiple matching local artifacts;
- PCTR-B confirmation is requested without a Feishu SDD URL/revision;
- both PCTR-B confirmation checkboxes are selected;
- plan approval is requested before a complete route-specific plan exists or when its confirmed requirement revision is stale;
- implementation is requested before plan approval;
- completion is requested with failed/partial/missing acceptance items;
- a bug fix is requested without bug description or affected acceptance point;
- document revisions conflict.

## Output of Start Development

- Default ABC: A implementation path; B files/config/resources/tests; C risks/ambiguity/regression.
- Enhanced ABC: default output plus state/sequence, exact integration, staged implementation, compatibility, rollback, and test matrix.
- SDD route in PCTR-A: requirements, design, tasks, test-plan, evidence/source mapping, and unresolved decisions.
- PCTR-B: the confirmed role-based SDD is the design/confirmation artifact; `开始功能开发` generates a separate implementation plan and records only its local path.
