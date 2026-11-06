"""Check the portable skills and plugin paths using only the standard library."""
from __future__ import annotations

import json
import re
from pathlib import Path


def validate(root: Path) -> list[str]:
    errors = []
    expected = {"sec-open-api", "sec-fund-search", "sec-onboarding"}
    for name in sorted(expected):
        path = root / "skills" / name / "SKILL.md"
        if not path.is_file():
            errors.append(f"Missing {path.relative_to(root)}")
            continue
        text = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
        if not match:
            errors.append(f"Missing frontmatter: {name}")
            continue
        fields = dict(re.findall(r"^([a-z-]+): (.+)$", match[1], re.MULTILINE))
        if fields.get("name") != name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            errors.append(f"Invalid skill name: {name}")
        if not fields.get("description"):
            errors.append(f"Missing description: {name}")
        for reference in re.findall(r"`([^`\n]+\.md)`", text):
            if "<" not in reference and not (path.parent / reference).is_file():
                errors.append(f"Broken reference in {name}: {reference}")

    claude = json.loads((root / ".claude-plugin/plugin.json").read_text())
    codex = json.loads((root / ".codex-plugin/plugin.json").read_text())
    version = re.search(r'^version = "([^"]+)"', (root / "pyproject.toml").read_text(), re.MULTILINE).group(1)
    if f'__version__ = "{version}"' not in (root / "secopendata/__init__.py").read_text():
        errors.append("Python package version differs from pyproject.toml")
    for host, manifest in (("Claude", claude), ("Codex", codex)):
        if manifest.get("version") != version:
            errors.append(f"{host} plugin version differs from package")
        paths = manifest["skills"]
        paths = [paths] if isinstance(paths, str) else paths
        discovered = set()
        for relative in paths:
            folder = root / relative
            if not folder.is_dir():
                errors.append(f"Missing {host} skills path: {relative}")
            if (folder / "SKILL.md").is_file():
                discovered.add(folder.name)
            else:
                discovered.update(p.parent.name for p in folder.glob("*/SKILL.md"))
        if discovered != expected:
            errors.append(f"{host} skill discovery differs: {sorted(discovered)}")

    for manifest in (".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json"):
        marketplace = json.loads((root / manifest).read_text())
        for plugin in marketplace["plugins"]:
            if "version" in plugin and plugin["version"] != version:
                errors.append(f"Marketplace version differs: {manifest}")
            source = plugin["source"]
            relative = source if isinstance(source, str) else source["path"]
            if not (root / relative).is_dir():
                errors.append(f"Missing marketplace source: {manifest}: {relative}")

    command = root / "commands/onBording.md"
    if not command.is_file() or "skills/sec-onboarding/SKILL.md" not in command.read_text():
        errors.append("Missing onBording command or onboarding target")
    if not (root / "secopendata/data/fund_catalog.json.gz").is_file():
        errors.append("Missing bundled offline catalog")
    return errors


if __name__ == "__main__":
    problems = validate(Path(__file__).resolve().parents[1])
    for problem in problems:
        print(problem)
    if not problems:
        print("Validated 3 skills, plugin/marketplace paths, references, and onBording command.")
    raise SystemExit(bool(problems))
