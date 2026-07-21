# PCTR-A Planning Acceptance Workflow

Use this human paired-document workflow only when `pctr_mode=A`. PCTR-B keeps detailed rounds in the sidecar and bug artifacts while the single development document lists artifact paths.

## Submission

`提交 <FEATURE-ID> 策划验收` creates the next acceptance round and records:

- implementation version, build, or commit;
- testing entry point and environment;
- implementation summary;
- known limitations;
- planner-readable acceptance checklist;
- submission time.

Set development status to `submitted-for-planning-acceptance` and acceptance status to `pending`.

## Acceptance Checklist

Convert technical acceptance criteria into planner-observable behavior. Give each item a stable ID:

```text
PA-<FEATURE-ID>-<NN>
```

Results: `未验收`, `通过`, `失败`, `不适用`. Mandatory items cannot be `不适用` without an explicit planner decision.

## Failure

On `<FEATURE-ID> 验收失败存在Bug：...`:

- preserve the round as failed;
- record failed acceptance IDs and planner description verbatim;
- create a bug ID such as `BUG-<FEATURE-ID>-<NN>`;
- update states to failed/bug-fixing/in-progress;
- generate first analysis using confirmed requirements, ACSDM, implementation record, logs, and code;
- wait for authorization before changing code.

## Re-submission

`<FEATURE-ID> 重新提交策划验收` creates a new round. Include the prior bug IDs, fix summary, verification evidence, and affected acceptance points. Do not delete previous failures.

## Completion

`<FEATURE-ID> 策划已验收（任务完毕）` may complete only if:

- every mandatory acceptance point in the current round passed;
- no blocking bug remains open;
- the feature is confirmed;
- an approved plan and implementation submission exist;
- the user issued the exact completion command.

Update both documents and completion metadata. ACSDM recording remains opt-in through `并记录` or the ACSDM recording command.
