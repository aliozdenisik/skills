---
name: requirement-verification
description: Verify every mandatory requirement against implemented code and evidence after implementation, and gate completion on exact ID coverage. Use for delegated final requirement audits or completion checks against requirements.md; requirement authoring belongs to the requirements skill.
---

# Requirement Verification

Implementation stays flexible. Completion requires deterministic coverage and objective evidence. This is a solo-developer final verification layer, not a planning pipeline.

## Establish the source

Use the project's `requirements.md` as the sole authoritative requirements source. Read it in full, including constraints and acceptance criteria. Code, tests, conversations, and audit reports are evidence, not alternative specifications. If the file is absent, report `INCOMPLETE` and the missing source; do not reconstruct requirements from implementation.

Preserve the existing requirement wording and acceptance-criteria structure, including nested criteria, thresholds, and exceptions. The companion `requirements` skill specifies verifiability but no fixed acceptance-criteria template: do not invent a replacement. An ambiguous criterion or unresolved mandatory TBD/TBR blocks satisfaction until clarified in `requirements.md`.

Every mandatory requirement must have a unique, stable ID. Preserve existing IDs; assign missing ones once using the existing convention or `REQ-001`, `REQ-002`, etc. Never renumber, reuse retired IDs, or weaken/delete requirements to pass the gate. If IDs are duplicated or mandatory scope is ambiguous, report the source defect and resolve it before claiming completion. Goals (`should`) and declarations (`will`) are not mandatory unless explicitly designated as such; `shall`, `must`, and equivalent obligations are mandatory.

For deterministic extraction without reformatting acceptance criteria, place exactly one standalone marker immediately before each mandatory requirement declaration, using its existing ID:

```markdown
<!-- requirement: REQ-001 -->
```

Markers are metadata in `requirements.md`, not a second requirements list. Read the whole document to ensure every mandatory declaration has a marker and no optional item or cross-reference is marked. Nested acceptance criteria remain attached to their parent; independently declared mandatory requirements receive their own IDs. Add only IDs/markers where needed. If source editing is unavailable, report the blocker instead of claiming complete coverage.

## Verify after implementation

1. Extract the expected ID inventory mechanically with the bundled helper (resolve `<skill>` to this skill's directory):
   ```bash
   python3 <skill>/scripts/coverage_gate.py extract requirements.md > /tmp/requirement-inventory.json
   ```
   Use a task-specific temporary path for concurrent work. The inventory is a disposable snapshot, never an editable source of truth.
2. Delegate the extracted IDs using the subagent protocol below. Each verifier audits its assigned IDs against the current codebase and relevant tests. Cover the entire requirement and every acceptance criterion, including error cases and measurable limits. Reuse suitable existing checks; add or run only checks necessary to establish missing evidence. A green suite alone does not prove unrelated requirements.
3. Record one row per expected ID in an audit Markdown table. Choose only the verification methods needed for that requirement: `TEST` (executed assertions), `INSPECTION` (direct examination), `ANALYSIS` (reasoning/calculation using observed inputs), `DEMONSTRATION` (observed operation). Combine methods with ` + ` only when necessary; use `—` if no verification occurred. Do not require every method or add method fields to the source.
4. Require concrete, current evidence for `SATISFIED`: test command/result and relevant test, file/line or symbol with the inspected finding, reproducible calculation with inputs/result, or demonstration steps and observed output. Explain the evidence-to-criterion link briefly. Test existence, intended behavior, agent assertions, and stale results are insufficient. Inspection can prove structural requirements; choose runtime checks when the required behavior cannot be established by reading code. Unavailable execution or dependencies means `UNVERIFIED` for the unproven behavior, not an assumed pass.
5. Compare the inventory with audit rows mechanically:
   ```bash
   python3 <skill>/scripts/coverage_gate.py check requirements.md /tmp/requirement-inventory.json audit.md
   ```
   Resolve missing, extra, and duplicate IDs. If requirements changed, re-extract and reassess affected evidence; if implementation changed, rerun affected verification. The helper checks coverage and evidence-field presence, not evidence truth, semantic marker completeness, or code freshness; those remain the agent's responsibility.

## Status and completion

Use these statuses consistently; a proven contradiction takes precedence over partial coverage or uncertainty:

- `SATISFIED`: the entire requirement and all acceptance criteria are supported by concrete evidence.
- `PARTIAL`: some required behavior is demonstrably implemented, with a known unmet portion.
- `MISSING`: the required implementation is absent.
- `CONTRADICTED`: observed behavior or implementation conflicts with the requirement, including a relevant failing assertion.
- `UNVERIFIED`: evidence is insufficient, blocked, ambiguous, or not current. If implemented portions are proven but the remainder is only unknown, use this instead of `PARTIAL`.

Report only the compact table and a short verdict/coverage line:

```markdown
| ID | Verification | Evidence | Status | Missing Work |
| --- | --- | --- | --- | --- |
| REQ-001 | TEST | `pytest tests/test_export.py -q`: 3 passed; covers required formats | SATISFIED | — |
```

Keep cells single-line; escape literal pipes as `\|`. For unsuccessful rows, state the smallest specific fix, missing check, or clarification in `Missing Work`. Report source/coverage defects briefly below the table without inventing requirement IDs.

Say `COMPLETE` only when the mandatory inventory is valid and nonempty, expected and audited IDs match exactly once each, every row is `SATISFIED`, and the evidence substantively covers every criterion in the current source and implementation. Otherwise say `INCOMPLETE`, even if all implemented tests pass. Zero extracted requirements is a source/coverage blocker, never a vacuous pass.

When entered from the implementation loop, return unsuccessful rows to its coordinator for targeted fixes, cleanup, and another delegated audit. Verifiers report findings rather than modifying implementation. For other authorized repair requests, the parent owns the same targeted repair-and-reaudit cycle. For audit-only requests, report the targeted missing work. Stop with `INCOMPLETE` when a blocker needs user input or unavailable access; do not replan the project or introduce team roles, approval chains, boards, or organizational fields.

## Mandatory subagent verification

The parent prepares the source and inventory, coordinates verification, and merges results; it cannot replace the independent audit with its own verdict. After extraction, let N be the number of mandatory IDs. For 1–10 IDs, spawn one independent verifier. For N > 10, split IDs in source order into disjoint batches of at most 10 and spawn one verifier per batch (at least two). Run batches concurrently where capacity permits, otherwise in waves; every batch still requires a subagent. Missing delegation is a blocker, not permission to self-certify.

Give each verifier this skill, its explicit ID assignment, the full `requirements.md`, the inventory snapshot, the current implementation location/revision (including uncommitted changes), and relevant check commands. Ask it to inspect evidence independently and return exactly one prescribed audit row per assigned ID, plus any source or cross-requirement conflict. An assigned verifier executes only its batch: it does not spawn further verifiers, run the whole-inventory gate, invoke cleanup, repair implementation, or declare overall completion.

Keep implementation and requirements unchanged while verifiers run. Use separate temporary output paths and isolate conflicting test resources or serialize those checks. Verifiers may run checks and temporary probes but leave source edits to the parent. If the audited state changes, discard affected results and reassign verification against a consistent current state. A failed or absent worker result leaves its IDs unverified; never silently drop them.

Merge rows into one table with one header, then run the full inventory comparison above. Preserve adverse findings until evidence resolves them; do not average statuses or accept majority votes. Each repair cycle delegates all mandatory IDs again so previously satisfied rows are reassessed against the final state; unchanged evidence may be reused only after its continued applicability is established. In audit-only requests, return `INCOMPLETE` and missing work without starting repairs.
