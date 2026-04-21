# Optional local Odoo project setup

Use this only after you have already installed `odoo-skills` for your Claude Code user.

This step is optional and project-local. It is for Odoo repositories where you want local docs/source path materialization and local test harness configuration.

## Prerequisites

Before running project setup:

- Install the plugin for your Claude Code user with `odoo-skills install-plugin` or `python3 -m tooling.install_plugin`
- Be inside the Odoo repository you want to configure
- Have access to your local Odoo documentation clone and Odoo core source clone
- Know which config file the repository should use for local test commands

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
- `odoo-bin` path from the Odoo core source tree
- Odoo config file path used by that project

## Files written

Project setup writes project-local configuration files inside the current Odoo repository:

- `.claude/settings.local.json`
- `.claude/odoo-skill-paths.json`

These files are separate from the user-local Claude Code plugin installation.

## Re-run with `--force`

If the project moves, changes Odoo series, or you need to refresh saved paths, re-run with `--force`:

```bash
odoo-skills project-setup --force
# fallback
python3 -m tooling.cli project-setup --force
```

## Custom addons example

If your custom addons live outside the Odoo core checkout, still point `--source-root` at the Odoo core source tree and use the project config that includes the correct `addons_path` entries:

```bash
odoo-skills project-setup \
  --docs-root /home/xmars/src/odoo/documentation \
  --source-root /home/xmars/src/odoo/odoo-community \
  --version 18.0 \
  --odoo-bin /home/xmars/src/odoo/odoo-community/odoo-bin \
  --config /etc/odoo/odoo.conf \
  --yes
```

In that arrangement, custom addons may live in another repository, while the config file ties together Odoo core addons and custom addons through `addons_path`.

## `ODOO_TEST_BASE_CMD` note

The local test harness expects `.claude/settings.local.json` to define `ODOO_TEST_BASE_CMD` under `env`.

That base command must already include `-c` or `--config`, and it must not include runtime-managed flags such as `-d`, `--test-tags`, `-i`, `-u`, `--test-enable`, or `--stop-after-init`.

Project setup is the supported path for capturing the config inputs needed for this local harness behavior.
