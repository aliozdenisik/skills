# Agent Skills

[![skills.sh](https://skills.sh/b/aliozdenisik/skills)](https://skills.sh/aliozdenisik/skills)

A collection of reusable AI coding agent skills for NASA-standard requirement authoring, minimal requirement-driven implementation, behavior-preserving structure cleanup, deterministic requirement verification, and session retrospectives.

## Installation

Install all skills via the [skills.sh](https://www.skills.sh/aliozdenisik/skills) CLI:

```bash
# Install into the current project
npx skills add aliozdenisik/skills

# Install globally across all projects and supported agents
npx skills add aliozdenisik/skills -g
```

Install an individual skill:

```bash
npx skills add aliozdenisik/skills --skill requirements
npx skills add aliozdenisik/skills --skill implement-requirements
npx skills add aliozdenisik/skills --skill code-structure-cleanup
npx skills add aliozdenisik/skills --skill requirement-verification
npx skills add aliozdenisik/skills --skill retro
```

## Included Skills

| Skill | Description |
| :--- | :--- |
| [`requirements`](./requirements/SKILL.md) | Write verifiable requirements in `requirements.md` using NASA's *Appendix C: How to Write a Good Requirement* checklist, assigning stable `<!-- requirement: REQ-xxx -->` markers. |
| [`implement-requirements`](./implement-requirements/SKILL.md) | Implement requirements from `requirements.md` with the smallest correct change, reusing existing/native capabilities first, then automatically chaining into cleanup and verification. |
| [`code-structure-cleanup`](./code-structure-cleanup/SKILL.md) | Refactor working feature code to remove duplicated runtime mechanics, API calls, parsing, validation, or business logic while preserving behavior and public contracts. |
| [`requirement-verification`](./requirement-verification/SKILL.md) | Audit every mandatory requirement against implemented code and objective test/runtime evidence, gating completion on exact ID coverage via [`scripts/coverage_gate.py`](./requirement-verification/scripts/coverage_gate.py). |
| [`retro`](./retro/SKILL.md) | Review an agent session and produce evidence-backed recommendations to improve agent instructions, guardrails, and workspace configuration. |

## Requirement-Driven Workflow

1. **Author (`requirements`)** — Define mandatory (`shall`/`must`) requirements with stable `REQ-xxx` markers in `requirements.md`.
2. **Implement (`implement-requirements`)** — Deliver the minimal change satisfying `requirements.md`.
3. **Clean Up (`code-structure-cleanup`)** — Extract concrete duplicated mechanics without altering behavior.
4. **Verify (`requirement-verification`)** — Run deterministic ID extraction (`coverage_gate.py extract`) and verify every mandatory requirement (`coverage_gate.py check`) before completion.
