---
name: implement-requirements
description: Implement given requirements with the smallest correct change, reusing existing and native capabilities before adding mechanisms. Use for requirement-driven implementation; authoring requirements and final coverage audits are separate tasks.
---

# Implement Requirements

- Use `requirements.md` as the authoritative scope and preserve its acceptance criteria and existing contracts. Resolve material ambiguity instead of inventing behavior; keep changes within the requested requirements.
- Inspect the codebase, standard library, installed dependencies, and native SDK/backend capabilities first. Verify the actual version's semantics against the requirement, including relevant edge cases; prefer an existing solution when it fits.
- Add custom code, a dependency, abstraction, or wrapper only for a concrete unmet requirement or necessary correctness invariant. Keep custom code limited to the missing behavior; weigh dependency cost against maintenance saved. Avoid forwarding-only wrappers and architecture for hypothetical future needs.
- Make the smallest correct change in the existing structure. Keep each shared rule in one authoritative place without merging distinct contracts; remove superseded code within the change's scope unless compatibility requires it. Avoid unrelated cleanup and feature expansion.
- For mechanisms the change actually touches, preserve explicit resource ownership and cleanup, consistency across concurrent decisions, and distinguishable error outcomes. Use existing boundaries; introduce separation only where it reduces concrete complexity.
- Run relevant existing checks and required project checks; add focused behavioral verification where evidence is missing, proportional to risk. Fix failures caused by the change. Report results and blocked checks briefly; do not claim completion while relevant verification is unrun or failing. Apply `requirement-verification` for the final requirement-coverage gate.
