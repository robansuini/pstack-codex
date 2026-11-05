#!/usr/bin/env python3
"""Validate the portable package and its on-demand Codex entry points."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/pstack"
manifest = json.loads((PLUGIN / "plugin.json").read_text())
marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
assert manifest["name"] == marketplace["plugins"][0]["name"] == "pstack"
assert (ROOT / marketplace["plugins"][0]["source"]["path"]).resolve() == PLUGIN
assert (PLUGIN / "LICENSE").read_text() == (ROOT / "LICENSE").read_text()
skills = sorted((PLUGIN / "skills").glob("*/SKILL.md"))
assert len(skills) == 59, f"Expected 58 upstream skills plus router, found {len(skills)}"
for skill in skills:
    text = skill.read_text()
    assert text.startswith("---\n"), skill
    front = text.split("---", 2)[1]
    assert re.search(rf"^name: {re.escape(skill.parent.name)}$", front, re.M), skill
    assert re.search(r"^description: \S", front, re.M), skill
    assert not re.search(r"^(paths|icon|color|disable-model-invocation):", front, re.M), skill
    policy = (skill.parent / "agents/openai.yaml").read_text()
    assert "  allow_implicit_invocation: false\n" in policy, skill
    assert f"${skill.parent.name}" in policy, skill
    assert "../../CODEX.md" in text, skill

for file in PLUGIN.rglob("*.md"):
    if "node_modules" in file.parts:
        continue
    for link in re.findall(r"\]\(([^)]+)\)", file.read_text()):
        target = link.split("#", 1)[0]
        if not target or "://" in target or target.startswith(("/", "mailto:")) or target == "url":
            continue
        assert (file.parent / target).exists(), f"Broken link in {file.relative_to(ROOT)}: {target}"
print(f"Package valid: {len(skills)} explicit-only skills; relative links and marketplace resolve.")
