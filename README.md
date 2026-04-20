# odoo-skills

Public Claude Code plugin for Odoo-focused skills.

## Recommended local setup

Clone the repo and run the guided one-command setup from project root:

```bash
git clone git@github.com:vdx-vn/ai-agent
cd ai-agent
python3 tooling/setup_local.py
```

The setup prompts for:
- your local Odoo documentation clone path
- your local Odoo source clone path
- the Odoo version if auto-detection cannot infer it
- the `odoo-bin` path
- the Odoo config file path

It then materializes the local `.claude/skills` copy, writes `.claude/odoo-skill-paths.json`, stores `ODOO_TEST_BASE_CMD` in `.claude/settings.local.json`, builds the local marketplace bundle, and installs the plugin into Claude Code.

### Non-interactive example

```bash
python3 tooling/setup_local.py \
  --docs-root /path/to/odoo/documentation \
  --source-root /path/to/odoo/source \
  --odoo-bin /path/to/odoo-bin \
  --config /path/to/odoo.conf \
  --yes
```

### Uninstall

```bash
python3 tooling/setup_local.py --uninstall
```

## Advanced manual fallback

If you only want skill-path materialization without the guided local install flow, run:

```bash
python3 tooling/materialization/materialize_odoo_skill_paths.py --docs-root /path/to/odoo/documentation --source-root /path/to/odoo/source
```

Add `--version 18.0` or similar if auto-detection cannot infer the Odoo series.

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
