# ACSDM Usage Guide

## Install

A personal Codex install uses this folder:

```text
C:\Users\<user>\.codex\skills\acsdm-project-catalog
```

To share with another developer, send the whole `acsdm-project-catalog` folder. They should copy it into their Codex skills directory and restart or open a new Codex conversation.

## Initialize a Project

From a project root, ask Codex:

```text
使用 acsdm-project-catalog，在当前项目初始化 .ACSDM
```

Or run the script directly:

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File scripts/acsdm-init.ps1 -ProjectRoot "F:\AASMWORK\UnityProject\PJ-m032"
```

The skill should create or repair:

```text
<project root>/.ACSDM/
  0000ACSDMRootIndex.md
  00Rule/0000Index.md
  01ProjectOverview/0100Index.md
  02LevelEditor/0200Index.md
  03LevelLoading/0300Index.md
  04PlayerInput/0400Index.md
  05PropSystem/0500Index.md
  06Review/0600Index.md
  07ADMD/0700Index.md
```

It should add `.ACSDM/` to `<project root>/.git/info/exclude` when the project is a valid git repository. It must not modify project `.gitignore` unless the user explicitly requests it.

Do not initialize, export, or migrate ACSDM into `<project root>/docs/`. That directory is reserved for Orange Unity Forge. When ACSDM records reference PCTR artifacts, use `<project root>/.PCTR/A/<document-code>/` or `<project root>/.PCTR/B/<document-code>/` according to the active mode.

## External Notes

External folders such as `F:\AAAASMWORK\ALLNote\M032` are examples, references, or migration sources. They are not the live catalog root. Use them only when the user explicitly asks to scan or migrate content.

## Test Prompts

Use these prompts after installation:

```text
使用 acsdm-project-catalog，在当前项目初始化 .ACSDM
```

Expected: creates or verifies `.ACSDM` directly under the project root with eight modules and indexes.

```text
按照项目规范，实现一个弹窗功能，先查阅相关文档
```

Expected: reads `.ACSDM/00Rule/0000Index.md` before implementation and presents A/B/C if the request is broad.

```text
查阅关卡加载相关文档
```

Expected: reads `.ACSDM/0000ACSDMRootIndex.md`, then `.ACSDM/03LevelLoading/0300Index.md`, then relevant docs only.

```text
开始实施并记录
```

Expected: creates a new numbered document in the matched module and updates indexes.

## Modify the Skill

- Change trigger coverage in `SKILL.md` frontmatter `description`.
- Change module matching and prompt behavior in `references/retrieval-policy.md`.
- Change indexes and folder schema in `references/index-schema.md`.
- Change new document layout in `references/document-template.md`.
- Change deterministic filesystem behavior in `scripts/*.ps1`.

After modification, run:

```powershell
python C:\Users\<user>\.codex\skills\.system\skill-creator\scripts\quick_validate.py C:\Users\<user>\.codex\skills\acsdm-project-catalog
```

Then open a new Codex conversation and try the test prompts above.

## PCTR Dual-Mode Integration

Exact mode commands:

```text
启用PCTR-A
启用PCTR-B
```

- Mode A uses the legacy paired requirement and planning-confirmation/acceptance documents.
- Mode B uses one human development document, one role-based SDD per feature, local implementation-plan paths, and append-only bug-record paths.
- ACSDM records must include the active PCTR mode and use the matching confirmation source.
- PCTR-A persistent paths use `.PCTR/A/<document-code>/`; PCTR-B persistent paths use `.PCTR/B/<document-code>/`.
