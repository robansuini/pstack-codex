# Contributing

This repository maintains the Codex adaptation of Lauren Tan's pstack. Keep the upstream MIT notice, attribution, and pinned provenance in `UPSTREAM.json` intact.

Report a reproducible problem with the Codex version, operating system, skill or helper involved, expected behavior, and observed result. Remove credentials and private project data from logs and examples.

Work on a branch and open a focused pull request. Changes to skill instructions should explain the intended behavior, any change in autonomy or tool access, and how the behavior was checked. Keep skills on demand and preserve the user's project instructions and identity rules.

Run the package check from the repository root:

```sh
python3 scripts/validate.py
```

Run the watcher and plan-checker checks with Node.js and Bun 1.4.4:

```sh
cd plugins/pstack/skills/poteto-mode/scripts
npm ci --ignore-scripts
bun test watch-pr check-plan.test.ts
npm run typecheck
```

Run statechart checks from `plugins/pstack/skills/statechart/scripts`:

```sh
npm ci --ignore-scripts
npm test
```

Live TLC tests skip unless `TLA2TOOLS` points to the model checker and Java is available. Report those skips; replay tests alone do not establish a live TLC result.

To check installation without changing your normal Codex configuration, run the following from the repository root with Codex CLI 0.164.0:

```sh
pstack_test_home=$(mktemp -d)
CODEX_HOME="$pstack_test_home" ./scripts/install.sh
CODEX_HOME="$pstack_test_home" python3 scripts/verify-install.py
```

Delete the temporary directory when finished. This check starts the app-server for skill discovery; it does not run a model turn or require an OpenAI API key.

The maintainer reviews and merges releases. Automatic upstream synchronization is not yet configured. For an upstream update, inspect the changed workflows, preserve Codex adaptations, refresh provenance, and account for new or removed skills before changing the expected package inventory.
