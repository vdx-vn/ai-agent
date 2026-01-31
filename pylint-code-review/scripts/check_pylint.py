#!/usr/bin/env python3
"""Pylint code review script with specific error checks.

This script runs pylint with a predefined set of error/warning checks
to review Python code quality.
"""

import subprocess
import sys
import json
from pathlib import Path

# Pylint checks to enable (from user requirements)
PYLINT_CHECKS = [
    # Error checks
    "syntax-error",
    "undefined-variable",
    "no-member",
    "not-callable",
    "used-before-assignment",
    "possibly-used-before-assignment",
    "unsubscriptable-object",
    "bad-file-encoding",
    "duplicate-key",
    "reimported",
    "redefined-builtin",
    "redefined-outer-name",
    "function-redefined",
    "expression-not-assigned",
    "unreachable",

    # Convention checks
    "missing-final-newline",
    "bad-indentation",
    "trailing-whitespace",
    "line-too-long",
    "superfluous-parens",
    "redundant-u-string-prefix",
    "multiple-statements",
    "unnecessary-pass",

    # Refactor checks
    "super-with-arguments",
    "consider-using-generator",
    "consider-using-set-comprehension",
    "consider-using-dict-items",
    "consider-using-in",
    "consider-using-ternary",
    "simplifiable-if-expression",
    "consider-using-with",
    "use-a-generator",
    "unnecessary-comprehension",
    "useless-return",
    "useless-parent-delegation",
    "self-assigning-variable",
    "chained-comparison",
    "singleton-comparison",
    "f-string-without-interpolation",

    # Warning checks
    "unused-import",
    "unused-argument",
    "raise-missing-from",
    "no-else-return",
    "no-else-raise",
    "use-implicit-booleaness-not-len",
    "pointless-string-statement",
    "pointless-statement",
    "inconsistent-return-statements",
    "too-many-nested-blocks",
    "unidiomatic-typecheck",
]

def run_pylint(file_path, output_format="json"):
    """Run pylint on the given file with the specified checks.

    Args:
        file_path: Path to the Python file to check
        output_format: Either 'json' or 'text'

    Returns:
        Pylint output as string
    """
    # Build pylint command
    cmd = [
        sys.executable, "-m", "pylint",
        file_path,
        "--disable=all",
        "--enable=" + ",".join(PYLINT_CHECKS),
        f"--output-format={output_format}",
        "--max-line-length=100",
    ]

    # Add confidence level for better results
    cmd.extend(["--confidence=HIGH,INFERENCE"])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False  # Don't raise on pylint errors
        )
        return result.stdout, result.stderr, result.returncode
    except FileNotFoundError:
        return "", "Error: pylint is not installed. Run: pip install pylint", 1

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: check_pylint.py <file_or_directory>", file=sys.stderr)
        sys.exit(1)

    target = sys.argv[1]
    output_format = "text" if len(sys.argv) < 3 else sys.argv[2]

    stdout, stderr, returncode = run_pylint(target, output_format)

    if stderr:
        print(stderr, file=sys.stderr)

    print(stdout)
    sys.exit(returncode)

if __name__ == "__main__":
    main()
