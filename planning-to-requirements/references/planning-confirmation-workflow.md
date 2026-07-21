# PCTR-A Planning Confirmation Workflow

Use only when `pctr_mode=A`. PCTR-B uses the uploaded SDD confirmation checkboxes.

## Purpose

Create a planner-facing document after the requirement development document. It is the source of truth for planning decisions and planning acceptance, while the requirement document remains the technical source of truth.

## Feature Section

Every active feature must include:

1. feature ID and title;
2. short implementation description understandable without code knowledge;
3. current scope and visible player/product behavior;
4. confirmation items;
5. final confirmation summary and metadata;
6. planner acceptance checklist;
7. acceptance rounds and bug descriptions.

## Confirmation Item Schema

Use stable confirmation IDs:

```text
PC-<FEATURE-ID>-<NN>
```

Each item contains:

- source statement(s);
- ambiguity or missing decision;
- impact on implementation or acceptance;
- recommended options without silently selecting one;
- blocking: yes/no;
- planner response;
- item status: pending/confirmed/rejected;
- confirmed by/time.

## Blocking Rules

Blocking examples:

- whether the feature is in scope;
- core trigger and cancellation behavior;
- final numerical rule;
- priority between conflicting behaviors;
- persistence/session/account boundary;
- reward/advertising success and failure behavior;
- data compatibility or migration behavior.

Non-blocking examples:

- final color or asset;
- minor animation duration tuning;
- audio resource selection;
- wording polish that does not change logic.

Only all blocking items resolved plus an explicit user command may create `confirmed` status.

## Synchronization

The planning document is authoritative for planner-entered fields. The requirement document receives a synchronized copy containing:

- final confirmation summary;
- resolved item table;
- confirmation document ID/link/revision;
- confirmer and time;
- updated scope and acceptance;
- recalculated route;
- regenerated task capsule.

Preserve original planning text and previous conflict notes.

## Concurrent Edits

Before synchronization, compare both document revisions with the last synchronization state. Preserve human-entered priority, owner, estimate, planner responses, acceptance results, and notes. If both documents changed the same generated field, produce a conflict report instead of overwriting.
