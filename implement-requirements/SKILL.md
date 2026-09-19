---
name: implement-requirements
description: Implement given requirements with the smallest correct change, reusing existing and native capabilities before adding mechanisms. Use for requirement-driven implementation followed automatically by structure cleanup and delegated requirement verification.
---

# Implement Requirements

- Use `requirements.md` as the authoritative scope and preserve its acceptance criteria and existing contracts. Resolve material ambiguity instead of inventing behavior; keep changes within the requested requirements.
- Inspect the codebase, standard library, installed dependencies, and native SDK/backend capabilities first. Verify the actual version's semantics against the requirement, including relevant edge cases; prefer an existing solution when it fits.
- Add custom code, a dependency, abstraction, or wrapper only for a concrete unmet requirement or necessary correctness invariant. Keep custom code limited to the missing behavior; weigh dependency cost against maintenance saved. Avoid forwarding-only wrappers and architecture for hypothetical future needs.
- Make the smallest correct change in the existing structure. Keep each shared rule in one authoritative place without merging distinct contracts; remove superseded code within the change's scope unless compatibility requires it. Avoid unrelated cleanup and feature expansion.
- For mechanisms the change actually touches, preserve explicit resource ownership and cleanup, consistency across concurrent decisions, and distinguishable error outcomes. Use existing boundaries; introduce separation only where it reduces concrete complexity.
- Run relevant existing checks and required project checks; add focused behavioral verification where evidence is missing, proportional to risk. Fix failures caused by the change. Report results and blocked checks briefly; do not claim completion while relevant verification is unrun or failing. Then automatically run `code-structure-cleanup`, which hands off to `requirement-verification`; wait for its delegated audit before ending the task.

## Completion loop

Own the loop in this task: implement → `code-structure-cleanup` → `requirement-verification`. Read and follow each skill when entering its stage; continue without a new user prompt. After an unsuccessful audit, fix only reported gaps within authorized scope, run relevant checks, then repeat cleanup and delegated verification against the updated code. Reconcile every mandatory ID on every cycle, including previously satisfied requirements. Do not recursively invoke this skill or create scheduled tasks for retries.

Finish only when the verification gate passes. If missing access, an unresolved requirement, unavailable delegation, or repeated identical findings prevent progress, stop with `INCOMPLETE`, the evidence, and the specific blocker; do not spin indefinitely or substitute self-verification.
