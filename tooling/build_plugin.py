from __future__ import annotations

import shutil
from pathlib import Path


RUNTIME_PATHS = (".claude-plugin", "skills", "README.md", "LICENSE")


def build_marketplace(root: Path, output_dir: Path) -> Path:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for relative_path in RUNTIME_PATHS:
        source_path = root / relative_path
        destination_path = output_dir / relative_path

        if source_path.is_dir():
            shutil.copytree(source_path, destination_path)
        else:
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, destination_path)

    return output_dir
