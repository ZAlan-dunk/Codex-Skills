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

- Final plan generation requires `planning_confirmation_status=confirmed`.
- In PCTR-B, non-missing planner confirmation also requires a current A-01 local path, attachment token/block identity, and containing development-document revision. A separate planner-confirmation Docx/Wiki URL is invalid.
- In PCTR-B, final plan generation instead requires `sdd_confirmation_status=confirmed`, one current local SDD Markdown path, a matching attachment reference inside the feature section, the containing development-document revision, and no blocking SDD decision.
- Plan approval requires the explicit command `批准 <FEATURE-ID> 技术方案` after a route-appropriate plan is generated and validated.
- Implementation requires `technical_plan_status=approved` plus an explicit implementation command.
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
