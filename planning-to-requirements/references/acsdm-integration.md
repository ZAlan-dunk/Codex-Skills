# ACSDM Integration

## Boundary

PCTR owns requirement translation, planning confirmation, route orchestration, and planning acceptance state. ACSDM owns project-local knowledge retrieval and optional implementation/bug/completion records.

## Retrieval Order

1. Confirm `<project root>/.ACSDM`.
2. Read `.ACSDM/0000ACSDMRootIndex.md`.
3. Read `00Rule` for rule-first triggers.
4. Read matching module indexes and directly relevant documents.
5. Inspect referenced scripts, methods, and line ranges.
6. Record evidence and missing evidence.

## Feature-ID Commands

For `开始 <FEATURE-ID> 功能开发`:

- read the confirmed requirement feature section;
- read the synchronized planner summary;
- verify confirmation gate;
- retrieve ACSDM and code evidence;
- generate the route-specific plan only.

For `开始实施 <FEATURE-ID>`:

- require an approved plan;
- apply the ACSDM planning/authorization gate;
- modify only approved scope.

For acceptance failure:

- read the failed planner acceptance IDs and bug description;
- retrieve rules, historical implementation, implementation record, and related code;
- produce first analysis before edits.

For completion:

- update ACSDM only when the command includes `并记录` or the user separately requests recording.

## Record Content

Implementation or bug records should include:

- feature ID and bug ID;
- confirmed requirement revision;
- planner confirmation source;
- route and approved plan;
- changed files/methods/line ranges;
- verification commands/results;
- planning acceptance rounds and final result;
- risks, rollback, and completion time.

## Missing Catalog

If `.ACSDM` is unavailable, label implementation guidance provisional and prevent fabricated file paths or project mechanisms.
