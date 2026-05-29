#!/usr/bin/env python3
"""Simple version bumping script for nessus-reportgen."""
import re
import sys
from pathlib import Path

INIT_FILE = Path("src/reportgen/__init__.py")
VERSION_PATTERN = re.compile(r'__version__\s*=\s*[\'"]([^\'"]+)[\'"]')


def get_current_version() -> str:
    """Get the current version from __init__.py."""
    content = INIT_FILE.read_text()
    match = VERSION_PATTERN.search(content)
    if not match:
        print(f"Error: Could not find version in {INIT_FILE}", file=sys.stderr)
        sys.exit(1)
    return match.group(1)


def bump_version(version: str, part: str) -> str:
    """Bump the specified part of the version (major, minor, patch)."""
    try:
        major, minor, patch = map(int, version.split("."))
    except ValueError:
        print(f"Error: Invalid version format: {version}", file=sys.stderr)
        sys.exit(1)

    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        print(f"Error: Invalid part: {part} (must be major, minor, or patch)", file=sys.stderr)
        sys.exit(1)

    return f"{major}.{minor}.{patch}"


def write_version(new_version: str) -> None:
    """Write the new version back to __init__.py."""
    content = INIT_FILE.read_text()
    new_content = VERSION_PATTERN.sub(f'__version__ = "{new_version}"', content)
    INIT_FILE.write_text(new_content)
    print(f"Updated version to {new_version}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python bump_version.py [major|minor|patch]", file=sys.stderr)
        sys.exit(1)

    part = sys.argv[1]
    current_version = get_current_version()
    new_version = bump_version(current_version, part)
    write_version(new_version)


if __name__ == "__main__":
    main()
