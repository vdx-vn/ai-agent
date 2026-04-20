# odoo-skills Runtime marketplace bundle

Public Claude Code plugin for Odoo-focused skills.

## Install from local marketplace

```bash
claude plugin marketplace add ./
claude plugin install odoo-skills@odoo-skills-dev --scope local
```

Slash-command equivalents:

- /plugin marketplace add
- /plugin install odoo-skills@odoo-skills-dev

## Runtime contents

This marketplace bundle ships plugin metadata, public `skills/`, and license files only.
Repo-only authoring tools such as `tooling/` and `.claude/skills/` are not included in runtime bundle.
