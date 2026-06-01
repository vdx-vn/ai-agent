# odoo-skills-v19

Odoo-focused skills for coding agents, packaged with provider metadata for Codex CLI and Claude Code.

This repository follows the top-level skill-library layout used by `obra/superpowers`: plugin metadata lives in provider-specific directories, while the shipped skills live in `skills/`.

## Installation

Clone the repository and install the local development commands:

```bash
git clone git@github.com:vdx-vn/ai-agent
cd ai-agent
python3 -m pip install -e .
export ODOO_SKILLS_REPO="$PWD"
```

### Codex CLI

Install Codex CLI if it is not already available:

```bash
npm install -g @openai/codex
# or, on macOS:
brew install --cask codex
```

Authenticate and add this repository as a local plugin marketplace:

```bash
codex login
odoo-skills build
codex plugin marketplace add "$ODOO_SKILLS_REPO/dist/marketplace"
codex
```

`codex plugin marketplace add` needs the path to this built skills marketplace, not the Odoo/project repository where you want to use the skills. If you are already inside a separate project repository, pass the absolute path instead:

```bash
codex plugin marketplace add /absolute/path/to/ai-agent/dist/marketplace
```

If you previously added the source repository root, replace it after building:

```bash
codex plugin marketplace remove odoo-skills-v19
codex plugin marketplace add "$ODOO_SKILLS_REPO/dist/marketplace"
```

Inside Codex, open `/plugins`, search for `odoo-skills-v19`, and install the local plugin.

Codex CLI installation reference: [OpenAI Codex CLI getting started](https://help.openai.com/en/articles/11096431-openai-codex-ligetting-started) and [openai/codex](https://github.com/openai/codex).

### Claude Code

Install the plugin for your Claude Code user:

```bash
odoo-skills install-plugin
claude plugin list --json
```

Fallback if the shell entrypoint is unavailable:

```bash
python3 -m tooling.install_plugin
claude plugin list --json
```

For detailed Claude Code install, verification, troubleshooting, and uninstall guidance, see [docs/install.md](docs/install.md).

## Optional Project Setup

Only do this if you want local Odoo docs/source paths and local test harness setup inside a specific Odoo repository.

Run this inside the Odoo repository you want to configure:

```bash
odoo-skills project-setup
# fallback
python3 -m tooling.cli project-setup
```

For prerequisites, prompts, written files, reruns, and examples, see [docs/project-setup.md](docs/project-setup.md).

## Repository Contents

Runtime plugin payload:

- `.codex-plugin/` - Codex plugin metadata
- `.claude-plugin/` - Claude Code plugin metadata and local marketplace metadata
- `skills/` - public shipped skill library
- `README.md`, `LICENSE`

Development-only support:

- `tooling/` - build, install, validation, and project setup commands
- `tests/` - unittest coverage for plugin structure, skills, and scripts
- `docs/` - install, project setup, authoring, and reference docs
- `skill-creator/` - local authoring helper skill

## Development

Run validation and tests:

```bash
odoo-skills verify
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Build the runtime marketplace bundle:

```bash
odoo-skills build
```

Smoke-test the local install flow:

```bash
odoo-skills smoke-install
```

Deprecated compatibility shim:

```bash
python3 -m tooling.setup_local
python3 -m tooling.setup_local --uninstall
```

Use `odoo-skills install-plugin` for Claude Code user-local installation. For Codex CLI, build the runtime marketplace, add its path as a local plugin marketplace, and install `odoo-skills-v19` from `/plugins`. Then use `odoo-skills project-setup` only inside Odoo repositories that need local integration.
