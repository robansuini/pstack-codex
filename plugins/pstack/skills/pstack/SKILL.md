---
name: pstack
description: Use pstack on demand to choose an engineering workflow, investigate code, compare designs, implement changes, review, or verify a project.
---

# pstack for Codex

Read [the Codex runtime contract](../../CODEX.md) once, then select the narrowest workflow matching the request. Read its complete SKILL.md before applying it. A bare `$pstack` invocation shows the main choices below without changing the project. With a concrete request, route and do the work.

| Request | Skill |
| --- | --- |
| Full deliberate engineering workflow | [poteto-mode](../poteto-mode/SKILL.md) |
| Understand implementation or historical decisions | [how](../how/SKILL.md), [why](../why/SKILL.md) |
| Compare designs or candidate implementations | [architect](../architect/SKILL.md), [arena](../arena/SKILL.md) |
| Adversarial review with reproduced findings | [interrogate](../interrogate/SKILL.md) |
| Parallel coverage or independent verification | [swarm](../swarm/SKILL.md) |
| Test-driven implementation | [tdd](../tdd/SKILL.md) |
| Assess affected callers and risks | [blast-radius](../blast-radius/SKILL.md) |
| Create a reusable project verification harness | [create-verification-skill](../create-verification-skill/SKILL.md) |
| Formal checks and state-machine diagrams | [create-formal-verification-skill](../create-formal-verification-skill/SKILL.md), [statechart](../statechart/SKILL.md) |
| Recover prior work or summarize current progress | [recall](../recall/SKILL.md), [ketchup](../ketchup/SKILL.md) |
| Configure optional role models | [setup-pstack](../setup-pstack/SKILL.md) |
| Configure optional issue triage and reproduction | [Benny recipe](../../automations/benny/FOR_AGENTS.md) |
| Full skill catalog and recipes | [poteto-help](../poteto-help/SKILL.md) |

Examples: `$pstack review this branch`, `$pstack explain the authentication flow`, `$poteto-mode fix the failing checkout test`, `$interrogate the current diff`.
