#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tooling.install_plugin import run_install as run_install_plugin
from tooling.install_plugin import run_uninstall as run_uninstall_plugin

DEPRECATION_MESSAGE = (
    "Deprecated: `tooling.setup_local` now only installs or uninstalls plugin bundle. "
    "Use `python3 -m tooling.install_plugin` for plugin install and `odoo-skills project-setup` inside each Odoo project."
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Deprecated local setup shim. Installs local odoo-skills plugin bundle; "
            "Odoo project paths now belong in `odoo-skills project-setup`."
        )
    )
    parser.add_argument("--docs-root", help="Deprecated compatibility option")
    parser.add_argument("--source-root", help="Deprecated compatibility option")
    parser.add_argument("--version", help="Deprecated compatibility option")
    parser.add_argument("--python-bin", default="python3", help="Deprecated compatibility option")
    parser.add_argument("--odoo-bin", help="Deprecated compatibility option")
    parser.add_argument("--config", help="Deprecated compatibility option")
    parser.add_argument("--base-cmd", help="Deprecated compatibility option")
    parser.add_argument("--yes", action="store_true", help="Deprecated compatibility option")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall local plugin and remove marketplace")
    return parser.parse_args(argv)


def run_setup(repo_root: Path, args: argparse.Namespace) -> int:
    print(DEPRECATION_MESSAGE)
    print("Next after install: run `odoo-skills project-setup` inside each Odoo project.")
    print("Fallback: `python3 -m tooling.cli project-setup`.")
    return run_install_plugin(repo_root, args)


def run_uninstall(repo_root: Path, args: argparse.Namespace) -> int:
    print(DEPRECATION_MESSAGE)
    return run_uninstall_plugin(repo_root, args)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(__file__).resolve().parents[1]
    if args.uninstall:
        return run_uninstall(repo_root, args)
    return run_setup(repo_root, args)


if __name__ == "__main__":
    raise SystemExit(main())
