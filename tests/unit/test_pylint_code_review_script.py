import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "skills" / "pylint-code-review" / "scripts" / "check_pylint.py"


def load_script_module():
    spec = importlib.util.spec_from_file_location("pylint_code_review_script", SCRIPT_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    old_value = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = old_value
    return module


class PylintCodeReviewScriptTests(unittest.TestCase):
    def test_run_pylint_normalizes_missing_module_error(self) -> None:
        result = types.SimpleNamespace(
            stdout="",
            stderr="/usr/bin/python3: No module named 'pylint'\n",
            returncode=1,
        )
        script = load_script_module()

        with patch.object(script.subprocess, "run", return_value=result):
            stdout, stderr, returncode = script.run_pylint("tooling/cli.py")

        self.assertEqual(stdout, "")
        self.assertEqual(
            stderr,
            "Error: pylint is not installed. Run: pip install pylint",
        )
        self.assertEqual(returncode, 1)


if __name__ == "__main__":
    unittest.main()
