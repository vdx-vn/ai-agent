# odoo-skills

Public Claude Code plugin for Odoo-focused skills.

## Local development

Run Claude Code with this repository as a local plugin source, plus default claude plugin sources:

```bash
claude --plugin-dir ~/.claude/plugins --plugin-dir .
```

## Local marketplace install test

Add the local marketplace and install this plugin from it:

```bash
claude plugin marketplace add ./
claude plugin install odoo-skills@odoo-skills-dev --scope local
```

Slash-command equivalents:

- /plugin marketplace add
- /plugin install odoo-skills@odoo-skills-dev
