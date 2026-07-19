# Complexity Routing

## Hard SDD Triggers

Route to SDD when any applies:

- persistence schema change, migration, or old-data repair;
- public/shared framework or foundational service change;
- three or more project modules;
- complex state machine or multiple asynchronous sequences;
- advertising, payment, account, privacy, network protocol, or external platform SDK behavior;
- global operation lock, popup queue, or animation concurrency with broad impact;
- high-cost ambiguity in core behavior;
- five or more core script changes are likely;
- rollback, rollout, or compatibility design is required.

## Score Dimensions

Score each from 0 to 2:

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| module span | one | two | three or more |
| data impact | none | config field | persistence/migration |
| state complexity | direct | several states | state machine/async sequence |
| shared impact | local | reusable component | public framework |
| external dependency | none | asset/config | SDK/platform/service |
| ambiguity | clear | minor | core ambiguity |
| regression scope | one view | one flow | multi-flow/global |

## Route

- `0-3`: standard ACSDM A/B/C.
- `4-6`: enhanced A/B/C.
- `7-14`: SDD.
- Any hard trigger: SDD regardless of score.

## Standard A/B/C Output

- A: recommended implementation path and reused project mechanism.
- B: files, methods, configuration, assets, and tests to change.
- C: ambiguity, risk, regression, and confirmation points.
- Wait for explicit authorization before edits.

## Enhanced A/B/C Output

Add:

- sequence/state description;
- exact integration points;
- test matrix;
- compatibility and rollback notes;
- staged implementation order.

Use this when architecture already exists and no SDD hard trigger applies.

## SDD Output

Require ACSDM retrieval first, then create or update:

- requirements artifact;
- design artifact;
- implementation tasks;
- test plan;
- evidence/source mapping;
- unresolved decisions.

Do not implement until the SDD review gate passes.

## Guardrails

Detail level does not equal complexity. A long but local UI requirement may remain A/B/C. A short request such as “change save format” may require SDD because of migration risk.

## Planning Confirmation Precondition

Complexity scoring before planning confirmation is provisional. Do not create a final ABC/SDD plan until all blocking planning items are confirmed and synchronized. Recalculate score and hard triggers after confirmation changes scope, persistence, module span, SDK use, locking, compatibility, or ambiguity.
