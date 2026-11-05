#!/usr/bin/env python3
"""Ask Codex's skill loader to discover pstack from an unrelated project."""
import json
import os
import selectors
import subprocess
import tempfile
import time
from pathlib import Path

root = Path(__file__).resolve().parents[1]
expected = {p.parent.name for p in (root / "plugins/pstack/skills").glob("*/SKILL.md")}
with tempfile.TemporaryDirectory(prefix="pstack-discovery-") as project, tempfile.TemporaryFile() as errors:
    process = subprocess.Popen(
        ["codex", "app-server", "--stdio"], cwd=project,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=errors,
    )
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)
    pending = b""

    def send(message):
        process.stdin.write((json.dumps(message) + "\n").encode())
        process.stdin.flush()

    def response(request_id):
        global pending
        deadline = time.monotonic() + 45
        while time.monotonic() < deadline:
            while b"\n" in pending:
                line, pending = pending.split(b"\n", 1)
                message = json.loads(line)
                if message.get("id") == request_id:
                    if "error" in message:
                        raise RuntimeError(message["error"])
                    return message["result"]
            if selector.select(timeout=min(1, max(0, deadline - time.monotonic()))):
                chunk = os.read(process.stdout.fileno(), 1024 * 1024)
                if not chunk:
                    raise RuntimeError("Codex app-server exited before skill discovery completed")
                pending += chunk
        raise TimeoutError("Codex skill discovery timed out")

    try:
        send({"id": 1, "method": "initialize", "params": {
            "clientInfo": {"name": "pstack-install-check", "version": "1.0.0"},
            "capabilities": {"experimentalApi": True},
        }})
        response(1)
        send({"method": "initialized", "params": {}})
        send({"id": 2, "method": "skills/list", "params": {"cwds": [project], "forceReload": True}})
        result = response(2)
        entries = result["data"]
        skills = [s for entry in entries for s in entry["skills"]
                  if "/pstack/" in s["path"] and "/plugins/cache/" in s["path"]]
        found = {s["name"].removeprefix("pstack:") for s in skills}
        assert found == expected, f"Missing: {expected - found}; unexpected: {found - expected}"
        assert all(s["enabled"] for s in skills), "Some pstack skills are disabled"
        plugin_errors = [e for entry in entries for e in entry.get("errors", []) if "/pstack/" in e["path"]]
        assert not plugin_errors, plugin_errors
        for skill in skills:
            path = Path(skill["path"])
            assert "allow_implicit_invocation: false" in (path.parent / "agents/openai.yaml").read_text()
        print(f"Codex discovered all {len(skills)} installed pstack skills from an unrelated project.")
        print("Every entry is enabled and has explicit-only invocation metadata.")
        print("Installed root: " + str(Path(skills[0]["path"]).parents[2]))
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        selector.close()
