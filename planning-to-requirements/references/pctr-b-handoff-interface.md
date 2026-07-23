# PCTR-B Orange SDD Markdown Attachment Interface

## Purpose

Allow Orange Unity Forge to hand off one newly generated feature-local `B-01-runtime-sdd.md` role-based SDD Markdown file to an existing PCTR-B feature section. In the normal active path, this interface consumes the receipt from `pctr-b-feature-lookup-interface.md`. Use the narrow fallback only when PCTR is disabled and the SDD already contains an exact Feature ID obtained earlier. Never create a separate Feishu SDD document.

## Gate

Normal coexisting path requires:

- `orange_unity_forge=true`;
- `pctr=true` and `pctr_mode=B`.
- a fresh lookup receipt matching the current sidecar/source revision;
- SDD metadata matching the receipt's full/base Feature IDs, planning sequence, exact title, heading path, source identity, development document, confirmed A-02 decomposition path, and B-01 output path.

Fallback path requires:

- `orange_unity_forge=true`;
- `pctr=false`;
- `.codex/skill-gates.json` contains `pctr_b_handoff_interface="orange-sdd-upload-only"`;
- the generated SDD contains an exact PCTR Feature ID;
- a registered PCTR-B development document and sidecar contain that same ID;
- the sidecar identifies one unambiguous Feishu development document and feature section.

The fallback does not set `pctr=true` or `pctr_mode=B`.

## Allowed Operation

For one Feature ID only:

1. Read the generated SDD and require its path/name to equal the receipt's `.PCTR/<planning-version>/<FEATURE-ID>/B-01-runtime-sdd.md`.
2. Read the matching feature section and sidecar entry identified by the receipt.
3. Validate SDD identity, required role sections, status, local path, source metadata, and lookup receipt freshness.
4. Insert the local `.md` file itself as an attachment directly inside the matching feature section only when exact-position insertion and the resulting block can be verified.
5. Write only:
   - local SDD path, which must be the feature-local `B-01-runtime-sdd.md`;
   - attachment name/token/URL;
   - containing development-document revision and SDD status/version;
   - synchronization time.
6. Leave both confirmation checkboxes unchecked and keep `sdd_confirmation_status=pending`.
7. Return the attachment reference and updated PCTR-B document path.

If automatic exact-position insertion or callout preservation is unreliable, stop before external write and return the local Markdown path plus the exact target feature heading for user manual upload. After manual insertion, `登记PCTR-B Markdown附件 <FEATURE-ID>` performs the state-only registration.

## Forbidden Operation

Do not:

- generate or restructure PCTR documents;
- inspect unrelated PCTR features;
- change confirmation checkboxes;
- mark an SDD confirmed or ambiguous;
- create implementation plans;
- implement code;
- enter acceptance or bug lifecycle states;
- invoke ACSDM;
- create a separate Feishu SDD document;
- append the attachment to a guessed or unrelated Feishu position.

## Failure Rules

Stop before external write when:

- Feature ID is missing or duplicated;
- the lookup receipt is missing/stale or differs from SDD metadata;
- zero or multiple SDDs match, or the SDD is not named `B-01-runtime-sdd.md` under the matched feature folder;
- document/sidecar identity differs;
- Feishu development document or exact feature section is missing or ambiguous;
- the SDD validator fails;
- the target feature already records a newer attachment snapshot.

After a successful automatic or manual attachment, use `sync_pctr_b_sdd.py` with `--confirmation pending`, attachment metadata, and containing-document revision to update local artifacts deterministically.
