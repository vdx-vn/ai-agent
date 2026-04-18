from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from tooling.validate_plugin import validate_plugin


def run_verify(root: Path) -> int:
    errors = validate_plugin(root)
    for error in errors:
        print(error)

    try:
        result = subprocess.run(
            ["claude", "plugin", "validate", str(root)],
            check=False,
        )
        claude_exit = result.returncode
    except FileNotFoundError:
        claude_exit = 0

    if errors:
        return 1
    return claude_exit


def verify_main() -> int:
    root = Path(__file__).resolve().parents[1]
    return run_verify(root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="odoo-skills-verify")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("verify")

    args = parser.parse_args(argv)
    if args.command == "verify":
        return verify_main()

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
