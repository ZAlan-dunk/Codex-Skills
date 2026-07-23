# PCTR Mode Routing

## Gate Source

Read `<project root>/.codex/skill-gates.json` before any PCTR action.

| Exact standalone command | Gate result | Workflow |
|---|---|---|
| `启用 PCTR` | `pctr=true`, `pctr_mode=A` | Backward-compatible PCTR-A |
| `启用PCTR-A` | `pctr=true`, `pctr_mode=A` | PCTR-A |
| `启用PCTR-B` | `pctr=true`, `pctr_mode=B` | PCTR-B |
| `禁用 PCTR` | `pctr=false`, `pctr_mode=null` | Disabled |

Both modes may coexist with Orange Unity Forge and ACSDM when their gates are independently enabled. Do not infer a mode from a document, path, feature ID, or conversation wording.

## Directory Ownership

PCTR owns `<project root>/.PCTR/` for persistent artifacts and never writes new artifacts under `<project root>/docs/`.

| Mode | Default persistent directory |
|---|---|
| PCTR-A | `<project root>/.PCTR/A/<document-code>/` |
| PCTR-B | `<project root>/.PCTR/<planning-version>/`, with one `<FEATURE-ID>/` folder per feature |

`docs/pctr/` is a legacy migration source only. Orange Unity Forge owns `docs/`; ACSDM owns `.ACSDM/`; Orange working artifacts may use `CodexTemp/OrangeUnityForge/` under its own rules.

## PCTR-A

Use the legacy paired-document workflow:

```text
planning source
  -> requirement development document
  -> planning confirmation and acceptance document
  -> confirmed route-specific plan
  -> implementation
  -> planning acceptance / bug loop
```

Apply atomic decomposition, confirmation IDs, acceptance IDs, paired revisions, multi-block confirmation, and the existing validators.

## PCTR-B

Use the single-development-document workflow:

```text
planning source
  -> one concise development document
  -> .PCTR/<planning-version>/<FEATURE-ID>/A-01 planner confirmation snapshot
  -> .PCTR/<planning-version>/<FEATURE-ID>/A-02 single decomposition file
  -> .PCTR/<planning-version>/<FEATURE-ID>/B-01 detailed SDD attachment inside each matching feature section
  -> local implementation-plan artifact path
  -> implementation
  -> local bug-fix record paths
```

The human-facing Feishu document stays compact but contains planning-grounded requirement descriptions. It is the only Feishu document PCTR-B creates. A local sidecar manifest carries machine lifecycle state, planning-version roots, feature artifact folders, planning-sequence IDs, attachment references, and stable source mapping.

## No Mixed Documents

- Never add PCTR-A confirmation/acceptance blocks to a PCTR-B document.
- Never replace PCTR-A atomic features with source headings in place.
- Never reuse one sidecar for documents from different modes.
- When migration is requested, generate a new target-mode document, preserve source links and IDs where possible, and mark the old document superseded. Do not overwrite it.

## Backward Compatibility

`启用 PCTR` selects Mode A so existing commands, templates, scripts, and paired documents continue to work unchanged.
