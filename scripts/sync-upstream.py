#!/usr/bin/env python3
"""Prepare a conservative, reviewable upstream update without executing upstream code."""
import argparse
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path, PurePosixPath

UPSTREAM = "https://github.com/cursor/plugins.git"
ROOT = Path(__file__).resolve().parents[1]
REGULAR = {"100644", "100755"}


def git(repo, *args, check=True):
    return subprocess.run(["git", "-C", str(repo), *args], check=check, capture_output=True)


def revision(repo, ref):
    return git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}").stdout.decode().strip()


def tree_id(repo, commit):
    return git(repo, "rev-parse", f"{commit}:pstack").stdout.decode().strip()


def entries(repo, commit):
    result = {}
    for row in git(repo, "ls-tree", "-rz", commit, "--", "pstack/").stdout.split(b"\0"):
        if not row:
            continue
        metadata, raw_path = row.split(b"\t", 1)
        mode, kind, oid = metadata.decode().split()
        path = raw_path.decode("utf-8").removeprefix("pstack/")
        parts = PurePosixPath(path).parts
        if not parts or path.startswith("/") or any(p in {"..", ".git"} for p in parts):
            raise ValueError("Unsafe upstream path")
        result[path] = (mode, kind, oid)
    return result


def blob(repo, entry):
    if entry is None:
        return None
    if entry[0] not in REGULAR or entry[1] != "blob":
        raise ValueError("Upstream symlinks and submodules require manual review")
    size = int(git(repo, "cat-file", "-s", entry[2]).stdout)
    if size > 4 * 1024 * 1024:
        raise ValueError("File exceeds the automatic merge size limit")
    return git(repo, "cat-file", "blob", entry[2]).stdout


def merge_bytes(base, ours, theirs):
    """Return merged bytes, or raise for a conflict; None means deletion."""
    if ours == base:
        return theirs
    if ours == theirs or base == theirs:
        return ours
    if base is None or ours is None or theirs is None:
        raise ValueError("Conflicting addition or deletion")
    for data in (base, ours, theirs):
        if b"\0" in data:
            raise ValueError("Conflicting binary change")
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError("Non-UTF-8 merge requires manual review") from error
    with tempfile.TemporaryDirectory(prefix="pstack-merge-") as directory:
        paths = [Path(directory) / name for name in ("ours", "base", "theirs")]
        for path, data in zip(paths, (ours, base, theirs)):
            path.write_bytes(data)
        result = subprocess.run(["git", "merge-file", "-p", *map(str, paths)], capture_output=True)
        if result.returncode:
            raise ValueError("Overlapping changes; Codex file retained without conflict markers")
        return result.stdout


def local_file(plugin, name):
    path = plugin / name
    # Never follow upstream or local symlinks, including parent directories.
    for candidate in [path, *path.parents]:
        if candidate == plugin.parent:
            break
        if candidate.is_symlink():
            raise ValueError("Symlink path requires manual review")
    if path.exists() and not path.is_file():
        raise ValueError("File/directory collision requires manual review")
    return path, path.read_bytes() if path.exists() else None


def protected(name):
    return (name in {"plugin.json", "README.md", "CODEX.md", ".gitignore"}
            or name.startswith((".cursor-plugin/", "agents/", ".github/", ".git/"))
            or name.endswith("/agents/openai.yaml"))


def prepare(root, upstream, target):
    pin = json.loads((root / "UPSTREAM.json").read_text())
    if pin["repository"] != UPSTREAM.removesuffix(".git") or pin["path"] != "pstack":
        raise ValueError("Unexpected upstream repository or path")
    base = pin["commit"]
    if not re.fullmatch(r"[0-9a-f]{40}", base):
        raise ValueError("Upstream pin must be a full commit SHA")
    target = revision(upstream, target)
    old_tree, new_tree = tree_id(upstream, base), tree_id(upstream, target)
    state = {"changed": old_tree != new_tree, "base": base, "target": target, "tree": new_tree}
    if not state["changed"]:
        return state

    before, after = entries(upstream, base), entries(upstream, target)
    version = json.loads(blob(upstream, after["plugin.json"]))["version"]
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("Upstream version needs manual interpretation")
    state.update(version=version, branch=f"codex/upstream-sync-{new_tree[:12]}")
    plugin = root / "plugins/pstack"
    conflicts, applied, notices = [], [], []
    paths = sorted(name for name in before.keys() | after.keys() if before.get(name) != after.get(name))
    for name in paths:
        old, new = before.get(name), after.get(name)
        try:
            if protected(name):
                if name == "plugin.json":
                    previous = json.loads(blob(upstream, old))
                    current = json.loads(blob(upstream, new))
                    previous.pop("version", None)
                    current.pop("version", None)
                    if previous != current:
                        raise ValueError("Upstream manifest fields changed; Codex manifest retained")
                    notices.append("Upstream manifest version is handled by the Codex version bump.")
                    continue
                raise ValueError("Port-owned file retained; review upstream changes manually")
            path, ours = local_file(plugin, name)
            old_data, new_data = blob(upstream, old), blob(upstream, new)
            # Do not resurrect files deliberately omitted from the original port.
            if old is not None and ours is None and new is not None:
                raise ValueError("File was omitted from the port; review before importing")
            merged = merge_bytes(old_data, ours, new_data)
            old_mode = old[0] if old else None
            new_mode = new[0] if new else None
            ours_mode = ("100755" if path.stat().st_mode & 0o111 else "100644") if ours is not None else None
            if ours_mode not in (old_mode, new_mode) and old_mode != new_mode:
                raise ValueError("Conflicting file permissions")
            mode = new_mode if ours_mode == old_mode else ours_mode
            if merged is None:
                if path.exists():
                    path.unlink()
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(merged)
                path.chmod(0o755 if mode == "100755" else 0o644)
            applied.append(name)
            if re.fullmatch(r"skills/[^/]+/SKILL\.md", name) and (old is None or new is None):
                conflicts.append((name, "Skill inventory changed; adapt Codex metadata, catalog and validators"))
        except (ValueError, OSError) as error:
            conflicts.append((name, str(error)))

    # Validate data with our trusted validator; never run imported helper code here.
    validation = subprocess.run(["python3", str(root / "scripts/validate.py")], cwd=root, capture_output=True)
    if validation.returncode:
        conflicts.append(("Package validation", "Run python3 scripts/validate.py and resolve its failures"))
    if not conflicts:
        manifest_path = plugin / "plugin.json"
        manifest = json.loads(manifest_path.read_text())
        old_port_version = manifest["version"]
        if version == pin["version"]:
            match = re.fullmatch(re.escape(version) + r"-codex\.(\d+)", old_port_version)
            if not match:
                raise ValueError("Cannot determine the next Codex revision")
            port_version = f"{version}-codex.{int(match[1]) + 1}"
        else:
            port_version = f"{version}-codex.1"
        readme = root / "README.md"
        updated_readme, replacements = re.subn(
            r"based on upstream \*\*\d+\.\d+\.\d+\*\*",
            f"based on upstream **{version}**", readme.read_text())
        if replacements != 1:
            raise ValueError("Expected exactly one README upstream version; refusing to advance provenance")
        manifest["version"] = port_version
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        pin.update(commit=target, version=version)
        (root / "UPSTREAM.json").write_text(json.dumps(pin, indent=2) + "\n")
        readme.write_text(updated_readme)
        state["port_version"] = port_version

    state.update(conflicts=conflicts, applied=applied)
    report = ["# Upstream sync review", "",
              f"- Upstream version: `{version}`",
              f"- Previous source: `{base}`",
              f"- Proposed source: `{target}`",
              f"- Source tree: `{new_tree}`",
              f"- [Upstream comparison](https://github.com/cursor/plugins/compare/{base}...{target}) (filter to `pstack/`)", "",
              "This candidate was prepared without running upstream code. Review all instruction changes and CI before merging.", "",
              "## Manual work", ""]
    if conflicts:
        report.append("The upstream pin and package version have not advanced. Resolve these items, then update `UPSTREAM.json`, the package version and README provenance before marking the PR ready.")
        report.extend(f"- `{json.dumps(name, ensure_ascii=True)}`: {reason}" for name, reason in conflicts)
    else:
        report.append("No mechanical conflicts were found. The upstream pin and package version were updated. Semantic review of the Codex adaptations is still required.")
    report.extend(["", "## Applied file changes", ""])
    report.extend(f"- `{json.dumps(name, ensure_ascii=True)}`" for name in applied)
    report.extend(["", *notices, "", "After review: pass all required checks, mark the draft ready, merge, and publish a new release when appropriate. Installation updates remain manual.", ""])
    (root / "docs/upstream-sync.md").write_text("\n".join(report))
    return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream-repo", type=Path, help="Use a local Git repository (for testing)")
    parser.add_argument("--target", default="FETCH_HEAD")
    args = parser.parse_args()
    output = ROOT / ".tools/upstream-sync"
    output.mkdir(parents=True, exist_ok=True)
    # Clear stale metadata before any operation that can fail.
    (output / "state.json").unlink(missing_ok=True)
    if args.upstream_repo:
        state = prepare(ROOT, args.upstream_repo.resolve(), args.target)
    else:
        pin = json.loads((ROOT / "UPSTREAM.json").read_text())["commit"]
        if not re.fullmatch(r"[0-9a-f]{40}", pin):
            raise ValueError("Upstream pin must be a full commit SHA")
        with tempfile.TemporaryDirectory(prefix="pstack-upstream-") as directory:
            upstream = Path(directory)
            git(upstream, "init", "--bare")
            git(upstream, "fetch", "--depth=1", "--no-tags", UPSTREAM, pin)
            git(upstream, "fetch", "--depth=1", "--no-tags", UPSTREAM, "refs/heads/main")
            state = prepare(ROOT, upstream, "FETCH_HEAD")
    (output / "state.json").write_text(json.dumps(state, indent=2) + "\n")
    print("Upstream candidate prepared; review required." if state["changed"] else "Already synchronized: upstream pstack tree is unchanged.")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as stream:
            stream.write("Upstream pstack: " + ("candidate prepared" if state["changed"] else "no changes") + ".\n")


if __name__ == "__main__":
    main()
