# Codex Skills

This repository contains two reusable Codex skills for project knowledge retrieval and planning-to-development workflows.

## Included skills

### `acsdm-project-catalog`

Maintains and retrieves a project-local ACSDM Markdown knowledge catalog under `<project root>/.ACSDM`. It provides index-first retrieval, rule-first project guidance, implementation-record conventions, and PCTR lifecycle integration.

### `planning-to-requirements` (PCTR)

Converts planning documents and requirement drafts into development-ready requirement specifications plus a paired planning-confirmation and acceptance document. It supports stable feature IDs, ACSDM evidence retrieval, ABC/enhanced ABC/SDD routing, implementation gates, acceptance rounds, and bug-fix loops.

## Installation

Copy each complete skill directory into your Codex skills directory:

```text
C:\Users\<username>\.codex\skills\acsdm-project-catalog
C:\Users\<username>\.codex\skills\planning-to-requirements
```

Do not copy only `SKILL.md`; each skill depends on its `agents`, `references`, `assets`, and/or `scripts` directories.

Restart Codex or open a new task after installation.

## Independent Git tracking and updates

Keep a separate clone for each installation scope. This prevents the user-level tracking state from conflicting with a project-level tracking state.

Recommended clone locations:

```text
User scope:    C:\Users\<username>\.codex\skill-sources\Codex-Skills
Project scope: <project>\.agents\skill-sources\Codex-Skills
```

Each clone stores an ignored, scope-specific manifest after a successful update:

```text
.codex-skill-tracking.user.json
.codex-skill-tracking.project.json
```

The manifests record the source clone, target root, installed repository commit, timestamp, and installed skill paths. They are intentionally ignored by Git and never overwrite one another.

### Update user-level skills

Run this command from the user-scope clone:

```powershell
powershell -ExecutionPolicy Bypass -File .\Update-UserCodexSkills.ps1
```

### Update project-level skills

Run this command from the project-scope clone:

```powershell
powershell -ExecutionPolicy Bypass -File .\Update-ProjectCodexSkills.ps1
```

The updater performs a fast-forward-only pull, stages both skills, removes generated cache files, validates both staged copies, and only then replaces the installed copies. If copying or validation fails, the previous installed copies are retained or restored.

If GitHub access requires a proxy, configure it per tracking clone so the two scopes remain independent:

```powershell
git config --local http.proxy http://127.0.0.1:7897
git config --local https.proxy http://127.0.0.1:7897
```

Use `-SkipPull` only for an offline reinstall from the commit already present in that tracking clone.

## Validation

Run the bundled Codex skill validator against each directory:

```powershell
$env:PYTHONUTF8 = "1"
python C:\Users\<username>\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\acsdm-project-catalog
python C:\Users\<username>\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\planning-to-requirements
```

PowerShell 5.1 and locale-dependent Python installations may require `PYTHONUTF8=1` because the skill documentation is UTF-8.

## Security and portability

The repository does not include personal access tokens, Feishu credentials, project-private source code, project-local `.ACSDM` content, or local tracking manifests. The skills operate on the installing user's own projects and available CLI/API integrations.
