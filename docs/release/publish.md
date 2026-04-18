# odoo-skills publish checklist

Use this checklist before publishing the `odoo-skills` plugin.

## Scope confirmation
- [ ] Changes are limited to approved release scope for this iteration.
- [ ] Business skill frontmatter descriptions are normalized to approved wording.
- [ ] Business skill docs contain no unresolved release placeholders or TODO/TBD markers.

## Required verification commands
- [ ] `python3 -m unittest tests.unit.test_business_skill_contracts -v`
- [ ] `python3 -m unittest tests.unit.test_validate_frontmatter tests.unit.test_validate_release tests.unit.test_verify_command -v`
- [ ] `python3 -m venv /tmp/odoo-skills-task10-venv`
- [ ] `/tmp/odoo-skills-task10-venv/bin/pip install -e .`
- [ ] `/tmp/odoo-skills-task10-venv/bin/odoo-skills-verify`
- [ ] `claude plugin validate .`

## Publish readiness checks
- [ ] `skills/` and `.claude/skills/` business skill content are aligned.
- [ ] `docs/release/publish.md` exists and is up to date.
- [ ] Working tree is reviewed and contains only intended changes.
- [ ] Any `__pycache__` created during verification has been removed.

## Evidence to capture in release note or handoff
- [ ] Command outputs for all required verification commands.
- [ ] Final status recorded as `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or `BLOCKED`.
- [ ] Any blockers or concerns documented with impact and next action.
