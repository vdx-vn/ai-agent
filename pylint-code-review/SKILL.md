---
name: pylint-code-review
description: Python code review skill using pylint to enforce code quality standards. Automatically runs pylint with 45+ specific error, warning, and refactor checks including - syntax-error, undefined-variable, unused-import, bad-indentation, trailing-whitespace, line-too-long, missing-final-newline, unreachable, and many Python best practices like use context managers, avoid no-else-return, prefer generators. Use when reviewing Python code for quality, style, and best practice violations. Generates detailed reports with explanations and fix suggestions for each violation.
---

# Pylint Code Review

Automatically review Python code using pylint with comprehensive quality checks.

## Quick Start

To review a Python file:

```bash
python scripts/check_pylint.py <path-to-file>
```

For JSON output (useful for further processing):

```bash
python scripts/check_pylint.py <path-to-file> json
```

## Workflow

1. **Run the review**: Execute `check_pylint.py` on the target file or directory
2. **Review findings**: Examine the output for violations
3. **Fix issues**: Apply suggested fixes based on the detailed explanations
4. **Re-run**: Run again to verify all issues are resolved

## Understanding Checks

The skill runs pylint with 45+ specific checks covering:

- **Error checks**: syntax-error, undefined-variable, no-member, not-callable, etc.
- **Convention checks**: missing-final-newline, bad-indentation, trailing-whitespace, line-too-long, etc.
- **Refactor checks**: super-with-arguments, consider-using-generator, consider-using-with, etc.
- **Warning checks**: unused-import, unused-argument, no-else-return, etc.

For detailed explanations and fix suggestions for each check, see [pylint_checks.md](references/pylint_checks.md).

## Example Violations and Fixes

### Bad Indentation
```python
# Bad
def foo():
    x = 1
      y = 2  # bad-indentation

# Good
def foo():
    x = 1
    y = 2
```

### No-Else-Return
```python
# Bad
def check(x):
    if x > 0:
        return True
    else:
        return False

# Good
def check(x):
    if x > 0:
        return True
    return False
```

### Consider-Using-With
```python
# Bad
f = open("file.txt")
content = f.read()
f.close()

# Good
with open("file.txt") as f:
    content = f.read()
```

### Use-Implicit-Booleaness-Not-Len
```python
# Bad
if len(items) == 0:
    pass

# Good
if not items:
    pass
```

## Installation

Ensure pylint is installed:

```bash
pip install pylint
```

The script uses the same Python interpreter as your environment.
