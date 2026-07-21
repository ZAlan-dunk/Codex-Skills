# ACSDM Integration

## Boundary

PCTR owns requirement translation, mode-specific confirmation, route orchestration, and planning acceptance state. ACSDM owns project-local knowledge retrieval and optional implementation/bug/completion records.

- PCTR-A confirmation authority: paired planning confirmation/acceptance document.
- PCTR-B confirmation authority: uploaded role-based SDD plus its synchronized confirmation state; the single development document is the human index.

## Retrieval Order

1. Confirm `<project root>/.ACSDM`.
2. Read `.ACSDM/0000ACSDMRootIndex.md`.
3. Read `00Rule` for rule-first triggers.
4. Read matching module indexes and directly relevant documents.
5. Inspect referenced scripts, methods, and line ranges.
6. Record evidence and missing evidence.

## Feature-ID Commands

For `开始 <FEATURE-ID> 功能开发`:

- read the active PCTR mode and the matching requirement feature section;
- PCTR-A: read the synchronized planner summary and confirmation revision;
- PCTR-B: read the confirmed SDD, Feishu revision, source feature section, and sidecar;
- verify the mode-specific confirmation gate;
- retrieve ACSDM and code evidence;
- generate the route-specific plan only.

For `批准 <FEATURE-ID> 技术方案`:

- verify the generated plan still matches the confirmed requirement revision and selected route;
- set the technical plan state to `approved`;
- do not modify code or ACSDM records.

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

For PCTR-B, also include:

- PCTR mode `B`;
- local and Feishu SDD paths/revisions;
- SDD confirmation result;
- local implementation-plan artifact path;
- all bug-record paths linked from the single development document.

## Missing Catalog

If `.ACSDM` is unavailable, label implementation guidance provisional and prevent fabricated file paths or project mechanisms.
