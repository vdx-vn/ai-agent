# Overview

## Primary routing rule
Use this skill only when the primary requested output is Python static-analysis review findings. If the user wants non-Python review, runtime testing, or direct implementation, another skill should own the request.

## Scope
Review existing Python code with the bundled pylint profile and turn raw findings into structured, actionable review feedback.

## Primary artifact
Structured Python static-analysis findings with rule names, affected targets, fix guidance, and execution blockers.

## Dependencies
- Python 3
- `pylint` available in the active environment

## Boundaries
- This skill is for Python code only.
- This skill does not execute runtime tests.
- This skill does not implement fixes.
- This skill should not own non-Python review requests.

## Core command
- `python3 skills/pylint-code-review/scripts/check_pylint.py <target>`
- `python3 skills/pylint-code-review/scripts/check_pylint.py <target> json`

## Frequent nearby workflows
- implementation workflow for applying fixes
- testing workflow for runtime validation after fixes
