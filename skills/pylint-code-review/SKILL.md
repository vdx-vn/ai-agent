---
name: pylint-code-review
description: "Review Python code with bundled pylint checks and return structured static-analysis findings. Use when the main output should be Python lint-style review findings for a file, module, or diff. Do not use for non-Python review, runtime testing, or direct code implementation."
---

# Purpose
Review Python code with a bundled pylint profile and return structured findings, fix guidance, and execution blockers.

# Primary routing rule
Use this skill only when the primary requested output is Python static-analysis review findings. If the user wants direct code changes, use a build or implementation skill. If the user wants runtime validation or test execution, use a testing skill.

# Use this skill when
- review a Python file, module, package, or diff for lint-style correctness and maintainability issues
- run a deterministic pylint profile and explain reported findings
- turn pylint output into prioritized review feedback with fix suggestions
- sanity-check Python code quality before merge when static analysis is the main artifact

# Do not use this skill when
- the target is not Python code
- the user wants runtime testing, debugging, or executed validation evidence
- the user wants code changes implemented instead of review findings
- the task is to design or enforce a repository-wide lint policy

# Required inputs
- Python target path to review, or diff context that identifies the target files
- desired output shape if the user wants raw findings, grouped findings, or concise review notes
- current environment status if pylint is known to be unavailable

# Workflow
1. Confirm the target is Python code and static-analysis review is the requested artifact.
2. Run `scripts/check_pylint.py` against the target path.
3. Read `references/pylint_checks.md` when a reported rule needs interpretation or fix guidance.
4. Group findings by severity or category, naming the affected path and rule.
5. Return structured review findings, suggested fixes, and any blocker such as missing `pylint`.

# Output contract
- reviewed target path or scope
- execution status for `scripts/check_pylint.py`
- grouped findings with pylint rule names
- concise fix guidance for each actionable issue
- blockers, assumptions, or missing-environment notes

# Guardrails
- Keep the skill narrow to Python static analysis.
- Prefer deterministic findings from the bundled pylint profile over ad-hoc stylistic opinions.
- If `pylint` is unavailable, report the blocker and required install command instead of guessing.
- Do not claim runtime correctness from static-analysis output alone.

# Must hand off when
- If the user wants code edits now, hand off to the relevant implementation workflow.
- If the user wants runtime validation or test evidence, hand off to a testing workflow.
- If the review target is not Python, hand off to the more appropriate language or review workflow.

# References
- Read `references/overview.md` first for routing and boundaries.
- Use `references/checklist.md` for deterministic review steps.
- Use `references/examples.md` for trigger and non-trigger patterns.
- Use `references/pylint_checks.md` for rule explanations and fix suggestions.
