# Upstream sync review

- Upstream version: `0.15.42`
- Previous source: `2776ddd2355d6d6c8747d3964600f28daf62f049`
- Proposed source: `bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7`
- Source tree: `ca1f48a4c8565485745aab0e6ce6145b176c4bf8`
- [Upstream comparison](https://github.com/cursor/plugins/compare/2776ddd2355d6d6c8747d3964600f28daf62f049...bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7) (filter to `pstack/`)

This candidate was prepared without running upstream code. Review all instruction changes and CI before merging.

## Manual work

The upstream pin and package version have not advanced. Resolve these items, then update `UPSTREAM.json`, the package version and README provenance before marking the PR ready.
- `".cursor-plugin/plugin.json"`: Port-owned file retained; review upstream changes manually
- `"README.md"`: Port-owned file retained; review upstream changes manually
- `"agents/comment-sicko.md"`: Port-owned file retained; review upstream changes manually
- `"automations/benny/FOR_AGENTS.md"`: Overlapping changes; Codex file retained without conflict markers
- `"automations/benny/skills/setup-benny/SKILL.md"`: Overlapping changes; Codex file retained without conflict markers
- `"docs/guide/01-setup.md"`: File was omitted from the port; review before importing
- `"docs/guide/02-poteto-mode.md"`: File was omitted from the port; review before importing
- `"docs/guide/03-understand.md"`: File was omitted from the port; review before importing
- `"docs/guide/04-design.md"`: File was omitted from the port; review before importing
- `"docs/guide/10-recipes-and-pitfalls.md"`: File was omitted from the port; review before importing
- `"docs/harness/claude-code.md"`: File was omitted from the port; review before importing
- `"skills/architect/SKILL.md"`: Overlapping changes; Codex file retained without conflict markers
- `"skills/arena/SKILL.md"`: Overlapping changes; Codex file retained without conflict markers
- `"skills/how/SKILL.md"`: Overlapping changes; Codex file retained without conflict markers
- `"skills/no-comments/SKILL.md"`: Overlapping changes; Codex file retained without conflict markers
- `"skills/poteto-help/SKILL.md"`: Overlapping changes; Codex file retained without conflict markers
- `"skills/poteto-mode/SKILL.md"`: Overlapping changes; Codex file retained without conflict markers
- `"skills/poteto-mode/playbooks/bug-fix.md"`: Overlapping changes; Codex file retained without conflict markers
- `"skills/poteto-mode/playbooks/feature.md"`: Overlapping changes; Codex file retained without conflict markers
- `"skills/poteto-mode/playbooks/hillclimb.md"`: Overlapping changes; Codex file retained without conflict markers
- `"skills/poteto-mode/playbooks/multi-phase-plan.md"`: Overlapping changes; Codex file retained without conflict markers
- `"skills/poteto-mode/playbooks/perf-issue.md"`: Overlapping changes; Codex file retained without conflict markers
- `"skills/poteto-mode/playbooks/refactoring.md"`: Overlapping changes; Codex file retained without conflict markers
- `"skills/reflect/SKILL.md"`: Overlapping changes; Codex file retained without conflict markers
- `"skills/setup-pstack/SKILL.md"`: Overlapping changes; Codex file retained without conflict markers
- `"skills/swarm/SKILL.md"`: Overlapping changes; Codex file retained without conflict markers
- `"skills/why/SKILL.md"`: Overlapping changes; Codex file retained without conflict markers

## Applied file changes

- `"automations/benny/skills/reproduce-and-fix-issues/SKILL.md"`
- `"automations/benny/skills/triage-issue-reports/SKILL.md"`
- `"skills/blast-radius/SKILL.md"`
- `"skills/how/references/explainer-prompt.md"`
- `"skills/how/references/explorer-prompt.md"`
- `"skills/poteto-mode/playbooks/investigation.md"`
- `"skills/recall/SKILL.md"`
- `"skills/reflect/references/synthesizer.md"`
- `"skills/sharpen/SKILL.md"`
- `"skills/statechart/scripts/backends/mermaid.ts"`
- `"skills/statechart/scripts/run.ts"`
- `"skills/statechart/scripts/test/chart.test.ts"`
- `"skills/statechart/scripts/test/cli.test.ts"`
- `"skills/statechart/scripts/test/corpus.test.ts"`
- `"skills/statechart/scripts/test/corpus/Login/chart.mmd"`
- `"skills/statechart/scripts/test/drawn.ts"`
- `"skills/statechart/scripts/test/labels.ts"`
- `"skills/statechart/scripts/test/render.test.ts"`
- `"skills/teach/SKILL.md"`
- `"skills/why/references/epistemics.md"`
- `"skills/why/references/investigator-prompt.md"`
- `"skills/why/references/source-playbook.md"`
- `"skills/why/references/sources/code-archaeology.md"`
- `"skills/why/references/sources/databricks.md"`
- `"skills/why/references/sources/datadog.md"`
- `"skills/why/references/sources/incident-postmortem.md"`
- `"skills/why/references/sources/linear.md"`
- `"skills/why/references/sources/notion.md"`
- `"skills/why/references/sources/sentry.md"`
- `"skills/why/references/sources/slack.md"`
- `"skills/why/references/synthesizer-prompt.md"`

Upstream manifest version is handled by the Codex version bump.

After review: pass all required checks, mark the draft ready, merge, and publish a new release when appropriate. Installation updates remain manual.
