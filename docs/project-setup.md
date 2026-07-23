# Optional local Odoo project setup

Use this after you have installed `odoo-skills` for Codex CLI or Claude Code.

This step is optional and project-local. It is for Odoo repositories where you want local docs/source path materialization.

## Prerequisites

Before running project setup:

- Install the plugin for Codex CLI or Claude Code
- Be inside the Odoo repository you want to configure
- Have access to your local Odoo documentation clone and Odoo core source clone

## Run project setup

From inside the target Odoo repository:

```bash
odoo-skills project-setup
```

Fallback:

```bash
python3 -m tooling.cli project-setup
```

## What project setup prompts for

Project setup can prompt for:

- local Odoo documentation clone path
- local Odoo core source clone path
- Odoo version if auto-detection cannot infer it

## Files written

Project setup writes project-local configuration files inside the current Odoo repository:

- `.odoo-skills/project.json`
- `.claude/odoo-skill-paths.json`

These files store the docs/source path materialization configuration and are separate from the user-local agent plugin installation.

## Re-run with `--force`

If the project moves, changes Odoo series, or you need to refresh saved paths, re-run with `--force`:

```bash
odoo-skills project-setup --force
# fallback
python3 -m tooling.cli project-setup --force
```

## Custom addons example

If your custom addons live outside the Odoo core checkout, still point `--source-root` at the Odoo core source tree:

```bash
odoo-skills project-setup \
  --docs-root /home/xmars/src/odoo/documentation \
  --source-root /home/xmars/src/odoo/odoo-community \
  --version 18.0 \
  --yes
```

In that arrangement, custom addons may live in another repository alongside the Odoo core source tree.

