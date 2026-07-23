# Command Contract

State-changing actions require explicit commands. Do not infer them from discussion or document edits.

| Command | Effect | Code changes? |
|---|---|---:|
| `生成策划确认文档` | Create paired planner document | No |
| `生成 PCTR-B 功能需求开发文档` | Create `.PCTR/<planning-version>/`, every ordered `<FEATURE-ID>/` folder, the local Mode-B development document and sidecar with planning-sequence IDs and requirement descriptions, import/create the one Feishu development document, and register its URL/revision | Feishu document only |
| `阅读这个功能生成策划确认文档` | For one PCTR-B feature, collect ACSDM rule/history indexes, write/update `A-02-feature-decomposition.md`, render `A-01-planner-confirmation-snapshot.md` with concrete lettered preselection options, separate recommended choice/reason, and per-item reply blocks, then attach the native A-01 Markdown file immediately below the matching `2. SDD确认文档` heading in the one registered Feishu development document | Single development-document attachment only; never a new Docx/Wiki |
| `策划已确认` | Parse every per-item reply code block from the current PCTR-B planner confirmation document; accept a listed code or an empty selection plus non-empty custom supplement, reject invalid codes/unresolved must-answer items, update decomposition/sidecar, and unlock detailed SDD generation only if all must-answer ambiguities are resolved | No |
| `生成详细 SDD 工件` | After PCTR-B planner confirmation, hand the confirmed `A-02-feature-decomposition.md` to OUF and generate one role-based local `B-01-runtime-sdd.md` | No |
| `<FEATURE-ID> 程序已确认` | Confirm programmer review of the current detailed SDD and unlock implementation according to risk | No |
| `程序已确认，开始实施` | Confirm programmer review and, when explicitly authorized, proceed to implementation; high-risk or cross-module work still needs a local plan/checklist gate | Yes only after risk gate |
| `同步PCTR-B SDD <FEATURE-ID>` | Validate the matched local Markdown and attach it inside the matching feature section only when exact-position insertion is reliable; otherwise prepare manual upload | Feishu document only when automatic attachment is safe |
| `登记PCTR-B Markdown附件 <FEATURE-ID>` | Register an automatically or manually inserted Markdown attachment and containing document revision | No new document |
| `<FEATURE-ID> SDD已确认` | Confirm the attached local SDD snapshot and unlock plan generation | No |
| `<FEATURE-ID> SDD存在歧义需要修改` | Return the SDD for revision and keep planning locked | No |
| `同步策划确认 <FEATURE-ID>` | Validate and synchronize planner decisions | No |
| `<FEATURE-ID> 策划已确认` | Same as synchronization after validation | No |
| `开始 <FEATURE-ID> 功能开发` | If planner confirmation is missing/pending, generate/update A-01 and A-02, attach A-01 in the matching feature section, and remain locked. After planner and SDD/program confirmation pass, generate the detailed route-specific plan | Feishu attachment only while gated; otherwise no |
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
- formal plan or implementation is requested before required SDD/program confirmation;
- a planner confirmation document has a document-level reply section instead of per-item reply code blocks;
- any reply-bearing planner confirmation item lacks meaningful lettered options, a recommended option code, or a separate recommendation reason;
- a must-answer reply has both fields empty, an unknown option code, or multiple codes for an item that is not explicitly multi-select;
- a PCTR-B planner confirmation is represented by a separate Feishu Docx/Wiki, or A-01 is not attached at the exact matching `2. SDD确认文档` position;
- PCTR-B SDD synchronization has zero or multiple matching local artifacts, or the SDD is not the feature-local `B-01-runtime-sdd.md`;
- PCTR-B confirmation is requested without a current local Markdown identity, attachment reference, or containing development-document revision;
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
- PCTR-B: the confirmed planner-confirmation document is the product-rule gate; the confirmed role-based local Markdown SDD is the technical design artifact. `开始功能开发` normally generates a separate implementation plan and records only its local path; small low-risk work may use a short local checklist when the user explicitly asks to proceed after programmer confirmation.
