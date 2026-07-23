# Feature Lifecycle

## State Fields

PCTR-A stores these fields in the paired human documents. PCTR-B stores equivalent machine state in the sidecar and exposes only SDD confirmation checkboxes plus artifact paths in the human document.

Keep these states separate:

| Field | Values |
|---|---|
| `planning_confirmation_status` | `pending`, `partial`, `confirmed`, `rejected` |
| `technical_plan_status` | `not-created`, `creating`, `pending-approval`, `approved` |
| `development_status` | `not-started`, `implementing`, `integrating`, `submitted-for-planning-acceptance`, `bug-fixing`, `completed` |
| `planning_acceptance_status` | `not-entered`, `pending`, `in-review`, `partial`, `failed`, `accepted` |
| `final_feature_status` | `not-started`, `in-progress`, `blocked`, `completed`, `out-of-scope`, `superseded` |

PCTR-B additionally stores:

| Field | Values |
|---|---|
| `sdd_status` | `Draft`, `In Review`, `Approved` |
| `sdd_confirmation_status` | `pending`, `confirmed`, `ambiguous` |

## Legal Transitions

```text
planning_confirmation_status: pending -> partial -> confirmed
planning_confirmation_status: pending -> confirmed
planning_confirmation_status: pending/partial -> rejected
technical_plan_status: not-created -> creating -> pending-approval -> approved
development_status: not-started -> implementing -> integrating -> submitted-for-planning-acceptance
development_status: submitted-for-planning-acceptance -> bug-fixing -> submitted-for-planning-acceptance
planning_acceptance_status: pending/in-review -> partial/failed/accepted
accepted + explicit completion command -> development_status=completed and final_feature_status=completed
```

## Gates

- PCTR-A final plan generation requires `planning_confirmation_status=confirmed` and its existing confirmation gate.
- In PCTR-B, non-missing planner confirmation also requires a current A-01 local path, attachment token/block identity, and containing development-document revision. A separate planner-confirmation Docx/Wiki URL is invalid.
- In PCTR-B, joint-review plan generation requires `planner_confirmation.status=confirmed`, one current local Draft SDD Markdown path, matching source/decomposition identity, and no unresolved must-answer planner decision. It does not require SDD approval or Feishu attachment registration; the plan remains `pending-approval`.
- Plan approval requires the explicit command `批准 <FEATURE-ID> 技术方案` after a route-appropriate plan is generated and validated.
- Implementation requires the current SDD and plan identities, `sdd_status=Approved`, `sdd_confirmation_status=confirmed`, `technical_plan_status=approved`, no blocking review decision, and an explicit implementation command. `<FEATURE-ID> 程序已确认，开始实施` may validate and set these approval states atomically before execution.
- Planning acceptance submission requires implementation and technical verification evidence.
- Completion requires `planning_acceptance_status=accepted`, no open blocking bugs, and the explicit completion command.

## Illegal Examples

```text
pending confirmation -> approved plan
pending confirmation -> implementation
failed acceptance -> completed
partial acceptance -> completed
code completed -> planning accepted
```

## Scope Changes

Do not change a stable feature ID's meaning. If confirmation requires splitting, set the parent to `superseded` and create child IDs. If requirements are merged, preserve source IDs and point them to a new aggregate ID.

## Acceptance Rounds

Each round contains:

- round number;
- submission version/build/commit;
- submitted time;
- checklist results;
- planner notes;
- failed point IDs;
- bug IDs;
- result;
- re-submission link.

Never overwrite prior rounds.
