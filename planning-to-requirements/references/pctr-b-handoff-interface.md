# PCTR-B Orange SDD Upload Interface

## Purpose

Allow Orange Unity Forge to hand off one newly generated role-based SDD to an existing PCTR-B feature. In the normal active path, this interface consumes the receipt from `pctr-b-feature-lookup-interface.md`. Use the narrow fallback only when PCTR is disabled and the SDD already contains an exact Feature ID obtained earlier.

## Gate

Normal coexisting path requires:

- `orange_unity_forge=true`;
- `pctr=true` and `pctr_mode=B`.
- a fresh lookup receipt matching the current sidecar/source revision;
- SDD metadata matching the receipt's Feature ID, exact title, heading path, source identity, development document, and target.

Fallback path requires:

- `orange_unity_forge=true`;
- `pctr=false`;
- `.codex/skill-gates.json` contains `pctr_b_handoff_interface="orange-sdd-upload-only"`;
- the generated SDD contains an exact PCTR Feature ID;
- a registered PCTR-B development document and sidecar contain that same ID;
- the sidecar identifies one unambiguous Feishu parent/target.

The fallback does not set `pctr=true` or `pctr_mode=B`.

## Allowed Operation

For one Feature ID only:

1. Read the generated SDD.
2. Read the matching feature section and sidecar entry identified by the receipt.
3. Validate SDD identity, required role sections, status, local path, source metadata, and lookup receipt freshness.
4. Upload/create the SDD as a Feishu Docx under the configured target using the `lark-doc` Markdown workflow.
5. Write only:
   - local SDD path;
   - Feishu SDD URL/token;
   - uploaded SDD revision/status;
   - synchronization time.
6. Leave both confirmation checkboxes unchecked and keep `sdd_confirmation_status=pending`.
7. Return the uploaded URL and updated PCTR-B document path.

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
- upload to a guessed Feishu location.

## Failure Rules

Stop before external write when:

- Feature ID is missing or duplicated;
- the lookup receipt is missing/stale or differs from SDD metadata;
- zero or multiple SDDs match;
- document/sidecar identity differs;
- Feishu parent/target is missing or ambiguous;
- the SDD validator fails;
- the target feature already links a newer revision.

After a successful upload, use `sync_pctr_b_sdd.py` with `--confirmation pending` to update local artifacts deterministically.
