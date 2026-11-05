---
name: setup-pstack
description: Configure optional Codex model choices for pstack roles, or restore parent-model inheritance, without changing other projects or global agent behavior.
---

# Configure pstack

Read [the Codex runtime contract](../../CODEX.md) once. No setup is needed to use pstack: every role inherits the current Codex model by default.

1. Read `${CODEX_HOME:-~/.codex}/pstack/models.json` if it exists. Do not create or modify a global AGENTS.md or config.toml for role selection.
2. Inspect the currently available subagent tool schema for supported models and reasoning options. Never guess a model slug or use a rejected value. If model overrides are unavailable, keep inheritance and explain the limitation.
3. Apply the user's requested role choices. Ask a concise preference question only if the request lacks the needed choice. Do not require a model-selection interview when the user merely wants pstack installed.
4. Store the requested roles as JSON in the user-level file above. Preserve unrelated roles. `inherit-parent` and `auto` mean omit both model and reasoning overrides. A concrete model is an object with `model` and optionally `reasoning_effort`. Panel roles are lists whose length is the number of seats. Example:

```json
{
  "version": 1,
  "roles": {
    "feature, refactoring": "inherit-parent",
    "judgment and prose": "inherit-parent",
    "arena runners": ["inherit-parent", "inherit-parent"],
    "architect runners": ["inherit-parent", "inherit-parent"],
    "interrogate reviewers": ["inherit-parent", "inherit-parent"],
    "swarm workers": "inherit-parent"
  }
}
```

Other supported roles are `bug-fix`, `perf-issue`, `hillclimb`, `hardest tasks`, `how explorer`, `how explainer`, `why investigators`, `why synthesizer`, `reflect tooling`, `reflect judgment, divergent, synthesizer`, and `arena cross-judge pool`. A missing role inherits the parent; a missing panel uses two independent parent-model runs. An explicit one-seat panel stays one seat.

5. Parse the written JSON and verify each concrete model and reasoning value against the observed tool schema. Report the path and changed roles. Settings apply when a pstack workflow next reads the file. Same-model runs provide independent contexts, not model diversity.

Only create project verification skills if the user requests them. Use [create-verification-skill](../create-verification-skill/SKILL.md) or [create-formal-verification-skill](../create-formal-verification-skill/SKILL.md) for that work.
