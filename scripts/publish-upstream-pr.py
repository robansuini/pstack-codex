#!/usr/bin/env python3
"""Publish a prepared candidate with a narrowly scoped robansuini credential."""
import argparse
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "robansuini/pstack-codex"
LOGIN = "robansuini"
NAME = "Roberto Ansuini"
EMAIL = "1525892+robansuini@users.noreply.github.com"
PREFIX = "codex/upstream-sync-"


def run(*args, env=None, check=True):
    return subprocess.run(args, cwd=ROOT, env=env, capture_output=True, text=True, check=check)


def authenticate():
    if not os.environ.get("GH_TOKEN"):
        raise SystemExit("Add the PSTACK_SYNC_TOKEN Actions secret: a robansuini fine-grained token for this repository with Contents and Pull requests read/write. Never put the token in logs or chat.")
    run("gh", "auth", "status", "--active", "--hostname", "github.com")
    login = run("gh", "api", "user", "--jq", ".login").stdout.strip()
    if login != LOGIN:
        raise SystemExit("Sync credential must belong to robansuini; refusing GitHub writes.")
    repository = json.loads(run("gh", "api", f"repos/{REPOSITORY}").stdout)
    if repository["full_name"] != REPOSITORY or repository["default_branch"] != "main":
        raise SystemExit("Unexpected repository or default branch; refusing GitHub writes.")
    return login


def publish():
    authenticate()
    state = json.loads((ROOT / ".tools/upstream-sync/state.json").read_text())
    if not state["changed"]:
        print("No upstream changes; no PR needed.")
        return
    target, tree, branch = state["target"], state["tree"], state["branch"]
    if not all(re.fullmatch(r"[0-9a-f]{40}", value) for value in (target, tree)) or branch != PREFIX + tree[:12]:
        raise SystemExit("Invalid candidate metadata")
    if not re.fullmatch(r"\d+\.\d+\.\d+", state["version"]):
        raise SystemExit("Invalid upstream version")
    opened = json.loads(run("gh", "pr", "list", "--repo", REPOSITORY, "--state", "open", "--limit", "1000", "--json", "headRefName,url").stdout)
    pending = [pr for pr in opened if pr["headRefName"].startswith(PREFIX)]
    if pending:
        print("Existing sync PR retained without modifying its branch: " + pending[0]["url"])
        return
    previous = json.loads(run("gh", "pr", "list", "--repo", REPOSITORY, "--head", branch, "--state", "all", "--json", "url").stdout)
    if previous:
        print("This upstream tree already has a PR; not reopening it: " + previous[0]["url"])
        return

    # A failed PR creation can leave a pushed branch. Reuse it without a force push.
    remote = run("git", "ls-remote", "origin", f"refs/heads/{branch}").stdout.strip()
    if not remote:
        changed = set(run("git", "diff", "HEAD", "--name-only", "-z").stdout.split("\0"))
        changed.update(run("git", "ls-files", "--others", "--exclude-standard", "-z").stdout.split("\0"))
        changed.discard("")
        allowed = {"UPSTREAM.json", "README.md", "docs/upstream-sync.md"}
        if not changed or any(name not in allowed and not name.startswith("plugins/pstack/") for name in changed):
            raise SystemExit("Candidate has unexpected changes; refusing to publish")
        env = dict(os.environ, GIT_AUTHOR_NAME=NAME, GIT_AUTHOR_EMAIL=EMAIL, GIT_COMMITTER_NAME=NAME, GIT_COMMITTER_EMAIL=EMAIL)
        for variable in ("GIT_AUTHOR_IDENT", "GIT_COMMITTER_IDENT"):
            identity = run("git", "var", variable, env=env).stdout.strip()
            if not re.fullmatch(re.escape(f"{NAME} <{EMAIL}>") + r" \d+ [+-]\d{4}", identity):
                raise SystemExit("Unexpected commit identity; refusing to commit")
        run("git", "switch", "-c", branch)
        run("git", "add", "--all", "--", "plugins/pstack", "UPSTREAM.json", "README.md", "docs/upstream-sync.md")
        run("git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false", "commit", "-m",
            f"chore: prepare pstack {state['version']} upstream sync", env=env)
        authenticate()
        run("git", "-c", "credential.helper=", "-c", "credential.helper=!gh auth git-credential",
            "push", f"https://github.com/{REPOSITORY}.git", f"HEAD:refs/heads/{branch}")

    body = ROOT / ".tools/upstream-sync/pr-body.md"
    body.write_text(
        f"Prepare upstream pstack **{state['version']}** for Codex.\n\n"
        f"Proposed source: `cursor/plugins@{target}`.\n\n"
        f"See [the review report](https://github.com/{REPOSITORY}/blob/{branch}/docs/upstream-sync.md) "
        "for applied changes and manual work. Conflicting files retain the Codex version; "
        "the upstream pin advances only when mechanical checks pass.\n\n"
        "Review instruction changes and Codex compatibility, resolve the report's manual items, "
        "and pass all required CI before marking this draft ready and merging. "
        "This automation does not merge PRs, publish releases, or update installed plugins.\n"
    )
    authenticate()
    result = run("gh", "pr", "create", "--repo", REPOSITORY, "--base", "main", "--head", branch,
                 "--draft", "--title", f"chore: sync upstream pstack {state['version']} ({tree[:8]})",
                 "--body-file", str(body))
    print(result.stdout.strip())
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as stream:
            stream.write("Draft upstream sync PR: " + result.stdout.strip() + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-auth", action="store_true")
    args = parser.parse_args()
    if args.check_auth:
        print("Verified unattended GitHub identity: " + authenticate())
    else:
        publish()


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        # Do not dump subprocess environments or credential-bearing diagnostics.
        raise SystemExit(f"{error.cmd[0]} failed (exit {error.returncode}); check the token's access and repository rules.") from None
