# PCTR-B Feature Identity Lookup Interface

## Purpose

Allow Orange Unity Forge to resolve the exact PCTR-B feature identity before generating a role-based SDD. This is a read-only normal integration interface, not a user-facing lifecycle command.

## Preconditions

- `orange_unity_forge=true`;
- `pctr=true` and `pctr_mode=B`;
- PCTR-B has already created one registered local development document and sidecar;
- the Feishu development-document URL/revision are recorded;
- Orange has the source planning URL/token, source revision, and exact planning heading path or source fingerprint.

If any precondition is absent, stop before SDD generation. Orange must not create or repair the PCTR-B document through this interface.

## Input

Use the strongest available source identity:

1. source planning URL/token;
2. source revision;
3. exact heading path and exact title;
4. source heading fingerprint when present;
5. document code when already known;
6. planning sequence or base Feature ID when already known.

Do not use title-only fuzzy matching.

## Lookup Procedure

1. Select exactly one registered PCTR-B development document/sidecar by source identity or document code.
2. Read only feature entries relevant to the requested source heading.
3. Match the source revision and exact heading path/fingerprint.
4. Require exactly one feature.
5. Return a lookup receipt without changing either file.

## Lookup Receipt

Return:

```text
PCTR Feature ID:
PCTR Base Feature ID:
Planning sequence:
Feature title:
Source heading path:
Source fingerprint:
Source URL/token:
Source revision:
PCTR-B local development document:
PCTR-B sidecar:
Feishu development document URL/token:
PCTR feature artifact folder:
Confirmed A-02 decomposition path and hash:
Expected B-01 runtime SDD output path:
Existing local SDD path, if any:
Existing attachment token/URL and containing-document revision, if any:
```

Orange must copy the exact full/base Feature IDs, planning sequence, title, heading path, source identity, Feishu development-document link, A-02 decomposition identity, and B-01 output path into the SDD metadata. The lookup receipt is valid only for the matched source revision and sidecar state.

## Forbidden Operations

Do not:

- assign or renumber a Feature ID;
- create, upload, or restructure a PCTR-B development document;
- modify the sidecar or human document;
- change confirmation state;
- inspect unrelated features;
- guess from title similarity or document order;
- continue when the source revision is stale or the Feishu development-document identity is ambiguous.

## Failure Rules

Stop before SDD generation when:

- zero or multiple documents match;
- zero or multiple feature entries match;
- the source revision, heading path, or fingerprint conflicts;
- the Feature ID is missing or duplicated;
- the registered Feishu development document is missing;
- the existing attached SDD snapshot is newer than the local source context.

After a successful lookup, Orange may generate one Draft local Markdown SDD at the returned `B-01-runtime-sdd.md` path, statically validate it, and invoke `pctr-b-handoff-interface.md` for exact-position attachment or manual-upload handoff.
