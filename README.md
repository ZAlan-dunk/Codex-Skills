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

## Validation

Run the bundled Codex skill validator against each directory:

```powershell
$env:PYTHONUTF8 = "1"
python C:\Users\<username>\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\acsdm-project-catalog
python C:\Users\<username>\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\planning-to-requirements
```

PowerShell 5.1 and locale-dependent Python installations may require `PYTHONUTF8=1` because the skill documentation is UTF-8.

## Security and portability

The repository does not include personal access tokens, Feishu credentials, project-private source code, or project-local `.ACSDM` content. The skills operate on the installing user's own projects and available CLI/API integrations.