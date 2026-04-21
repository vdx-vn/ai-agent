# Checklist

## Intake
- [ ] Confirm the target is Python code.
- [ ] Confirm static-analysis findings are the requested artifact.
- [ ] Identify the target path or files to review.
- [ ] Identify whether raw or summarized findings are preferred.

## Execution
- [ ] Run `scripts/check_pylint.py` against the target.
- [ ] Capture command success, failure, or environment blocker.
- [ ] Read `pylint_checks.md` for any non-obvious rule interpretation.

## Analysis
- [ ] Group findings by category or severity.
- [ ] Name affected path and pylint rule for each issue.
- [ ] Keep static-analysis findings separate from assumptions about runtime behavior.

## Output
- [ ] Return reviewed target scope.
- [ ] Return execution status.
- [ ] Return grouped findings.
- [ ] Return concise fix guidance.
- [ ] Return blocker or missing-environment note when relevant.
