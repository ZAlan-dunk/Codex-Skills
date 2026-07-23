# PCTR-B Lightweight Planner Confirmation Workflow

## Purpose

PCTR-B must not use a full Orange Unity Forge role-based SDD as the first planner confirmation surface. The first confirmation document is a lightweight planner-readable document focused on a short feature brief, real ambiguities, and useful improvement suggestions. Full functional understanding and breakdown stay in the local decomposition file.

The flow is:

```text
planning feature
  -> ACSDM reads related rules/history indexes
  -> PCTR-B saves source snapshot
  -> PCTR-B writes local decomposition
  -> PCTR-B writes one lightweight planner confirmation document
  -> planner answers per-item code blocks
  -> PCTR-B updates decomposition
  -> OUF generates detailed SDD from the confirmed decomposition
  -> programmer confirms SDD before implementation
```

## Commands

### `阅读这个功能生成策划确认文档`

Read the current or explicitly named PCTR-B feature and create a lightweight planner confirmation Markdown document. Do not upload to Feishu unless the user explicitly asks for upload.

Required actions:

1. Resolve exactly one PCTR-B feature by Feature ID or current feature context.
2. Read the matched planning source section and current source revision.
3. Save a source snapshot under `.PCTR/B/<document-code>/snapshots/<FEATURE-ID>-source-snapshot.md`.
4. Ask ACSDM, when available, for related project rules, historical development records, and code-evidence indexes. Store only compact index facts and paths; do not paste full ACSDM document bodies.
5. Save a local decomposition under `.PCTR/B/<document-code>/decompositions/<FEATURE-ID>-planning-decomposition.md`.
6. Render `assets/pctr-b-planner-confirmation-template.md` to `.PCTR/B/<document-code>/confirmations/<FEATURE-ID>-planner-confirmation.md`, or another user-supplied target.
7. Update sidecar `planner_confirmation.status=pending`, local paths, source revision, source snapshot hash, must-answer ambiguity IDs, and confirmation item IDs.

### `策划已确认`

Read the current feature's planner confirmation document, parse every per-item reply code block, update the decomposition, and decide whether detailed SDD generation is unlocked.

Required actions:

1. Locate exactly one current planner confirmation document from sidecar or Feature ID.
2. Parse the reply code block below each ambiguity / confirmation item. Use the item heading number as the identity; do not require or parse an item ID inside the code block. Do not rely on a document-level reply section.
3. If any must-answer ambiguity has an empty or invalid reply, set `planner_confirmation.status=needs_revision` and stop.
4. Write the selected option, planner supplement, resolved rule, and unresolved items back into the decomposition file.
5. If all must-answer ambiguities are resolved, set `planner_confirmation.status=confirmed` and `sdd_generation.status=ready`.
6. Do not generate SDD, upload Feishu, or implement code unless the user separately issues the next command.

### `生成详细 SDD 工件`

Requires `planner_confirmation.status=confirmed` and a current decomposition file. PCTR-B hands the confirmed decomposition to OUF. OUF generates the role-based SDD for programmers, QA, and Tech Lead.

The OUF SDD request must include:

- exact Feature ID and source heading path;
- source URL and revision;
- confirmed decomposition path and hash;
- resolved ambiguity decisions;
- ACSDM/history index summary;
- instruction not to invent new planner-facing ambiguities when PCTR-B already resolved them.

### `程序已确认，开始实施`

Requires a current SDD and explicit user implementation authorization. For small low-risk changes, PCTR-B may allow direct implementation from the confirmed SDD plus a short local implementation checklist. For cross-module, high-risk, save/protocol, external SDK, or architecture changes, generate and approve a separate implementation plan before code edits.

## Real Ambiguity Rule

Do not fabricate ambiguities. Create an ambiguity only when at least one condition is true:

1. The planning source does not specify a rule that implementation or QA must know.
2. The planning source contradicts itself.
3. The planning source conflicts with ACSDM project rules or known historical implementation.
4. The planning source gives a goal but omits trigger, end condition, priority, lifecycle, or exception behavior.
5. Without a decision, programmers could reasonably implement two different behaviors.

If no must-answer ambiguity exists, write: `本轮未发现需要策划确认的歧义点。`

## Per-Item Reply Blocks

There is no document-level reply section. Every ambiguity and every planner-facing confirmation / improvement item must include its own reply code block immediately under the item. The code block contains only two fields: `选择：` and `补充：`; the item number comes from the heading above it.

Required ambiguity item format:

````markdown
### A-01：<question>

为什么需要确认：<one short paragraph>

选项：

- A：<option>
- B：<option>
- C：<option, optional>

推荐：<option and reason>

影响：<short implementation / QA / player impact>

```text
选择：
补充：
```
````

Required confirmation / improvement item format:

````markdown
### C-01：<item>

建议确认或补充：<content>

推荐处理：<recommendation>

```text
选择：
补充：
```
````

## Content Boundaries

The planner confirmation document should be short and readable:

- write only a short feature-demand description in the planner confirmation document; keep full understanding and breakdown in the local decomposition file;
- separate planner-facing issues from programmer/resource/owner issues;
- do not include implementation class names, API sketches, code drafts, or long file path lists unless necessary for evidence;
- do not paste source planning prose, Feishu XML, images, tables, or ACSDM full bodies;
- list evidence as links, revisions, file paths, headings, and compact facts only.

## Local Artifact Layout

Default files:

```text
.PCTR/B/<document-code>/snapshots/<FEATURE-ID>-source-snapshot.md
.PCTR/B/<document-code>/decompositions/<FEATURE-ID>-planning-decomposition.md
.PCTR/B/<document-code>/confirmations/<FEATURE-ID>-planner-confirmation.md
.PCTR/B/<document-code>/sdd/<FEATURE-ID>-sdd.md
```

The snapshot is immutable source evidence. The decomposition is the living PCTR-B input to OUF. The confirmation document is the human planner surface. The SDD is generated only after planner confirmation.

