# Optional local Odoo project setup

Use this after you have installed `odoo-skills` for Codex CLI or Claude Code.

This step is optional and project-local. It is for Odoo repositories where you want local docs/source path materialization and local test harness configuration.

## Prerequisites

Before running project setup:

- Install the plugin for Codex CLI or Claude Code
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

- `.odoo-skills/project.json`
- `.claude/settings.local.json`
- `.claude/odoo-skill-paths.json`

`.odoo-skills/project.json` is the shared project setup used by Codex CLI and repo-local scripts. The `.claude/*` files are also written for Claude Code compatibility.

These files are separate from the user-local agent plugin installation.

Codex CLI does not need `.claude/settings.local.json`; the local harness can read `.odoo-skills/project.json` directly from the current repository. Claude Code uses `.claude/settings.local.json` to inject the same base command into its environment as `ODOO_TEST_BASE_CMD`.

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

The local test harness reads `ODOO_TEST_BASE_CMD` from the environment when it is present. This is the Claude Code compatibility path because Claude Code injects it from `.claude/settings.local.json`.

If that environment variable is not present, the harness searches upward from the current directory for `.odoo-skills/project.json` and reads `odooTestBaseCmd`. This is the default Codex CLI path.

That base command must already include `-c` or `--config`, and it must not include runtime-managed flags such as `-d`, `--test-tags`, `-i`, `-u`, `--test-enable`, or `--stop-after-init`.

If you prefer Codex CLI to pass the value as an environment variable instead of relying on `.odoo-skills/project.json`, add it to `~/.codex/config.toml` or a trusted project `.codex/config.toml`:

```toml
[shell_environment_policy]
inherit = "core"
set = { ODOO_TEST_BASE_CMD = "/path/to/python /path/to/odoo-bin -c /path/to/odoo.conf" }
```

Do not use `ODOO_TEST` or `DB` for this harness. Pass the test database at runtime with the harness `--db` argument.

Project setup is the supported path for capturing the config inputs needed for this local harness behavior in both Codex CLI and Claude Code.
