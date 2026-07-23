# Update and Monitoring

## Monitored Documents

PCTR-A tracks three sources:

1. planning source;
2. requirement development document;
3. planning confirmation and acceptance document.

PCTR-B tracks:

1. planning source;
2. single requirement development document;
3. local sidecar manifest;
4. per-feature local SDD identity, attachment token/URL/name, and containing development-document revision;
5. referenced implementation-plan and bug-record artifacts.

Record document IDs, revisions, heading fingerprints, feature mappings, last synchronization time, processed change IDs, and human-maintained fields.

Active local paths must resolve beneath `.PCTR/A/<document-code>/` for PCTR-A or `.PCTR/<planning-version>/` for PCTR-B. In PCTR-B, feature-local Markdown paths must be under `.PCTR/<planning-version>/<FEATURE-ID>/` and use `A-01-planner-confirmation-snapshot.md`, `A-02-feature-decomposition.md`, or `B-01-runtime-sdd.md`. Treat `docs/pctr/`, `.PCTR/B/<document-code>/`, `CodexTemp/PCTR/`, and PCTR-B SDD files under `CodexTemp/OrangeUnityForge/` as legacy locations: report them, migrate by copy when authorized, update active path fields, and do not delete the source without explicit permission.

## Comparison

Compare heading hierarchy, normalized content, tables/lists, deletion marks, media changes, source movement, confirmation responses, acceptance results, and feature-state changes.

## Authority

- Planning source: original requirement authority.
- Planning confirmation document: PCTR-A planner decision and acceptance authority.
- `A-01` planner confirmation snapshot and `A-02` decomposition: PCTR-B planner decision authority; `B-01-runtime-sdd.md` and its mutually exclusive checkbox state: program/SDD decision authority.
- Requirement document: technical specification, route, development, and completion authority.

## Synchronization

- Regenerate only affected generated sections.
- Preserve planner responses, confirmation metadata, acceptance rounds, priority, owner, estimate, progress, test state, and notes.
- Preserve base Feature IDs and legacy aliases; update the visible planning-sequence prefix when source hierarchy/order changes.
- Mark deleted source features pending removal until human confirmation.
- Never overwrite a planner-edited field from generated content.
- Detect concurrent revision changes and stop with a conflict report.

## State Change Log

Append feature ID, prior/new state, triggering command, source revisions, synchronized fields, preserved human fields, conflicts, operator, and timestamp.
