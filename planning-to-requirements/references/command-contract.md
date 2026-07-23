# Command Contract

State-changing actions require explicit commands. Do not infer them from discussion or document edits.

| Command | Effect | Code changes? |
|---|---|---:|
| `生成策划确认文档` | Create paired planner document | No |
| `生成 PCTR-B 功能需求开发文档` | Create `.PCTR/<planning-version>/`, every ordered `<FEATURE-ID>/` folder, the local Mode-B development document and sidecar with planning-sequence IDs and requirement descriptions; Feishu creation/upload is manual, then register its URL/revision | Feishu document only |
| `阅读这个功能生成策划确认文档` | For one PCTR-B feature, collect ACSDM rule/history indexes, write/update `A-02-feature-decomposition.md`, render `A-01-planner-confirmation-snapshot.md` with concrete lettered preselection options, separate recommended choice/reason, and per-item reply blocks, then return the native A-01 Markdown path and exact `2. SDD确认文档` target for manual upload/registration | Local files only; never a new Docx/Wiki |
| `策划已确认` | Parse every per-item reply code block from the current PCTR-B planner confirmation document; accept a listed code or an empty selection plus non-empty custom supplement, reject invalid codes/unresolved must-answer items, update decomposition/sidecar, and unlock detailed SDD generation only if all must-answer ambiguities are resolved | No |
| `生成详细 SDD 工件` | After PCTR-B planner confirmation, hand the confirmed `A-02-feature-decomposition.md` to OUF, preserve OUF outputs under `docs/forge-artifacts/`, and register their paths/hashes; produce `B-01-runtime-sdd.md` when a PCTR-bound SDD snapshot is needed and optionally generate its linked `Draft / pending-approval` implementation plan for joint review | No |
| `<FEATURE-ID> 程序已确认` | Confirm programmer review of the current detailed SDD; a separately pending plan still requires approval | No |
| `<FEATURE-ID> 程序已确认，开始实施` | Validate current SDD/plan identities and blocking decisions, atomically approve both, and proceed to implementation under the approved plan | Yes, only after atomic validation |
| `同步PCTR-B SDD <FEATURE-ID>` | Validate the matched local Markdown and return exact target heading/local path for manual upload | No automatic Feishu upload by default |
| `登记PCTR-B Markdown附件 <FEATURE-ID>` | Register a manually inserted Markdown attachment and containing document revision | No new document |
| `登记PCTR-B OUF产物 <FEATURE-ID>` | Register OUF artifact paths, hashes, types, and statuses from `docs/forge-artifacts/` in the sidecar | No |
| `<FEATURE-ID> SDD已确认` | Confirm the current local SDD snapshot; a review plan may already exist but remains separately approval-gated | No |
| `<FEATURE-ID> SDD存在歧义需要修改` | Return the SDD for revision and keep plan approval/implementation locked; an existing review plan remains pending | No |
| `同步策划确认 <FEATURE-ID>` | Validate and synchronize planner decisions | No |
| `<FEATURE-ID> 策划已确认` | Same as synchronization after validation | No |
| `开始 <FEATURE-ID> 功能开发` | If planner confirmation is missing/pending, generate/update A-01 and A-02, output the manual upload target for A-01, and remain locked. After planner confirmation, generate/refresh the Draft SDD plus `Draft / pending-approval` route-specific plan as a joint review package | Feishu attachment only while planner-gated; otherwise no |
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
- PCTR-B development-document generation lacks an unambiguous Feishu development-document target;
- a selected feature lacks a planning sequence or planning-grounded requirement content when the source contains content;
- Orange feature lookup has zero/multiple feature matches or stale source identity;
- detailed SDD generation is requested before PCTR-B planner confirmation;
- a PCTR-B review plan is requested before planner confirmation, or an executable/approved plan is requested before required SDD/program confirmation;
- a planner confirmation document has a document-level reply section instead of per-item reply code blocks;
- any reply-bearing planner confirmation item lacks meaningful lettered options, a recommended option code, or a separate recommendation reason;
- a must-answer reply has both fields empty, an unknown option code, or multiple codes for an item that is not explicitly multi-select;
- a PCTR-B planner confirmation is represented by a separate Feishu Docx/Wiki, or the registered A-01 attachment is not at the exact matching `2. SDD确认文档` position;
- PCTR-B SDD synchronization has zero or multiple matching local artifacts when a PCTR-bound B-01 is required, or the SDD is not the feature-local `B-01-runtime-sdd.md`;
- PCTR-B confirmation is requested without a current local Markdown identity, or any registered SDD attachment metadata is partial/stale (attachment name differs from `B-01-runtime-sdd.md`, token/URL is missing, or containing development-document revision is invalid);
- both PCTR-B confirmation checkboxes are selected;
- plan approval is requested before a complete route-specific plan exists or when its confirmed requirement revision is stale;
- implementation is requested before current SDD and plan identities are validated and approved;
- completion is requested with failed/partial/missing acceptance items;
- a bug fix is requested without bug description or affected acceptance point;
- document revisions conflict.

## Output of Start Development

- Default ABC: A implementation path; B files/config/resources/tests; C risks/ambiguity/regression.
- Enhanced ABC: default output plus state/sequence, exact integration, staged implementation, compatibility, rollback, and test matrix.
- SDD route in PCTR-A: requirements, design, tasks, test-plan, evidence/source mapping, and unresolved decisions.
- PCTR-B: the confirmed planner-confirmation document is the product-rule gate. `开始功能开发` normally generates a Draft role-based local Markdown SDD plus a separate `Draft / pending-approval` implementation plan as one joint review package and records the plan's local path. Program/user confirmation approves the current identities before implementation; small low-risk work may use a short local checklist only when explicitly requested.
