#!/usr/bin/env python3
"""Simple version bumping script for nessus-reportgen."""
import re
import sys
from pathlib import Path

INIT_FILE = Path("src/reportgen/__init__.py")
PYPROJECT_FILE = Path("pyproject.toml")
VERSION_PATTERN = re.compile(r'__version__\s*=\s*[\'"]([^\'"]+)[\'"]')
# Match poetry version field that's NOT indented (top-level)
POETRY_VERSION_PATTERN = re.compile(r'^version\s*=\s*[\'"]([^\'"]+)[\'"]', re.MULTILINE)


def get_current_version() -> str:
    """Get the current version from __init__.py, stripping any leading 'v'."""
    content = INIT_FILE.read_text()
    match = VERSION_PATTERN.search(content)
    if not match:
        print(f"Error: Could not find version in {INIT_FILE}", file=sys.stderr)
        sys.exit(1)
    version = match.group(1)
    return version.lstrip('v')


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

    return f"v{major}.{minor}.{patch}"


def write_version(new_version: str) -> None:
    """Write the new version back to __init__.py and pyproject.toml."""
    # Update __init__.py
    init_content = INIT_FILE.read_text()
    new_init_content = VERSION_PATTERN.sub(f'__version__ = "{new_version}"', init_content)
    INIT_FILE.write_text(new_init_content)

    # Update pyproject.toml - only top-level version fields
    pyproject_content = PYPROJECT_FILE.read_text()
    new_pyproject_content = POETRY_VERSION_PATTERN.sub(f'version = "{new_version}"', pyproject_content)
    PYPROJECT_FILE.write_text(new_pyproject_content)

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
