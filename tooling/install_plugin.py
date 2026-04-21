#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tooling.build_plugin import build_marketplace

PLUGIN_NAME = "odoo-skills"
MARKETPLACE_NAME = "odoo-skills-dev"
INSTALL_SCOPE = "local"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install local odoo-skills plugin bundle")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall local plugin and remove marketplace")
    return parser.parse_args(argv)


def ensure_claude_cli(*, required: bool = True) -> bool:
    if shutil.which("claude"):
        return True
    if required:
        raise SystemExit("Claude CLI is required. Install `claude` and try again.")
    return False


def run_command(repo_root: Path, command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=repo_root, check=True, capture_output=True, text=True)


def _error_text(exc: BaseException) -> str:
    stderr = getattr(exc, "stderr", None)
    stdout = getattr(exc, "stdout", None)
    parts = [part.decode(errors="replace") if isinstance(part, bytes) else str(part) for part in (stderr, stdout) if part]
    parts.append(str(exc))
    return "\n".join(parts).lower()


def add_marketplace(repo_root: Path, marketplace_path: Path) -> None:
    add_command = ["claude", "plugin", "marketplace", "add", str(marketplace_path)]
    try:
        run_command(repo_root, add_command)
    except subprocess.CalledProcessError as exc:
        if "exist" not in _error_text(exc):
            raise
        run_command(repo_root, ["claude", "plugin", "marketplace", "remove", MARKETPLACE_NAME])
        run_command(repo_root, add_command)


def _best_effort_run_command(repo_root: Path, command: list[str]) -> None:
    try:
        run_command(repo_root, command)
    except Exception:
        pass


def run_install(repo_root: Path, args: argparse.Namespace) -> int:
    del args
    ensure_claude_cli()
    marketplace_path = repo_root / "dist" / "marketplace"
    marketplace_added = False
    plugin_installed = False

    try:
        built_marketplace = build_marketplace(repo_root, marketplace_path)
        run_command(repo_root, ["claude", "plugin", "validate", str(built_marketplace)])
        add_marketplace(repo_root, built_marketplace)
        marketplace_added = True
        run_command(repo_root, ["claude", "plugin", "install", f"{PLUGIN_NAME}@{MARKETPLACE_NAME}", "--scope", INSTALL_SCOPE])
        plugin_installed = True
    except Exception:
        if plugin_installed:
            _best_effort_run_command(repo_root, ["claude", "plugin", "uninstall", PLUGIN_NAME, "--scope", INSTALL_SCOPE])
        if marketplace_added:
            _best_effort_run_command(repo_root, ["claude", "plugin", "marketplace", "remove", MARKETPLACE_NAME])
        if marketplace_path.exists():
            shutil.rmtree(marketplace_path)
        raise

    print(f"Installed {PLUGIN_NAME} from local marketplace bundle at {marketplace_path}")
    print("Next: install CLI entrypoints with `python3 -m pip install -e .` if needed.")
    print("Then run `odoo-skills project-setup` inside each Odoo project.")
    print("Fallback: `python3 -m tooling.cli project-setup`.")
    return 0


def run_uninstall(repo_root: Path, args: argparse.Namespace) -> int:
    del args
    if ensure_claude_cli(required=False):
        _best_effort_run_command(repo_root, ["claude", "plugin", "uninstall", PLUGIN_NAME, "--scope", INSTALL_SCOPE])
        _best_effort_run_command(repo_root, ["claude", "plugin", "marketplace", "remove", MARKETPLACE_NAME])
    marketplace_path = repo_root / "dist" / "marketplace"
    if marketplace_path.exists():
        shutil.rmtree(marketplace_path)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(__file__).resolve().parents[1]
    if args.uninstall:
        return run_uninstall(repo_root, args)
    return run_install(repo_root, args)


if __name__ == "__main__":
    raise SystemExit(main())
