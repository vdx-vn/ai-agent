#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NotebookLM Project Manager

Manages project-to-notebook mappings for the notebooklm-project skill.
Stores mappings in ~/.claude/notebooklm-projects.json
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any


MAPPINGS_FILE = Path.home() / ".claude" / "notebooklm-projects.json"


def get_mappings() -> Dict[str, Any]:
    """Load all project-notebook mappings."""
    if not MAPPINGS_FILE.exists():
        return {}
    try:
        with open(MAPPINGS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_mappings(mappings: Dict[str, Any]) -> None:
    """Save project-notebook mappings."""
    MAPPINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MAPPINGS_FILE, 'w') as f:
        json.dump(mappings, f, indent=2)


def get_project_notebook(project_dir: str) -> Optional[str]:
    """
    Get the notebook ID for a project directory.

    Args:
        project_dir: Absolute path to the project directory

    Returns:
        Notebook ID (UUID) if mapping exists, None otherwise
    """
    mappings = get_mappings()
    normalized_path = os.path.normpath(project_dir)
    return mappings.get(normalized_path, {}).get("notebook_id")


def set_project_notebook(project_dir: str, notebook_id: str, project_name: str = None) -> None:
    """
    Store a project-to-notebook mapping.

    Args:
        project_dir: Absolute path to the project directory
        notebook_id: NotebookLM notebook UUID
        project_name: Optional project name (defaults to directory basename)
    """
    mappings = get_mappings()
    normalized_path = os.path.normpath(project_dir)

    if project_name is None:
        project_name = os.path.basename(normalized_path)

    mappings[normalized_path] = {
        "notebook_id": notebook_id,
        "project_name": project_name,
        "created_at": datetime.now().isoformat()
    }
    save_mappings(mappings)


def remove_project(project_dir: str) -> bool:
    """
    Remove a project mapping.

    Args:
        project_dir: Absolute path to the project directory

    Returns:
        True if mapping was removed, False if it didn't exist
    """
    mappings = get_mappings()
    normalized_path = os.path.normpath(project_dir)

    if normalized_path in mappings:
        del mappings[normalized_path]
        save_mappings(mappings)
        return True
    return False


def list_projects() -> Dict[str, Dict[str, Any]]:
    """
    List all project mappings.

    Returns:
        Dict mapping project directories to their notebook info
    """
    return get_mappings()


def get_project_name(project_dir: str) -> str:
    """
    Get the project name from a directory path.

    Args:
        project_dir: Absolute path to the project directory

    Returns:
        Project name (directory basename)
    """
    return os.path.basename(os.path.normpath(project_dir))


if __name__ == "__main__":
    # CLI for testing
    import sys

    if len(sys.argv) < 2:
        print("Usage: python project_manager.py <command> [args]")
        print("Commands:")
        print("  get <project_dir>     - Get notebook ID for project")
        print("  set <project_dir> <notebook_id> [name] - Set notebook mapping")
        print("  remove <project_dir>  - Remove project mapping")
        print("  list                   - List all projects")
        print("  name <project_dir>     - Get project name from directory")
        sys.exit(1)

    command = sys.argv[1]

    if command == "get":
        if len(sys.argv) < 3:
            print("Error: project_dir required")
            sys.exit(1)
        notebook_id = get_project_notebook(sys.argv[2])
        if notebook_id:
            print(f"Notebook ID: {notebook_id}")
        else:
            print("No mapping found for this project")

    elif command == "set":
        if len(sys.argv) < 4:
            print("Error: project_dir and notebook_id required")
            sys.exit(1)
        name = sys.argv[4] if len(sys.argv) > 4 else None
        set_project_notebook(sys.argv[2], sys.argv[3], name)
        print(f"Mapping saved: {sys.argv[2]} -> {sys.argv[3]}")

    elif command == "remove":
        if len(sys.argv) < 3:
            print("Error: project_dir required")
            sys.exit(1)
        if remove_project(sys.argv[2]):
            print(f"Mapping removed for {sys.argv[2]}")
        else:
            print(f"No mapping found for {sys.argv[2]}")

    elif command == "list":
        projects = list_projects()
        if not projects:
            print("No project mappings found")
        else:
            print("Project mappings:")
            for project_dir, info in projects.items():
                print(f"  {project_dir}")
                print(f"    Notebook: {info['notebook_id']}")
                print(f"    Name: {info['project_name']}")
                print(f"    Created: {info['created_at']}")

    elif command == "name":
        if len(sys.argv) < 3:
            print("Error: project_dir required")
            sys.exit(1)
        print(get_project_name(sys.argv[2]))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
