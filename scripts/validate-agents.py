#!/usr/bin/env python3
"""Validate agent.md files for required frontmatter, schema, and consistency."""

import os
import re
import sys
from pathlib import Path

REQUIRED_FIELDS = ["description", "mode", "phase", "depends_on", "inputs", "outputs", "tools", "error_handling", "cost_per_run", "sla"]
REQUIRED_SECTIONS = ["## Role", "## Workflow", "## Constraints"]
AGENT_DIR = Path(__file__).resolve().parent


def extract_frontmatter_keys(content: str) -> set:
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return set()
    keys = set()
    for line in match.group(1).splitlines():
        if ":" in line:
            key = line.split(":", 1)[0].strip()
            if key:
                keys.add(key)
    return keys


def validate_agent(path: Path) -> list[str]:
    errors = []
    content = path.read_text()
    keys = extract_frontmatter_keys(content)

    for field in REQUIRED_FIELDS:
        if field not in keys:
            errors.append(f"Missing frontmatter field: {field}")

    mode = next((line.split(":", 1)[1].strip() for line in content.splitlines() if line.startswith("mode:")), None)
    if mode not in ("all", "chat", "command", "edit"):
        errors.append(f"Invalid mode: {mode}")

    phase_line = next((line for line in content.splitlines() if line.startswith("phase:")), None)
    if phase_line:
        try:
            phase = int(phase_line.split(":", 1)[1].strip())
            if phase < 0 or phase > 5:
                errors.append(f"Phase out of range: {phase}")
        except ValueError:
            errors.append(f"Phase is not an integer: {phase_line}")
    else:
        errors.append("Missing frontmatter field: phase")

    for section in REQUIRED_SECTIONS:
        if section not in content:
            errors.append(f"Missing section: {section}")

    return errors


def main():
    agent_files = sorted(list(AGENT_DIR.parent.glob("*/agent.md")) + list(Path("archive").glob("*/agent.md")))
    if not agent_files:
        print("No agent.md files found.")
        sys.exit(1)

    all_errors = []
    for path in agent_files:
        errors = validate_agent(path)
        if errors:
            all_errors.append((path, errors))

    if all_errors:
        print("VALIDATION FAILED")
        for path, errors in all_errors:
            print(f"\n{path}")
            for e in errors:
                print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"OK: {len(agent_files)} agent.md files validated.")


if __name__ == "__main__":
    main()
