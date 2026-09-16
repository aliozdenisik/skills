---
name: code-structure-cleanup
description: Clean up the structure of a working feature when its implementation contains duplicated mechanics, repeated API calls, parsing, validation, or business logic. Use after behavior works and before review; keep the refactor scoped and behavior-preserving.
license: MIT
metadata:
  short-description: Refactor working feature code without behavior changes
---

# Code Structure Cleanup

Run this pass after the feature works. Reduce duplication and make the feature easier for future agents to extend without redesigning unrelated parts of the application.

## Cleanup Pass

1. Inspect the feature's changed files and their immediate collaborators. Identify concrete duplication in runtime mechanics, API calls, parsing, validation, or business logic.
2. Separate policy from mechanics. Routes, actions, and components decide what should happen; shared modules handle reusable mechanics such as sending email, streaming a response, creating a sandbox, validating a webhook, normalizing data, or calling an external API.
3. Choose the smallest extraction that removes meaningful duplication. Reuse an existing suitable abstraction when one exists; add a focused service or helper only when it makes callers simpler.
4. Implement the extraction without changing user-facing behavior, public contracts, or domain policy. Keep naming churn and unrelated edits out of the diff.
5. Run the relevant tests, type checks, and linters available for the affected area. Review the diff for accidental behavior changes.
6. Summarize what duplication was removed, where the shared mechanism now lives, and which checks passed or could not run.

## Completion Criteria

- Repeated mechanics in the feature area are reduced rather than merely reformatted or moved.
- Domain decisions remain visible in the calling route, action, or component.
- Callers are simpler and use one consistent implementation of the shared mechanism.
- Observable behavior and public contracts remain unchanged.
- The diff stays focused on the completed feature and the relevant verification passes.

If no meaningful duplication or structural problem is present, report that result instead of manufacturing an abstraction.
