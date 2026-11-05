# pstack for Codex

An on-demand Codex port of [Lauren Tan's pstack](https://github.com/cursor/plugins/tree/main/pstack), based on upstream `0.15.36` at commit `2776ddd2355d6d6c8747d3964600f28daf62f049`. The original MIT license is preserved. This is an independent adaptation, not an official Cursor or OpenAI release.

Maintained by [Roberto Ansuini](https://github.com/robansuini). Report port-specific problems in [this repository's issues](https://github.com/robansuini/pstack-codex/issues). See [CONTRIBUTING.md](CONTRIBUTING.md) for changes and local checks.

## Use

From any project in Codex, invoke a skill and describe the task:

```text
$pstack review this branch
$poteto-mode fix the failing checkout test
$how explain the authentication flow
$architect compare designs for this change
$interrogate the current diff
$swarm verify these independent scenarios
```

Select the pstack entry when the skill picker shows a plugin namespace. `$pstack` alone shows the main workflows. `$poteto-help` explains the full catalog. All 59 skills are explicit-only, including setup and principles. They do not add always-on project rules. A selected workflow may read its sibling skills as needed.

Role models inherit the current Codex model. `$setup-pstack` optionally writes supported role choices to `${CODEX_HOME:-~/.codex}/pstack/models.json`, read only during pstack work. Independent runs of the same model are labeled accordingly.

## Install or refresh globally

Requires Python 3.9+ for the checkout scripts and a Codex CLI with `plugin marketplace add` and `plugin add`. The direct GitHub installation does not require Python. Public repositories can be cloned without GitHub authentication; if you are installing while this repository is private, authenticate an account with access.

To install directly from GitHub:

```sh
codex plugin marketplace add robansuini/pstack-codex
codex plugin add pstack@pstack-local
```

To install from a maintained checkout instead:

```sh
git clone https://github.com/robansuini/pstack-codex.git
cd pstack-codex
./scripts/install.sh
python3 scripts/verify-install.py
```

The installer registers this checkout as the user-level `pstack-local` marketplace and installs `pstack@pstack-local` into Codex's plugin cache. It does not write to your other projects. Keep this checkout for future refreshes; the installed copy runs from the cache. Re-run the installer after editing the maintained source. Skills become available on the next turn; if an existing client has a stale catalog, start a new chat or refresh the client.

For a GitHub-based install, refresh with `codex plugin marketplace upgrade pstack-local`, then `codex plugin add pstack@pstack-local`. For a checkout-based install, pull the reviewed changes with `git pull --ff-only`, then run `./scripts/install.sh`. Updates are manual; scheduled upstream synchronization is not configured.

Remove the plugin and its marketplace with:

```sh
codex plugin remove pstack@pstack-local
codex plugin marketplace remove pstack-local
```

## What changed

- Preserved all 58 upstream top-level skills, playbooks, reference prompts, principles, statechart fixtures, and helper tools. Added the `$pstack` router.
- Added native Codex marketplace/package metadata and explicit-only `agents/openai.yaml` for every discovered skill.
- Replaced Cursor agent types, model slugs, rules files, and private transcript paths with Codex delegation, optional role settings, and scoped chat tools. See [CODEX.md](plugins/pstack/CODEX.md).
- Replaced Cursor loops with current-task wait/watch guidance. No schedule, Slack integration, or remote worker is activated by installation.
- Adapted the optional [Benny recipes](plugins/pstack/automations/benny/FOR_AGENTS.md). Slack events require a separate configured event service; requested scheduled runs use Codex Automations. The recipes require their own Slack/tracker connections and app-control configuration.
- Rewrote the bot-UI workflow for a real supplied webhook and server-side credentials. There is no assumed Codex webhook routine API.
- Ported the PR watcher launcher to Node.js with a locked npm dependency install. Removed worktree audit's Cursor chat scan and its automatic “safe” classification. Preserved project identity/authorization rules and unrelated work.
- Replaced Cursor-specific help and guide pages with the Codex runtime contract and skill catalog. Preserved the original MIT attribution and source revision in [UPSTREAM.json](UPSTREAM.json).

## Helpers and validation

Package installation and skill discovery are tested with **Codex CLI 0.164.0**. Older versions are not verified. The Codex desktop app must expose compatible local plugins and skill discovery. Linux and macOS helper tests run in CI; Windows helper behavior is not verified.

The workflow instructions need no extra runtime beyond Codex tools. Optional helpers require:

| Helper | Requirements |
| --- | --- |
| PR watcher | Node 22.18+, 23.6+, or later; npm; authenticated `gh` |
| Plan checker | Node.js |
| Decision log / worktree audit | Shell, Git; audit also uses `jq`, `rg`, and optionally `gh` |
| Statechart | Supported Node/Bun/Deno; live TLA+ checks also need Java/TLC via `mise` or `JAVA` + `TLA2TOOLS` |

The PR watcher installs locked runtime dependencies on first use. No GitHub write is needed to install or verify pstack. Bun is used only to run the inherited PR-watcher/plan-checker test suite, not by the installed watcher launcher.

```sh
python3 scripts/validate.py
python3 scripts/verify-install.py
cd plugins/pstack/skills/poteto-mode/scripts
bun test watch-pr check-plan.test.ts
```

Statechart's tests run with `npm ci && npm test` from its `scripts/` directory. Live TLC tests skip when `TLA2TOOLS` is absent; replay tests exercise the parser, model results, reports, and CLI without it. The macOS symlink fixture canonicalizes the temporary directory so `/var` versus `/private/var` does not produce a broken relative link.

CI validates the package, tests the helpers, and installs into an empty Codex configuration to check discovery from an unrelated project. It does not run model turns, connect Slack, create schedules, or exercise live GitHub PR operations. See [the initial release notes](docs/releases/0.15.36-codex.1.md) for the release scope and limitations.
