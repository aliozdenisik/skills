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

## Acceptance Criteria

- **AC-1:** The cleaned feature shall preserve its public APIs, returned data, persisted data, external side effects, and business rules.
- **AC-2:** Each duplicated mechanism selected for cleanup shall have one canonical implementation used by every affected caller.
- **AC-3:** Each feature-specific business decision shall remain in its calling route, action, or component.
- **AC-4:** Every existing test, type check, and linter that covers a modified file shall pass.
- **AC-5:** The completion report shall list each unexecuted check with its reason.
- **AC-6:** The final diff shall contain only edits required to remove the identified duplication and verify the result.
- **AC-7:** The cleanup pass shall leave code unchanged when analysis finds no qualifying duplication.
- **AC-8:** The completion report shall state when analysis finds no qualifying duplication.

## Requirement implementation handoff

When this pass is entered from `implement-requirements`, automatically read and run `requirement-verification` after cleanup and its checks, including when no qualifying duplication exists. Return its audit to the implementation coordinator: unresolved gaps resume targeted implementation, then cleanup and verification repeat. Cleanup success alone does not complete the implementation task. Standalone cleanup requests retain their original scope.
