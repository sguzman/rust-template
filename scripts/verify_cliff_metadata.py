#!/usr/bin/env python3
import re
import sys
from pathlib import Path
from typing import Optional, Tuple


def parse_metadata(path: Path) -> Tuple[Optional[str], Optional[str]]:
    owner = None
    repo = None
    in_metadata = False
    pattern = re.compile(r'^([A-Za-z0-9_]+)\s*=\s*"(.*)"$')

    for line in path.read_text().splitlines():
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("[") and stripped.endswith("]"):
            in_metadata = stripped == "[metadata]"
            continue

        if not in_metadata:
            continue

        sanitized = stripped.split("#", 1)[0].strip()
        if not sanitized:
            continue

        match = pattern.match(sanitized)
        if not match:
            continue

        key, value = match.group(1), match.group(2)
        if key == "owner":
            owner = value.strip()
        elif key == "repo":
            repo = value.strip()

    return owner, repo


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: verify_cliff_metadata.py <path-to-cliff.toml>", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"cliff config not found at {path}", file=sys.stderr)
        sys.exit(1)

    owner, repo = parse_metadata(path)

    if not owner:
        print('cliff metadata key "owner" must be set and non-empty', file=sys.stderr)
        sys.exit(1)

    if not repo:
        print('cliff metadata key "repo" must be set and non-empty', file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
