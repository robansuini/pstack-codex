#!/usr/bin/env python3
"""Regression tests for the sync boundary, real three-way merges and PR publication."""
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


sync = module("sync", "sync-upstream.py")
publisher = module("publisher", "publish-upstream-pr.py")


class MergeTests(unittest.TestCase):
    def test_independent_edits_preserve_codex(self):
        base = b"one\ntwo\nthree\nfour\nfive\n"
        ours = base.replace(b"one", b"Codex")
        theirs = base.replace(b"five", b"new upstream")
        self.assertEqual(sync.merge_bytes(base, ours, theirs), b"Codex\ntwo\nthree\nfour\nnew upstream\n")

    def test_overlap_rejected(self):
        with self.assertRaises(ValueError):
            sync.merge_bytes(b"old\n", b"Codex\n", b"Cursor\n")

    def test_additions_deletions_and_binaries(self):
        self.assertEqual(sync.merge_bytes(None, None, b"new"), b"new")
        self.assertIsNone(sync.merge_bytes(b"old", b"old", None))
        self.assertEqual(sync.merge_bytes(b"\0old", b"\0old", b"\0new"), b"\0new")
        for values in [(None, b"ours", b"theirs"), (b"old", b"adapted", None),
                       (b"\0old", b"\0ours", b"\0theirs")]:
            with self.assertRaises(ValueError):
                sync.merge_bytes(*values)


class PreparationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "port"
        self.source = Path(self.temp.name) / "source"
        self.source.mkdir()
        self.plugin = self.root / "plugins/pstack"
        self.plugin.mkdir(parents=True)
        (self.root / "scripts").mkdir()
        (self.root / "scripts/validate.py").write_text("# Fixture validator\n")
        (self.root / "docs").mkdir()
        sync.git(self.source, "init", "-q")
        self.write("plugin.json", json.dumps({"name": "pstack", "version": "0.15.36"}))
        self.write("helper.txt", "one\ntwo\nthree\nfour\nfive\n")
        self.base = self.commit()
        self.pin = {"repository": sync.UPSTREAM.removesuffix(".git"), "path": "pstack", "commit": self.base, "version": "0.15.36"}
        (self.root / "UPSTREAM.json").write_text(json.dumps(self.pin))
        (self.root / "README.md").write_text(f"based on upstream `0.15.36` at commit `{self.base}`")
        (self.plugin / "plugin.json").write_text(json.dumps({"name": "pstack", "version": "0.15.36-codex.1", "author": {"name": "Roberto Ansuini"}}))
        (self.plugin / "helper.txt").write_text("Codex\ntwo\nthree\nfour\nfive\n")

    def write(self, name, data):
        path = self.source / "pstack" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data)

    def commit(self):
        env = dict(os.environ, GIT_AUTHOR_NAME=publisher.NAME, GIT_AUTHOR_EMAIL=publisher.EMAIL,
                   GIT_COMMITTER_NAME=publisher.NAME, GIT_COMMITTER_EMAIL=publisher.EMAIL)
        for variable in ("GIT_AUTHOR_IDENT", "GIT_COMMITTER_IDENT"):
            identity = subprocess.check_output(["git", "var", variable], cwd=self.source, env=env, text=True)
            self.assertTrue(identity.startswith(f"{publisher.NAME} <{publisher.EMAIL}> "))
        sync.git(self.source, "add", "--all")
        subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false", "commit", "-qm", "fixture"],
                       cwd=self.source, env=env, check=True)
        return sync.revision(self.source, "HEAD")

    def prepare(self):
        return sync.prepare(self.root, self.source, "HEAD")

    def test_unchanged_subtree_ignores_other_plugins(self):
        (self.source / "unrelated.txt").write_text("another plugin changed")
        self.commit()
        self.assertFalse(self.prepare()["changed"])
        self.assertFalse((self.root / "docs/upstream-sync.md").exists())

    def test_clean_sync_bumps_codex_revision_and_pin(self):
        self.write("helper.txt", "one\ntwo\nthree\nfour\nupstream\n")
        target = self.commit()
        result = self.prepare()
        self.assertEqual(result["conflicts"], [])
        self.assertEqual((self.plugin / "helper.txt").read_text(), "Codex\ntwo\nthree\nfour\nupstream\n")
        self.assertEqual(json.loads((self.root / "UPSTREAM.json").read_text())["commit"], target)
        manifest = json.loads((self.plugin / "plugin.json").read_text())
        self.assertEqual(manifest["version"], "0.15.36-codex.2")
        self.assertEqual(manifest["author"]["name"], "Roberto Ansuini")
        self.assertIn(target, (self.root / "README.md").read_text())

    def test_new_upstream_version(self):
        self.write("plugin.json", json.dumps({"name": "pstack", "version": "0.15.37"}))
        self.commit()
        self.assertEqual(self.prepare()["port_version"], "0.15.37-codex.1")

    def test_conflict_keeps_port_and_pin(self):
        self.write("helper.txt", "Cursor\ntwo\nthree\nfour\nfive\n")
        self.commit()
        result = self.prepare()
        self.assertTrue(result["conflicts"])
        self.assertTrue((self.plugin / "helper.txt").read_text().startswith("Codex\n"))
        self.assertEqual(json.loads((self.root / "UPSTREAM.json").read_text()), self.pin)

    def test_upstream_symlink_does_not_write_outside_plugin(self):
        (self.source / "pstack/escape").symlink_to("../../outside")
        self.commit()
        result = self.prepare()
        self.assertTrue(result["conflicts"])
        self.assertFalse((self.plugin / "escape").exists())

    def test_local_symlink_parent_is_not_followed(self):
        outside = self.root / "outside"
        outside.mkdir()
        (self.plugin / "linked").symlink_to(outside, target_is_directory=True)
        self.write("linked/file.txt", "unsafe")
        self.commit()
        self.assertTrue(self.prepare()["conflicts"])
        self.assertFalse((outside / "file.txt").exists())

    def test_new_skill_needs_manual_codex_adaptation(self):
        self.write("skills/new/SKILL.md", "---\nname: new\n---\nCursor instructions")
        self.commit()
        self.assertTrue(self.prepare()["conflicts"])
        self.assertEqual(json.loads((self.root / "UPSTREAM.json").read_text()), self.pin)

    def test_port_owned_files_and_manifest_changes_are_retained(self):
        self.write("README.md", "Cursor installation instructions")
        self.write("plugin.json", json.dumps({"name": "renamed", "version": "0.15.37"}))
        self.commit()
        result = self.prepare()
        self.assertEqual(len(result["conflicts"]), 2)
        self.assertFalse((self.plugin / "README.md").exists())
        self.assertEqual(json.loads((self.plugin / "plugin.json").read_text())["name"], "pstack")

    def test_failed_validation_keeps_pin(self):
        (self.root / "scripts/validate.py").write_text("raise SystemExit(1)\n")
        self.write("new.txt", "new")
        self.commit()
        self.assertTrue(self.prepare()["conflicts"])
        self.assertEqual(json.loads((self.root / "UPSTREAM.json").read_text()), self.pin)


class PublishingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / ".tools/upstream-sync").mkdir(parents=True)
        self.state = {"changed": True, "target": "a" * 40, "tree": "b" * 40,
                      "branch": publisher.PREFIX + "b" * 12, "version": "0.15.37"}
        (self.root / ".tools/upstream-sync/state.json").write_text(json.dumps(self.state))
        self.addCleanup(patch.stopall)
        patch.object(publisher, "ROOT", self.root).start()

    def test_wrong_login_refuses_writes(self):
        with patch.dict(os.environ, {"GH_TOKEN": "fixture"}), patch.object(publisher, "run") as run:
            run.return_value.stdout = "axos-ai\n"
            with self.assertRaises(SystemExit):
                publisher.authenticate()
            self.assertEqual(run.call_count, 2)

    def test_missing_credential_refuses_writes(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(publisher, "run") as run:
            with self.assertRaises(SystemExit):
                publisher.authenticate()
            run.assert_not_called()

    def test_open_pr_is_not_overwritten(self):
        with patch.object(publisher, "authenticate"), patch.object(publisher, "run") as run:
            run.return_value.stdout = json.dumps([{"headRefName": publisher.PREFIX + "c" * 12, "url": "https://example.test/pr/1"}])
            publisher.publish()
            self.assertEqual(run.call_count, 1)

    def test_no_upstream_change_does_not_create_pr(self):
        (self.root / ".tools/upstream-sync/state.json").write_text('{"changed": false}')
        with patch.object(publisher, "authenticate"), patch.object(publisher, "run") as run:
            publisher.publish()
            run.assert_not_called()

    def test_new_candidate_uses_human_identity_and_never_force_pushes(self):
        calls = []

        def fake_run(*args, env=None, check=True):
            calls.append(args)
            output = ""
            if args[:3] == ("gh", "pr", "list"):
                output = "[]"
            elif args[:3] == ("git", "diff", "HEAD"):
                output = "UPSTREAM.json\0"
            elif args[:2] == ("git", "var"):
                self.assertEqual(env["GIT_AUTHOR_EMAIL"], publisher.EMAIL)
                self.assertEqual(env["GIT_COMMITTER_EMAIL"], publisher.EMAIL)
                output = f"{publisher.NAME} <{publisher.EMAIL}> 1234567890 +0000"
            elif args[:3] == ("gh", "pr", "create"):
                output = "https://example.test/pr/1"
            return subprocess.CompletedProcess(args, 0, output)

        with patch.object(publisher, "authenticate") as auth, patch.object(publisher, "run", side_effect=fake_run):
            publisher.publish()
            self.assertEqual(auth.call_count, 3)
        self.assertTrue(any("commit" in call for call in calls))
        self.assertTrue(any("push" in call for call in calls))
        self.assertFalse(any(any(arg.startswith("--force") for arg in call) for call in calls))

    def test_closed_pr_is_not_reopened(self):
        with patch.object(publisher, "authenticate"), patch.object(publisher, "run") as run:
            run.side_effect = [subprocess.CompletedProcess([], 0, "[]"), subprocess.CompletedProcess([], 0, '[{"url":"https://example.test/pr/1"}]')]
            publisher.publish()
            self.assertEqual(run.call_count, 2)

    def test_push_without_pr_recovers_without_new_commit(self):
        with patch.object(publisher, "authenticate"), patch.object(publisher, "run") as run:
            run.side_effect = [subprocess.CompletedProcess([], 0, value) for value in ("[]", "[]", "existing-ref", "https://example.test/pr/1")]
            publisher.publish()
            self.assertEqual(run.call_count, 4)
            self.assertEqual(run.call_args.args[:3], ("gh", "pr", "create"))
            self.assertIn("--draft", run.call_args.args)

    def test_unexpected_workflow_change_refuses_commit(self):
        with patch.object(publisher, "authenticate"), patch.object(publisher, "run") as run:
            run.side_effect = [subprocess.CompletedProcess([], 0, value) for value in ("[]", "[]", "", ".github/workflows/ci.yml\0", "")]
            with self.assertRaises(SystemExit):
                publisher.publish()
            self.assertEqual(run.call_count, 5)


if __name__ == "__main__":
    unittest.main()
