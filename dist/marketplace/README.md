# odoo-skills Runtime marketplace bundle

Public Claude Code plugin for Odoo-focused skills.

## Install plugin from this bundle

```bash
claude plugin marketplace add ./dist/marketplace
claude plugin install odoo-skills@odoo-skills-dev --scope local
claude plugin list --json
```

## Optional: configure a local Odoo project

Optional for local Odoo repositories only. These follow-up commands must be run from a clone of the source repository, not from this runtime bundle. Install the repository CLI entrypoints from that separate source-repo clone first, then run project setup in the target Odoo repository:

```bash
python3 -m pip install -e .
odoo-skills project-setup
# fallback
python3 -m tooling.cli project-setup
```

## Runtime contents

This bundle ships plugin metadata, public skills, and license files only.
Repo-only authoring tools such as tooling/ and .claude/skills/ are not included.
