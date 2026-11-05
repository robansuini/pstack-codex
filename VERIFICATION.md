# Verification

Verified locally on 2026-11-05 with Node.js 26.12.1 and Bun 1.4.4 (test runner only).

- All 59 discovered skills pass Codex skill-creator's official validator.
- `python3 scripts/validate.py` passes package metadata, explicit-only policies, marketplace resolution, and relative links.
- `python3 scripts/verify-install.py` starts the Codex app-server without a model turn and discovers all 59 enabled pstack skills from an unrelated temporary project. Each installed skill has explicit-only invocation metadata.
- All 617 installed payload files matched their maintained source by SHA-256 after installation.
- The installed Node PR watcher bootstrapped its locked commander dependency and displayed its actual CLI help.
- PR-watcher and plan-checker suite: 61 passed, 0 failed.
- Statechart full final suite: 267 passed, 0 failed, 67 skipped. Live TLC tests require TLA2TOOLS and were not run. Replay, parser, rendering, launcher, and process lifecycle tests passed.
- The macOS relative-symlink fixture initially failed because /var resolves through /private/var. A separate probe reproduced ENOENT, canonicalizing the fixture directory fixed it, both targeted launcher checks passed, and the full suite then passed.
- Shell syntax and Node bootstrap syntax checks passed.

No commits, GitHub writes, schedules, Slack posts, or project-specific setup were needed for this installation. Optional service connections and live TLC checks remain configuration for the workflows that use them.
