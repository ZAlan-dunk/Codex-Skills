# Feature Lifecycle

## State Fields

Keep these states separate:

| Field | Values |
|---|---|
| `planning_confirmation_status` | `pending`, `partial`, `confirmed`, `rejected` |
| `technical_plan_status` | `not-created`, `creating`, `pending-approval`, `approved` |
| `development_status` | `not-started`, `implementing`, `integrating`, `submitted-for-planning-acceptance`, `bug-fixing`, `completed` |
| `planning_acceptance_status` | `not-entered`, `pending`, `in-review`, `partial`, `failed`, `accepted` |
| `final_feature_status` | `not-started`, `in-progress`, `blocked`, `completed`, `out-of-scope`, `superseded` |

## Legal Transitions

```text
pending -> partial -> confirmed
pending -> confirmed
pending/partial -> rejected
confirmed -> pending-plan
not-created -> creating -> pending-approval -> approved
not-started -> implementing -> integrating -> submitted-for-planning-acceptance
submitted-for-planning-acceptance -> bug-fixing -> submitted-for-planning-acceptance
pending/in-review -> partial/failed/accepted
accepted -> completed
```

## Gates

- Final plan generation requires `planning_confirmation_status=confirmed`.
- Implementation requires a route-appropriate approved plan.
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
