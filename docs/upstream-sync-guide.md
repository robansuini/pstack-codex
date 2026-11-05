# Keeping the Codex port synchronized

The [Upstream sync workflow](../.github/workflows/upstream-sync.yml) checks `cursor/plugins` daily at **07:23 UTC**, and can be started from GitHub Actions using **Run workflow** on `main`. Scheduled runs may be delayed by GitHub. GitHub can disable scheduled workflows in public repositories after 60 days without repository activity; re-enable the workflow if that happens.

## Authentication

The repository Actions secret **`PSTACK_SYNC_TOKEN`** must contain a fine-grained personal access token owned by **`robansuini`**, restricted to **`robansuini/pstack-codex`**, with these repository permissions:

- Contents: Read and write.
- Pull requests: Read and write.
- Metadata: Read-only (included automatically).

Create and rotate the token in GitHub settings and enter it directly in the repository's Actions secrets. Never paste it into chat, issues, commits or logs. Replace the secret before the token expires. No workflow-editing or administration permission is needed. The local GitHub CLI credential is not copied into Actions.

The workflow verifies the authenticated login before every GitHub write. Commits use `Roberto Ansuini <1525892+robansuini@users.noreply.github.com>` for both author and committer, without identity trailers. A missing, expired or wrong-account credential fails the workflow. Using a personal token makes the PR belong to `robansuini` and permits normal PR CI to run.

## What happens on an update

1. Fetch the pinned upstream commit from `UPSTREAM.json` and upstream `main`. Compare the Git tree for `pstack/`, ignoring unrelated plugin updates and detecting changes even without a version bump.
2. Apply a three-way file merge using the previous upstream file, our Codex file and the new upstream file. No upstream scripts or helper tests run in the preparation job. The publishing token is available only to the identity check and PR publisher steps.
3. Preserve port-owned metadata and Codex runtime instructions. Overlapping edits, deleted adapted files, symlinks, changed skill inventory and package-validation failures become manual review items in `docs/upstream-sync.md`. Conflicting files retain the Codex version; unresolved conflict markers are never written. Independently mergeable changes are included in the draft.
4. If mechanical checks pass, update `UPSTREAM.json`, README provenance and the package version. A new upstream version starts at `<upstream>-codex.1`; a change within the same upstream version increments the Codex revision. If manual items remain, keep the previous pin and version until the reviewer resolves them.
5. Push a new `codex/upstream-sync-<tree>` branch and open a **draft PR**. Existing open sync PRs are never overwritten. The same upstream tree is not reopened after its PR is closed. Reopen the original PR if you want to resume it; a later upstream tree can produce a new candidate after the open PR is resolved. If a push succeeds but PR creation fails, rerunning can open the PR from that branch without rewriting it.

## Reviewing and releasing

Read the generated report and upstream diff. A clean text merge does not establish Codex compatibility: review instructions, tools, permissions, model choices and runtime assumptions. New or removed skills require explicit attention to `agents/openai.yaml`, the Codex runtime contract, help/catalog references, and inventory checks in `scripts/validate.py`.

If the report lists conflicts, resolve them and update the provenance and package version to the report's proposed source before merging. Keep the original MIT attribution. All four required CI jobs must pass, review conversations must be resolved, and the draft must be marked ready. Reviewer approval is not required for this solo-maintainer repository.

The automation does not merge PRs, create tags, publish releases, or refresh installed plugins. Prepare release notes and assets before publishing an immutable release, then refresh installations using the README commands.

## Local checks

```sh
python3 scripts/test-upstream-sync.py
python3 scripts/validate.py
```

`python3 scripts/sync-upstream.py` prepares a candidate in the current checkout and writes ignored metadata under `.tools/upstream-sync/`. Use a clean disposable checkout to preview updates. The publisher is intended for the trusted `main` workflow and requires `GH_TOKEN`; it never falls back to another account or the built-in Actions token.
