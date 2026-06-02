# odoo-skills-v19

Odoo-focused skills for coding agents. Compatible with Claude Code, Codex CLI, Antigravity CLI (agy), and any agent CLI that reads `SKILL.md` files.

Plugin metadata lives in provider-specific directories; shipped skills live in `skills/`. Native workspace skills live in `.agents/skills/` (symlinked to `skills/`).

## Installation

Clone the repository and install the local development commands:

```bash
git clone git@github.com:vdx-vn/ai-agent -b odoo-19
cd ai-agent
python3 -m pip install -e .
export ODOO_SKILLS_REPO="$PWD"
```

### Antigravity CLI (agy)

Skills are auto-discovered from `.agents/skills/` when you work inside this repository. No install step needed — open agy from this repo root and skills are available immediately:

```bash
cd /path/to/ai-agent
agy
```

To use skills from a separate Odoo project, symlink or copy `.agents/skills/` into that project's root:

```bash
ln -s /path/to/ai-agent/.agents/skills /path/to/your-odoo-project/.agents/skills
```

Then open agy from your Odoo project and skills will be discovered automatically.

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

### Other CLIs

Any agent CLI that reads `{workspace}/.agents/skills/{skill_name}/SKILL.md` will discover these skills automatically. Skills use standard YAML frontmatter (`name`, `description`) with no CLI-specific syntax.

## Optional Project Setup

Only do this if you want local Odoo docs/source paths and local test harness setup inside a specific Odoo repository.

Run this inside the Odoo repository you want to configure:

```bash
odoo-skills project-setup
# fallback
python3 -m tooling.cli project-setup
```

For prerequisites, prompts, written files, reruns, and examples, see [docs/project-setup.md](docs/project-setup.md).

The supported shared test-harness configuration is `.odoo-skills/project.json`:

```json
{
  "odooTestBaseCmd": "/path/to/python /path/to/odoo-bin -c /path/to/odoo.conf"
}
```

Claude Code receives the same value through `.claude/settings.local.json` as `ODOO_TEST_BASE_CMD`. Codex CLI reads `.odoo-skills/project.json` directly; if you prefer environment injection for Codex shell commands, add this to `~/.codex/config.toml` or the trusted project `.codex/config.toml`:

```toml
[shell_environment_policy]
inherit = "core"
set = { ODOO_TEST_BASE_CMD = "/path/to/python /path/to/odoo-bin -c /path/to/odoo.conf" }
```

Keep `ODOO_TEST_BASE_CMD` as the immutable base command only. Do not include runtime-managed flags like `-d`, `--test-tags`, `-i`, `-u`, `--test-enable`, or `--stop-after-init`; the local harness appends those.

## Repository Contents

Runtime plugin payload:

- `.agents/skills/` - native workspace skills (symlinks to `skills/`); auto-discovered by agy and compatible CLIs
- `.codex-plugin/` - Codex plugin metadata
- `.claude-plugin/` - Claude Code plugin metadata and local marketplace metadata
- `skills/` - canonical public skill library (source of truth)
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
