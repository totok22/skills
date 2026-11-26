#!/usr/bin/env python3
"""Validate skill structure, links, Chinese mirrors, skills.sh.json, scripts, and public boundary.

Python 3.9+, standard library only (no third-party dependencies required).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
TRANSLATIONS_DIR = ROOT / "translations" / "zh-CN"
SKILLS_SH_CONFIG = ROOT / "skills.sh.json"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"(?<!!)\[[^]]*]\(([^)]+)\)")
FRONTMATTER_PATTERN = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_simple_yaml_mapping(block: str) -> dict[str, str]:
    """Parse flat key: value YAML frontmatter without third-party dependencies."""
    result: dict[str, str] = {}
    current_key: str | None = None
    for raw_line in block.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line[0] in (" ", "\t") and current_key is not None:
            result[current_key] = (result[current_key] + " " + raw_line.strip()).strip()
            continue
        if ":" not in raw_line:
            fail(f"invalid frontmatter line: {raw_line!r}")
        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        result[key] = value
        current_key = key
    return result


def validate_links(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for target in LINK_PATTERN.findall(text):
        clean = unquote(target.split("#", 1)[0].strip())
        if not clean or "://" in clean or clean.startswith("mailto:"):
            continue
        if not (path.parent / clean).resolve().exists():
            fail(f"{path.relative_to(ROOT)} contains a missing link: {target}")


def validate_openai_yaml(agent_file: Path, expected_name: str) -> None:
    text = agent_file.read_text(encoding="utf-8")
    if "interface:" not in text:
        fail(f"{agent_file.relative_to(ROOT)} is missing interface block")
    for required_key in ("display_name:", "short_description:", "default_prompt:"):
        if required_key not in text:
            fail(f"{agent_file.relative_to(ROOT)} is missing {required_key}")
    if f"${expected_name}" not in text:
        fail(f"{agent_file.relative_to(ROOT)} default_prompt must mention ${expected_name}")


def validate_skill(skill_dir: Path, *, announce: bool = True) -> None:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        fail(f"{skill_dir.relative_to(ROOT)} is missing SKILL.md")

    text = skill_file.read_text(encoding="utf-8")
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        fail(f"{skill_file.relative_to(ROOT)} has invalid frontmatter boundaries")

    metadata = parse_simple_yaml_mapping(match.group(1))
    if set(metadata) != {"name", "description"}:
        fail(f"{skill_file.relative_to(ROOT)} frontmatter must contain only name and description")
    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if not NAME_PATTERN.fullmatch(name):
        fail(f"{skill_file.relative_to(ROOT)} has an invalid skill name: {name!r}")
    if name != skill_dir.name:
        fail(f"skill folder {skill_dir.name} does not match name {name}")
    if not description.strip():
        fail(f"{skill_file.relative_to(ROOT)} has an empty description")
    if len(text.splitlines()) > 500:
        fail(f"{skill_file.relative_to(ROOT)} exceeds 500 lines; move details to references")

    validate_links(skill_file)
    references_dir = skill_dir / "references"
    if references_dir.is_dir():
        for reference in sorted(references_dir.glob("*.md")):
            validate_links(reference)

    agent_file = skill_dir / "agents" / "openai.yaml"
    if agent_file.is_file():
        validate_openai_yaml(agent_file, name)

    for json_file in sorted(skill_dir.rglob("*.json")):
        try:
            json.loads(json_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"invalid JSON in {json_file.relative_to(ROOT)}: {exc}")

    for py_file in sorted(skill_dir.rglob("*.py")):
        try:
            compile(py_file.read_text(encoding="utf-8"), str(py_file), "exec")
        except SyntaxError as exc:
            fail(f"Python syntax error in {py_file.relative_to(ROOT)}: {exc}")

    if announce:
        print(f"OK: {name}")


def validate_translations(skill_dirs: list[Path]) -> None:
    if not TRANSLATIONS_DIR.is_dir():
        fail("translations/zh-CN directory is missing")
    for skill_dir in skill_dirs:
        mirror_dir = TRANSLATIONS_DIR / skill_dir.name
        if not mirror_dir.is_dir():
            fail(f"missing Chinese mirror for {skill_dir.name}")
        source_files = {
            path.relative_to(skill_dir)
            for path in skill_dir.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts and path.name != ".DS_Store"
        }
        mirror_files = {
            path.relative_to(mirror_dir)
            for path in mirror_dir.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts and path.name != ".DS_Store"
        }
        missing = sorted(item.as_posix() for item in source_files - mirror_files)
        extra = sorted(item.as_posix() for item in mirror_files - source_files)
        if missing or extra:
            details = []
            if missing:
                details.append("missing: " + ", ".join(missing))
            if extra:
                details.append("extra: " + ", ".join(extra))
            fail(f"Chinese mirror of {skill_dir.name} does not match its file set ({'; '.join(details)})")
        validate_skill(mirror_dir, announce=False)
    print("OK: translations")


def validate_skills_sh(skill_names: set[str]) -> None:
    if not SKILLS_SH_CONFIG.is_file():
        return
    try:
        config = json.loads(SKILLS_SH_CONFIG.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        fail(f"skills.sh.json is invalid JSON: {error}")

    groupings = config.get("groupings") if isinstance(config, dict) else None
    if not isinstance(groupings, list) or not groupings:
        fail("skills.sh.json must contain at least one grouping")
    for index, grouping in enumerate(groupings, start=1):
        if not isinstance(grouping, dict):
            fail(f"skills.sh.json grouping {index} must be an object")
        title = grouping.get("title")
        names = grouping.get("skills")
        if not isinstance(title, str) or not title.strip():
            fail(f"skills.sh.json grouping {index} has an empty title")
        if not isinstance(names, list) or not names:
            fail(f"skills.sh.json grouping {index} has no skills")
        unknown = sorted(name for name in names if name not in skill_names)
        if unknown:
            fail(
                f"skills.sh.json grouping {index} references unknown skills: "
                + ", ".join(unknown)
            )
    print("OK: skills.sh.json")


def validate_public_boundary() -> None:
    forbidden_suffixes = {".key", ".pem", ".p12", ".pfx"}
    private_key_marker = "-----BEGIN " + "PRIVATE KEY-----"
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if path.name == ".env" or path.suffix.lower() in forbidden_suffixes:
            fail(f"credential file is not allowed: {path.relative_to(ROOT)}")
        if path.suffix.lower() not in {".json", ".md", ".py", ".yaml", ".yml"}:
            continue
        if private_key_marker in path.read_text(encoding="utf-8"):
            fail(f"private key content found in {path.relative_to(ROOT)}")
    print("OK: public boundary")


def main() -> None:
    if not SKILLS_DIR.is_dir():
        fail("skills directory is missing")
    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    if not skill_dirs:
        fail("no skills found")
    for skill_dir in skill_dirs:
        validate_skill(skill_dir)
    validate_translations(skill_dirs)
    validate_skills_sh({path.name for path in skill_dirs})
    for path in sorted(ROOT.glob("*.md")):
        validate_links(path)
    validate_public_boundary()
    print(f"Validated {len(skill_dirs)} skill(s)")


if __name__ == "__main__":
    main()
