# Update and Monitoring

## Monitored Documents

Track three sources:

1. planning source;
2. requirement development document;
3. planning confirmation and acceptance document.

Record document IDs, revisions, heading fingerprints, feature mappings, last synchronization time, processed change IDs, and human-maintained fields.

## Comparison

Compare heading hierarchy, normalized content, tables/lists, deletion marks, media changes, source movement, confirmation responses, acceptance results, and feature-state changes.

## Authority

- Planning source: original requirement authority.
- Planning confirmation document: planner decision and acceptance authority.
- Requirement document: technical specification, route, development, and completion authority.

## Synchronization

- Regenerate only affected generated sections.
- Preserve planner responses, confirmation metadata, acceptance rounds, priority, owner, estimate, progress, test state, and notes.
- Keep stable IDs.
- Mark deleted source features pending removal until human confirmation.
- Never overwrite a planner-edited field from generated content.
- Detect concurrent revision changes and stop with a conflict report.

## State Change Log

Append feature ID, prior/new state, triggering command, source revisions, synchronized fields, preserved human fields, conflicts, operator, and timestamp.
