# ACSDM OUF Link Index

## Purpose

`08OUFDevelopmentLogs/0800Index.md` lets ACSDM find Orange Unity Forge development artifacts without duplicating them. OUF remains the owner of `docs/forge-artifacts/`; ACSDM stores only compact link metadata.

## Default Locations

```text
<project root>/docs/forge-artifacts/
<project root>/.ACSDM/08OUFDevelopmentLogs/0800Index.md
```

## Update Command

```powershell
powershell -ExecutionPolicy Bypass -File acsdm-project-catalog/scripts/acsdm-link-ouf.ps1 -ProjectRoot <project-root>
```

Optional custom OUF root:

```powershell
powershell -ExecutionPolicy Bypass -File acsdm-project-catalog/scripts/acsdm-link-ouf.ps1 `
  -ProjectRoot <project-root> `
  -ForgeArtifactsRoot <project-root>/docs/forge-artifacts
```

## Retrieval Rule

1. Read `.ACSDM/0000ACSDMRootIndex.md`.
2. If the task mentions a PCTR Feature ID, base Feature ID, OUF, SDD, Plan, Report, Evidence, implementation log, or previous development process, read `.ACSDM/08OUFDevelopmentLogs/0800Index.md`.
3. Filter by Feature ID first, then title/topic, then artifact type.
4. Open only the selected original OUF file(s).
5. Summarize the needed facts back to the active workflow. Do not create ACSDM copies of OUF documents.

## Artifact Type Detection

| Type | Typical path/name signal |
|---|---|
| `context-brief` | `brief`, `context` |
| `sdd` | `spec`, `sdd` |
| `plan` | `plan` |
| `report` | `report` |
| `evidence` | `evidence` |
| `log` | `log`, `journal` |
| `bug-report` | `bug`, `fix` |
| `verification` | `verify`, `test`, `qa` |
| `other` | no stronger match |

## Non-Duplication Rule

ACSDM may quote or summarize a small fact from an OUF artifact when answering a task, but it must not create a second ACSDM development-log document containing the same body. If long-term recording is needed, record the decision/result and keep the OUF path/hash as evidence.
