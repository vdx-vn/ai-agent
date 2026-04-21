# Examples

## Positive triggers
1. "Review this Python module with pylint-style checks before merge."
   - Expected: use `pylint-code-review` as primary skill.
2. "Run static analysis on `tooling/build_plugin.py` and summarize issues."
   - Expected: use `pylint-code-review` as primary skill.
3. "Check these Python files for unused imports and unreachable code."
   - Expected: use `pylint-code-review` as primary skill.

## Negative triggers
1. "Run unit tests for this Python package and tell me what fails."
   - Expected: do not use `pylint-code-review` as primary skill.
2. "Fix this Python module for me."
   - Expected: do not use `pylint-code-review` as primary skill.
3. "Review this JavaScript component."
   - Expected: do not use `pylint-code-review` as primary skill.

## Tie-breaker
- Prompt: "Check this Python diff for lint issues and summarize what to fix."
- Why this skill wins: the requested artifact is Python static-analysis findings, not code changes or runtime test evidence.
