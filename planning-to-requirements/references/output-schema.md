# Output Schema

## Paired Document Metadata

Both documents must record:

- source planning document ID/link/revision;
- requirement document ID/link/revision;
- planning confirmation document ID/link/revision;
- generation mode and style profile;
- last synchronization time;
- stable feature count and out-of-scope count.

## Requirement Development Document

### Summary Table

Required columns:

| ID | Parent | Atomic function | Confirmation | Route | Plan | Development | Planning acceptance | Final status |

### Atomic Feature Section

Every active feature contains:

1. identity, source trace, goal, scope, and non-scope;
2. preconditions, main/branch flow, state/lifecycle, data/config/compatibility;
3. UI/presentation, dependencies, conflicts, errors, ACSDM evidence;
4. technical acceptance criteria and test matrix;
5. unresolved questions with owner and blocking status;
6. planning confirmation state and synchronized decision;
7. route and technical plan state;
8. development and implementation-submission state;
9. planning acceptance state, round, and bug state;
10. final feature state;
11. route-specific Agent task capsule with confirmation lock.

Use this state block:

```yaml
feature_id: FEATURE-ID
planning_confirmation_status: pending
technical_plan_status: not-created
development_status: not-started
planning_acceptance_status: not-entered
final_feature_status: not-started
confirmation_document_id: ""
confirmation_revision: -1
last_sync_at: ""
```

### Confirmation Synchronization Section

Include:

- original planning text/conflict;
- confirmation item IDs and resolved values;
- final planner summary;
- confirmer/time;
- confirmation document link/revision;
- synchronized requirement revision;
- route recalculation result.

## Planning Confirmation and Acceptance Document

### Summary Table

| Feature ID | Feature | Short implementation description | Blocking items | Confirmation | Development | Acceptance |

### Feature Section

1. short implementation description;
2. current visible scope;
3. confirmation item table;
4. final planner summary and metadata;
5. planner-readable acceptance checklist;
6. acceptance status and rounds;
7. failed bugs and re-submission history.

### Confirmation Item

```yaml
confirmation_id: PC-FEATURE-ID-01
blocking: true
status: pending
planner_response: ""
confirmed_by: ""
confirmed_at: ""
```

### Acceptance Item

```yaml
acceptance_id: PA-FEATURE-ID-01
mandatory: true
result: 未验收
planner_note: ""
```

## Evidence Labels

Use exact labels:

- `策划明确要求`
- `策划最终确认`
- `ACSDM 项目规则`
- `代码现状`
- `建议方案`
- `待确认`

## Task Capsule Gate

Every task capsule begins with:

```text
【策划确认门禁】
当前状态：{{planning_confirmation_status}}
未达到 confirmed 时停止，不生成正式方案或修改代码。
```

After confirmation, include the final planner summary, confirmation revision, route, and applicable authorization command.

## Display and State Mapping

- A generated but unapproved plan displays as `方案待批准` and stores `technical_plan_status: pending-approval`.
- An explicitly approved plan displays as `方案已批准` and stores `technical_plan_status: approved`.
- `功能已完成` is only a display label for the combined state `development_status: completed`, `planning_acceptance_status: accepted`, and `final_feature_status: completed`.
