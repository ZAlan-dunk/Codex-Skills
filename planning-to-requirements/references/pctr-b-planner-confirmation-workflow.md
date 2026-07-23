# PCTR-B Lightweight Planner Confirmation Workflow

## Purpose

PCTR-B must not use a full Orange Unity Forge role-based SDD as the first planner confirmation surface. The first confirmation document is a lightweight planner-readable document focused on a short feature brief, real ambiguities, and useful improvement suggestions. Full functional understanding and breakdown stay in the local decomposition file.

The flow is:

```text
planning feature
  -> ACSDM reads related rules/history indexes
  -> PCTR-B opens .PCTR/<planning-version>/<FEATURE-ID>/
  -> PCTR-B writes the single A-02 decomposition file
  -> PCTR-B writes the A-01 lightweight planner confirmation snapshot
  -> PCTR-B returns the native A-01 Markdown path and exact manual-upload target
  -> planner answers per-item code blocks
  -> PCTR-B updates decomposition
  -> OUF generates detailed SDD from the confirmed decomposition
  -> programmer confirms SDD before implementation
```

## Commands

### `阅读这个功能生成策划确认文档`

Read the current or explicitly named PCTR-B feature and create a lightweight planner confirmation Markdown file. PCTR-B has only one Feishu human document, so return the native A-01 `.md` path and exact matched feature section for manual upload; never create or import a separate planner-confirmation Docx/Wiki.

Required actions:

1. Resolve exactly one PCTR-B feature by Feature ID or current feature context.
2. Read the matched planning source section and current source revision.
3. Resolve or create the feature folder `.PCTR/<planning-version>/<FEATURE-ID>/`.
4. Ask ACSDM, when available, for related project rules, historical development records, and code-evidence indexes. Store only compact index facts and paths; do not paste full ACSDM document bodies.
5. Save or update exactly one local decomposition file: `.PCTR/<planning-version>/<FEATURE-ID>/A-02-feature-decomposition.md`. Put the source snapshot/fingerprint inside this file instead of creating another Markdown snapshot file.
6. Render `assets/pctr-b-planner-confirmation-template.md` to `.PCTR/<planning-version>/<FEATURE-ID>/A-01-planner-confirmation-snapshot.md`, or another user-supplied target only if it still keeps the A-01 name under the same feature folder.
7. Do not automatically upload A-01. Return the local A-01 path and exact matched `2. SDD确认文档` heading; the user/program manually uploads it and then registers the attachment identity.
8. Update sidecar `planner_confirmation.status=pending`, `feature_artifact_dir`, A-01/A-02/B-01 artifact paths, `feishu_blocks`, source revision, source snapshot hash, must-answer ambiguity IDs, confirmation item IDs, and sync time. Attachment name/token/block/URL and containing-document revision are filled after manual upload registration.

Always provide the local A-01 path plus exact Feature ID/heading for manual upload. Never fall back to creating a Feishu document.

### `策划已确认`

Read the current feature's planner confirmation document, parse every per-item reply code block, update the decomposition, and decide whether detailed SDD generation is unlocked.

Required actions:

1. Locate exactly one current planner confirmation document from sidecar or Feature ID.
2. Parse the reply code block below each ambiguity / confirmation item. Use the item heading number as the identity; do not require or parse an item ID inside the code block. Do not rely on a document-level reply section.
3. Validate each reply against the item's listed preselection codes:
   - one listed code is valid, with `补充：` preserved as an optional qualification;
   - empty `选择：` plus non-empty `补充：` is a valid custom planner solution and must be stored as `custom` with the supplement as the authoritative rule;
   - both fields empty means unanswered;
   - an unknown or multiple code is invalid unless that item explicitly declares multi-select.
4. If any must-answer ambiguity has an empty or invalid reply, set `planner_confirmation.status=needs_revision` and stop. An unanswered optional item does not block, but it remains unresolved/out of scope and must not be interpreted as accepting the recommendation.
5. Write the selected option, planner supplement, resolved rule, and unresolved items back into the decomposition file.
6. If all must-answer ambiguities are resolved, set `planner_confirmation.status=confirmed` and `sdd_generation.status=ready`.
7. Do not generate SDD, upload Feishu, or implement code unless the user separately issues the next command.

### `生成详细 SDD 工件`

Requires `planner_confirmation.status=confirmed` and the current `A-02-feature-decomposition.md`. PCTR-B hands this confirmed decomposition and the expected `B-01-runtime-sdd.md` output path to OUF. OUF generates the role-based SDD for programmers, QA, and Tech Lead.

The OUF SDD request must include:

- exact Feature ID and source heading path;
- source URL and revision;
- confirmed `A-02-feature-decomposition.md` path and hash;
- resolved ambiguity decisions;
- ACSDM/history index summary;
- expected output path `.PCTR/<planning-version>/<FEATURE-ID>/B-01-runtime-sdd.md`;
- instruction not to invent new planner-facing ambiguities when PCTR-B already resolved them;
- instruction to produce OUF-owned artifacts normally and produce `B-01-runtime-sdd.md` only when the PCTR workflow requests a PCTR-bound SDD snapshot.

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

There is no document-level reply section. Every ambiguity and every planner-facing confirmation / improvement item must include its own preselection list and reply code block immediately under the item. The code block contains only two fields: `选择：` and `补充：`; the item number comes from the heading above it.

Option rules:

- provide two to six meaningful alternatives using consecutive uppercase codes from `A`;
- make the options concrete enough to determine implementation and QA behavior;
- do not use vague `同意/不同意` choices when real behavior alternatives can be stated;
- do not add a generic “其他” option merely to force a selection;
- write the recommended option code and recommendation reason as separate fields;
- allow the planner to ignore all preselected options by leaving `选择：` empty and writing a custom rule in `补充：`.

Required ambiguity item format:

````markdown
### A-01：<question>

为什么需要确认：<one short paragraph>

预选项：

- A：<option>
- B：<option>
- C：<option, when meaningful>
- D：<option, when meaningful>

推荐选择：<one listed code>

推荐原因：<one short reason>

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

预选项：

- A：<option>
- B：<option>
- C：<option, when meaningful>

推荐选择：<one listed code>

推荐原因：<one short reason>

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
.PCTR/<planning-version>/<FEATURE-ID>/A-01-planner-confirmation-snapshot.md
.PCTR/<planning-version>/<FEATURE-ID>/A-02-feature-decomposition.md
.PCTR/<planning-version>/<FEATURE-ID>/B-01-runtime-sdd.md
```

`A-01` is the human planner surface. `A-02` is the only living PCTR-B decomposition and includes the source snapshot/fingerprint. `B-01` is generated only after planner confirmation and is the detailed SDD that OUF/program can read for direct execution. Do not create additional `A-*.md` files or multiple decomposition versions inside the feature folder.

`A-01` and `B-01` are uploaded manually as attachments in the same matching feature section of the one Feishu development document and then registered in the sidecar. They are different lifecycle artifacts and may coexist under `2. SDD确认文档`; neither may be converted into or replaced by a per-feature Docx/Wiki.

