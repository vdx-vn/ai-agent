# odoo-skills Runtime marketplace bundle

Public Claude Code plugin for Odoo-focused skills.

## Fastest local marketplace install

From the repository root that produced this bundle, build the runtime bundle and install from the local marketplace:

```bash
odoo-skills-build
claude plugin marketplace add ./dist/marketplace
claude plugin install odoo-skills@odoo-skills-dev --scope local
claude plugin list --json
```

Use this when you want the shortest local plugin install path. If the target repository is an Odoo project, run `odoo-skills project-setup` in that project after plugin install.

## Install and use plugin

After plugin install, configure each Odoo project separately:

```bash
odoo-skills project-setup
# fallback
python3 -m tooling.cli project-setup
```

## Runtime contents

This marketplace bundle ships plugin metadata, public `skills/`, and license files only.
Repo-only authoring tools such as `tooling/` and `.claude/skills/` are not included in runtime bundle.
