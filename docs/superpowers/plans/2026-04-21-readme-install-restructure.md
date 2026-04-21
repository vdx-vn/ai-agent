# README and Install Guidance Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make repository onboarding global-user-first so users can install `odoo-skills` from this repo without confusing local Odoo project setup with required bootstrap.

**Architecture:** Keep `README.md` as the landing page, but move detailed install and local project setup content into dedicated docs. Preserve install/build behavior, update runtime bundle README and CLI messaging to match the same story, and lock the wording with focused `unittest` coverage.

**Tech Stack:** Markdown docs, Python 3.12, `unittest`, Claude Code CLI plugin commands

---

## File structure and responsibilities

- **Modify:** `README.md`
  - Main landing page and quickstart for first-time global users.
- **Create:** `docs/install.md`
  - Detailed install, verification, uninstall, and troubleshooting guide.
- **Create:** `docs/project-setup.md`
  - Optional per-project Odoo setup guide for local docs/source/test integration.
- **Modify:** `tooling/build_plugin.py`
  - Runtime bundle README string written into `dist/marketplace/README.md`.
- **Modify:** `tooling/install_plugin.py`
  - Install success messaging only; no behavior change.
- **Modify:** `tooling/setup_local.py`
  - Legacy shim wording only; no behavior change.
- **Modify:** `docs/reference/odoo-paths.md`
  - Clarify that `project-setup` is per-project and optional.
- **Modify:** `docs/authoring/odoo-paths.md`
  - Mirror the same clarification.
- **Modify:** `tests/unit/test_plugin_foundation.py`
  - Lock README order, new docs, and optional project setup framing.
- **Modify:** `tests/unit/test_build_plugin.py`
  - Lock runtime bundle README wording and command order.
- **Modify:** `tests/unit/test_install_plugin.py`
  - Lock `run_install()` success output.
- **Modify:** `tests/unit/test_setup_local.py`
  - Lock stronger legacy shim messaging.
- **Modify:** `tests/unit/test_reference_docs.py`
  - Lock optional local-project framing in Odoo path reference docs.

**Do not create** `docs/development.md` in this pass. Keep maintainer commands in the lower half of `README.md` unless the README rewrite proves unmanageably long during implementation.

**Git note:** This plan includes optional commit checkpoints, but only execute them if the user explicitly asks for commits in that implementation session.

### Task 1: Lock global-user README flow, then rewrite README and add dedicated install docs

**Files:**
- Modify: `tests/unit/test_plugin_foundation.py`
- Modify: `README.md`
- Create: `docs/install.md`
- Create: `docs/project-setup.md`

- [ ] **Step 1: Replace the README contract test with the new global-user-first assertions**

Replace `PluginFoundationTests.test_readme_mentions_full_installation_and_usage_flow` in `tests/unit/test_plugin_foundation.py` with:

```python
    def test_readme_prioritizes_global_install_and_links_optional_project_setup_docs(self) -> None:
        readme_text = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertTrue((ROOT / "docs" / "install.md").exists())
        self.assertTrue((ROOT / "docs" / "project-setup.md").exists())
        self.assertIn("git clone git@github.com:vdx-vn/ai-agent", readme_text)
        self.assertIn("python3 -m pip install -e .", readme_text)
        self.assertIn("odoo-skills install-plugin", readme_text)
        self.assertIn("python3 -m tooling.install_plugin", readme_text)
        self.assertIn("## Optional: configure a local Odoo project", readme_text)
        self.assertIn(
            "Only do this if you want local Odoo docs/source paths and local test harness setup inside a specific Odoo repository.",
            readme_text,
        )
        self.assertIn("[docs/install.md](docs/install.md)", readme_text)
        self.assertIn("[docs/project-setup.md](docs/project-setup.md)", readme_text)
        self.assertIn("odoo-skills verify", readme_text)
        self.assertIn("odoo-skills build", readme_text)
        self.assertIn("odoo-skills smoke-install", readme_text)
        self.assertIn("claude --plugin-dir ~/.claude/plugins --plugin-dir .", readme_text)
        self.assertIn("claude plugin marketplace add ./dist/marketplace", readme_text)
        self.assertIn("python3 -m tooling.setup_local", readme_text)
        self.assertIn("deprecated", readme_text.lower())
        self.assertNotIn("## Fastest local marketplace install", readme_text)
        self.assertLess(
            readme_text.index("python3 -m pip install -e ."),
            readme_text.index("odoo-skills install-plugin"),
        )
        self.assertLess(
            readme_text.index("odoo-skills install-plugin"),
            readme_text.index("## Optional: configure a local Odoo project"),
        )
```

- [ ] **Step 2: Run the single README contract test and verify it fails**

Run:

```bash
python3 -m unittest tests.unit.test_plugin_foundation.PluginFoundationTests.test_readme_prioritizes_global_install_and_links_optional_project_setup_docs -v
```

Expected: FAIL because `docs/install.md` and `docs/project-setup.md` do not exist yet and the README still starts with `## Fastest local marketplace install`.

- [ ] **Step 3: Rewrite `README.md` with the new structure and create the two detailed docs**

Replace `README.md` with:

```markdown
# odoo-skills

Claude Code plugin for Odoo-focused skills. Install it once in Claude Code. Run per-project setup only if you want local Odoo docs, source, and test integration inside a specific Odoo repository.

## Quickstart

Clone this repository and install the CLI entrypoints:

```bash
git clone git@github.com:vdx-vn/ai-agent
cd ai-agent
python3 -m pip install -e .
```

Install the plugin into Claude Code:

```bash
odoo-skills install-plugin
claude plugin list --json
```

If `odoo-skills` is not on `PATH` yet, use the fallback:

```bash
python3 -m tooling.install_plugin
claude plugin list --json
```

Detailed install and troubleshooting: [docs/install.md](docs/install.md)

## Optional: configure a local Odoo project

Only do this if you want local Odoo docs/source paths and local test harness setup inside a specific Odoo repository.

```bash
cd /path/to/odoo-project
odoo-skills project-setup
# fallback
python3 -m tooling.cli project-setup
```

Detailed project setup guide: [docs/project-setup.md](docs/project-setup.md)

## What this repository contains

Runtime plugin payload stays small:
- `.claude-plugin/` - plugin metadata
- `skills/` - public shipped skill library
- `LICENSE`

Everything else supports authoring, validation, packaging, installation, project setup, or local development.

## Common workflows

### Verify plugin metadata and repo shape

```bash
odoo-skills verify
# fallback
python3 -m tooling.cli verify
# legacy script
odoo-skills-verify
```

### Build runtime marketplace bundle

```bash
odoo-skills build
# fallback
python3 -m tooling.cli build
# legacy script
odoo-skills-build
```

### Smoke-test local install flow

```bash
odoo-skills smoke-install
# fallback
python3 -m tooling.cli smoke-install
# legacy script
odoo-skills-smoke-install
```

### Run Claude Code directly against this repo during development

```bash
claude --plugin-dir .
```

If you also want default user plugins:

```bash
claude --plugin-dir ~/.claude/plugins --plugin-dir .
```

### Manual marketplace flow

Use this if you want to see or reproduce what `odoo-skills install-plugin` does:

```bash
odoo-skills build
claude plugin marketplace add ./dist/marketplace
claude plugin install odoo-skills@odoo-skills-dev --scope local
claude plugin list --json
```

### Uninstall

```bash
odoo-skills install-plugin --uninstall
# fallback
python3 -m tooling.install_plugin --uninstall
# legacy script
odoo-skills-install --uninstall
```

## Development commands

Install dev tooling:

```bash
python3 -m pip install -e .
```

Run full test suite:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Validate plugin metadata directly with Claude CLI:

```bash
claude plugin validate .
claude plugin validate dist/marketplace
```

## Deprecated compatibility shim

`python3 -m tooling.setup_local` remains as deprecated compatibility behavior for one release window.

Use:
- `odoo-skills install-plugin` for plugin installation
- `odoo-skills project-setup` only for local Odoo repositories

Deprecated commands:

```bash
python3 -m tooling.setup_local
python3 -m tooling.setup_local --uninstall
```
```

Create `docs/install.md` with:

```markdown
# Install odoo-skills from this repository

Use this flow when you want Claude Code to load the Odoo skill library from this repository.

## Requirements

- Python 3.12+
- Claude Code CLI installed as `claude`
- local clone of this repository

## Install

Clone the repository and install the CLI entrypoints:

```bash
git clone git@github.com:vdx-vn/ai-agent
cd ai-agent
python3 -m pip install -e .
```

Install the plugin into Claude Code:

```bash
odoo-skills install-plugin
```

Verify that Claude Code sees the plugin:

```bash
claude plugin list --json
```

If `odoo-skills` is not on `PATH`, run the module directly:

```bash
python3 -m tooling.install_plugin
claude plugin list --json
```

## What `install-plugin` does

`odoo-skills install-plugin`:
- builds `dist/marketplace/`
- runs `claude plugin validate`
- adds the local marketplace `odoo-skills-dev`
- installs `odoo-skills` with local scope

It does not ask for Odoo docs paths, Odoo source paths, `odoo-bin`, or project config.

## Optional local Odoo project setup

If you also want project-local Odoo docs/source/test integration, run `odoo-skills project-setup` inside that Odoo repository after plugin installation.

Guide: [project-setup.md](project-setup.md)

## Troubleshooting

### `odoo-skills: command not found`

The editable install did not put console entrypoints on your shell `PATH`.

Run:

```bash
python3 -m pip install -e .
```

Or use the module fallback:

```bash
python3 -m tooling.install_plugin
```

### `Claude CLI is required. Install \`claude\` and try again.`

Install Claude Code CLI first, then rerun `odoo-skills install-plugin`.

### `externally-managed-environment`

Use a virtual environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
```

## Uninstall

```bash
odoo-skills install-plugin --uninstall
```

Fallback:

```bash
python3 -m tooling.install_plugin --uninstall
```
```

Create `docs/project-setup.md` with:

```markdown
# Optional local Odoo project setup

Run this only for a local Odoo repository that needs Odoo docs, source paths, and local test harness integration.

## Before you start

Complete plugin installation first:

```bash
python3 -m pip install -e .
odoo-skills install-plugin
```

## Run project setup

From the Odoo project root:

```bash
odoo-skills project-setup
# fallback
python3 -m tooling.cli project-setup
```

The command prompts for:
- local Odoo documentation clone path
- local Odoo core source clone path
- Odoo version if auto-detection cannot infer it
- `odoo-bin` path from that Odoo core source tree
- Odoo config file path used by that project

It writes only project-local files:
- `.claude/settings.local.json`
- `.claude/odoo-skill-paths.json`

## Re-run after project moves or version changes

```bash
odoo-skills project-setup --force
# fallback
python3 -m tooling.cli project-setup --force
```

## Example with separate custom addons repository

```bash
cd /path/to/odoo-project
odoo-skills project-setup \
  --docs-root /home/xmars/src/odoo/documentation \
  --source-root /home/xmars/src/odoo/odoo-community \
  --version 18.0 \
  --odoo-bin /home/xmars/src/odoo/odoo-community/odoo-bin \
  --config /etc/odoo/odoo.conf \
  --yes
```

Fallback:

```bash
python3 -m tooling.cli project-setup \
  --docs-root /home/xmars/src/odoo/documentation \
  --source-root /home/xmars/src/odoo/odoo-community \
  --version 18.0 \
  --odoo-bin /home/xmars/src/odoo/odoo-community/odoo-bin \
  --config /etc/odoo/odoo.conf \
  --yes
```

## Local test harness note

Keep the base command in `.claude/settings.local.json` under `ODOO_TEST_BASE_CMD`.
`odoo-local-test-harness` treats it as the immutable base command, then appends runtime flags such as `-d`, `--test-tags`, `--test-enable`, `-i`, `-u`, and `--stop-after-init` safely.
```

- [ ] **Step 4: Run the updated README contract test and verify it passes**

Run:

```bash
python3 -m unittest tests.unit.test_plugin_foundation.PluginFoundationTests.test_readme_prioritizes_global_install_and_links_optional_project_setup_docs -v
```

Expected: PASS

- [ ] **Step 5: If the user asked for a commit in this session, create it**

```bash
git add README.md docs/install.md docs/project-setup.md tests/unit/test_plugin_foundation.py
git commit -m "docs: clarify repository install flow"
```

### Task 2: Lock runtime bundle README contract, then update the generated bundle README

**Files:**
- Modify: `tests/unit/test_build_plugin.py`
- Modify: `tooling/build_plugin.py`

- [ ] **Step 1: Tighten the runtime README assertions in `tests/unit/test_build_plugin.py`**

Replace the runtime README assertion block inside `BuildPluginTests.test_build_marketplace_creates_runtime_subset_only` with:

```python
            runtime_readme = (output_dir / "README.md").read_text(encoding="utf-8")
            self.assertIn("Runtime marketplace bundle", runtime_readme)
            self.assertIn("## Install plugin from this bundle", runtime_readme)
            self.assertIn("claude plugin marketplace add ./dist/marketplace", runtime_readme)
            self.assertIn("claude plugin install odoo-skills@odoo-skills-dev --scope local", runtime_readme)
            self.assertIn("## Optional: configure a local Odoo project", runtime_readme)
            self.assertIn("python3 -m pip install -e .", runtime_readme)
            self.assertIn("odoo-skills project-setup", runtime_readme)
            self.assertIn("Optional for local Odoo repositories only", runtime_readme)
            self.assertNotIn("odoo-skills-build", runtime_readme)
            self.assertNotIn("## Fastest local marketplace install", runtime_readme)
            self.assertLess(
                runtime_readme.index("claude plugin marketplace add ./dist/marketplace"),
                runtime_readme.index("claude plugin install odoo-skills@odoo-skills-dev --scope local"),
            )
            self.assertLess(
                runtime_readme.index("python3 -m pip install -e ."),
                runtime_readme.index("odoo-skills project-setup"),
            )
            self.assertNotIn("python3 tooling/setup_local.py", runtime_readme)
            self.assertNotIn("tooling/materialization/materialize_odoo_skill_paths.py", runtime_readme)
            self.assertNotIn(".claude/skills/odoo-paths.md", runtime_readme)
```

- [ ] **Step 2: Run the build plugin unit test and verify it fails**

Run:

```bash
python3 -m unittest tests.unit.test_build_plugin.BuildPluginTests.test_build_marketplace_creates_runtime_subset_only -v
```

Expected: FAIL because `RUNTIME_README` still starts with the old `## Fastest local marketplace install` block and still mentions `odoo-skills-build`.

- [ ] **Step 3: Replace `RUNTIME_README` in `tooling/build_plugin.py`**

Replace the `RUNTIME_README = """..."""` value with:

```python
RUNTIME_README = """# odoo-skills Runtime marketplace bundle

Public Claude Code plugin for Odoo-focused skills.

## Install plugin from this bundle

From the repository root that contains `dist/marketplace`:

```bash
claude plugin marketplace add ./dist/marketplace
claude plugin install odoo-skills@odoo-skills-dev --scope local
claude plugin list --json
```

## Optional: configure a local Odoo project

Optional for local Odoo repositories only. If you want local docs/source/test integration, install the repository CLI entrypoints from the original repository root first:

```bash
python3 -m pip install -e .
odoo-skills project-setup
# fallback
python3 -m tooling.cli project-setup
```

## Runtime contents

This marketplace bundle ships plugin metadata, public `skills/`, and license files only.
Repo-only authoring tools such as `tooling/` and `.claude/skills/` are not included in the runtime bundle.
"""
```

- [ ] **Step 4: Re-run the build plugin unit test and verify it passes**

Run:

```bash
python3 -m unittest tests.unit.test_build_plugin.BuildPluginTests.test_build_marketplace_creates_runtime_subset_only -v
```

Expected: PASS

- [ ] **Step 5: If the user asked for a commit in this session, create it**

```bash
git add tooling/build_plugin.py tests/unit/test_build_plugin.py
git commit -m "docs: fix runtime bundle install guidance"
```

### Task 3: Lock CLI wording, then update `install_plugin` and `setup_local` messages

**Files:**
- Modify: `tests/unit/test_install_plugin.py`
- Modify: `tests/unit/test_setup_local.py`
- Modify: `tooling/install_plugin.py`
- Modify: `tooling/setup_local.py`

- [ ] **Step 1: Add a focused `run_install()` output test and tighten shim messaging tests**

In `tests/unit/test_install_plugin.py`, change the import and add the new test class:

```python
from tooling.install_plugin import main, parse_args, run_install
```

```python
class RunInstallTests(unittest.TestCase):
    def test_run_install_prints_optional_project_setup_guidance(self) -> None:
        repo_root = ROOT
        args = Namespace(uninstall=False)
        marketplace_path = ROOT / "dist" / "marketplace"

        with patch("tooling.install_plugin.ensure_claude_cli"):
            with patch("tooling.install_plugin.build_marketplace", return_value=marketplace_path):
                with patch("tooling.install_plugin.run_command"):
                    with patch("builtins.print") as print_mock:
                        result = run_install(repo_root, args)

        self.assertEqual(result, 0)
        printed = "\n".join(call.args[0] for call in print_mock.call_args_list)
        self.assertIn("Plugin install complete", printed)
        self.assertIn("python3 -m pip install -e .", printed)
        self.assertIn("Optional for local Odoo repositories only", printed)
        self.assertIn("odoo-skills project-setup", printed)
        self.assertIn("python3 -m tooling.cli project-setup", printed)
```

In `tests/unit/test_setup_local.py`, tighten the printed-message assertions inside `SetupShimTests`:

```python
        printed = "\n".join(call.args[0] for call in print_mock.call_args_list)
        self.assertIn("deprecated", printed.lower())
        self.assertIn("legacy compatibility command", printed.lower())
        self.assertIn("odoo-skills install-plugin", printed)
        self.assertIn("python3 -m tooling.install_plugin", printed)
        self.assertIn("only when configuring a local odoo repository", printed.lower())
```

Use the same stronger assertions for `test_run_uninstall_prints_deprecation_and_delegates_to_install_plugin`, minus the `project-setup` check if the output string no longer includes it there.

- [ ] **Step 2: Run the focused CLI wording tests and verify they fail**

Run:

```bash
python3 -m unittest tests.unit.test_install_plugin tests.unit.test_setup_local -v
```

Expected: FAIL because `run_install()` and `setup_local` still print the older generic wording.

- [ ] **Step 3: Update the user-facing strings in `tooling/install_plugin.py` and `tooling/setup_local.py`**

In `tooling/install_plugin.py`, replace the success prints at the end of `run_install()` with:

```python
    print(f"Plugin install complete: {PLUGIN_NAME} from local marketplace bundle at {marketplace_path}")
    print("If `odoo-skills` is not on PATH yet, install repo CLI entrypoints with `python3 -m pip install -e .`.")
    print("Optional for local Odoo repositories only: run `odoo-skills project-setup` inside each Odoo project.")
    print("Fallback: `python3 -m tooling.cli project-setup`.")
```

In `tooling/setup_local.py`, replace `DEPRECATION_MESSAGE` with:

```python
DEPRECATION_MESSAGE = (
    "Deprecated legacy compatibility command: `tooling.setup_local` now only installs or uninstalls the plugin bundle. "
    "Use `odoo-skills install-plugin` or `python3 -m tooling.install_plugin` for plugin install. "
    "Use `odoo-skills project-setup` only when configuring a local Odoo repository."
)
```

Also replace the `ArgumentParser` description string with:

```python
        description=(
            "Deprecated legacy compatibility shim. Installs or uninstalls the local odoo-skills plugin bundle only; "
            "local Odoo repository configuration now lives in `odoo-skills project-setup`."
        )
```

And update `run_setup()` to print:

```python
    print(DEPRECATION_MESSAGE)
    print("Next after plugin install, run `odoo-skills project-setup` only when configuring a local Odoo repository.")
    print("Fallback: `python3 -m tooling.cli project-setup`.")
```

Keep behavior unchanged. Do not touch command dispatch or install semantics.

- [ ] **Step 4: Re-run the focused CLI wording tests and verify they pass**

Run:

```bash
python3 -m unittest tests.unit.test_install_plugin tests.unit.test_setup_local -v
```

Expected: PASS

- [ ] **Step 5: If the user asked for a commit in this session, create it**

```bash
git add tooling/install_plugin.py tooling/setup_local.py tests/unit/test_install_plugin.py tests/unit/test_setup_local.py
git commit -m "docs: align install and legacy shim messaging"
```

### Task 4: Lock optional project-setup framing in Odoo path reference docs, then update both docs

**Files:**
- Modify: `tests/unit/test_reference_docs.py`
- Modify: `docs/reference/odoo-paths.md`
- Modify: `docs/authoring/odoo-paths.md`

- [ ] **Step 1: Add a test that both Odoo path docs keep project setup scoped to local repositories**

Add this test to `tests/unit/test_reference_docs.py`:

```python
    def test_odoo_path_docs_scope_project_setup_to_local_repositories(self) -> None:
        for doc_path in (
            ROOT / "docs" / "reference" / "odoo-paths.md",
            ROOT / "docs" / "authoring" / "odoo-paths.md",
        ):
            text = doc_path.read_text(encoding="utf-8")
            self.assertIn(
                "Install repo entrypoints first with `python3 -m pip install -e .` from repo root.",
                text,
            )
            self.assertIn(
                "Only do this for a local Odoo repository that needs local docs/source/test integration.",
                text,
            )
            self.assertIn("Run `odoo-skills project-setup` from the Odoo project root.", text)
            self.assertIn("Keep local test harness base command", text)
```

- [ ] **Step 2: Run the new Odoo path docs test and verify it fails**

Run:

```bash
python3 -m unittest tests.unit.test_reference_docs.ReferenceDocsTests.test_odoo_path_docs_scope_project_setup_to_local_repositories -v
```

Expected: FAIL because both docs still say “From Odoo project root, run `odoo-skills project-setup`” without the explicit local-only framing.

- [ ] **Step 3: Replace the “Recommended workflow” section in both Odoo path docs**

In both `docs/reference/odoo-paths.md` and `docs/authoring/odoo-paths.md`, replace the entire `## Recommended workflow` list with:

```markdown
## Recommended workflow
1. Install repo entrypoints first with `python3 -m pip install -e .` from repo root.
2. Only do this for a local Odoo repository that needs local docs/source/test integration.
3. Run `odoo-skills project-setup` from the Odoo project root.
4. If `odoo-skills` is not on PATH, run `python3 -m tooling.cli project-setup`.
5. Command will ask for docs root, source root, version if auto-detection fails, `odoo-bin`, and config path, then write `.claude/odoo-skill-paths.json` and `.claude/settings.local.json` for that project.
6. Keep local test harness base command in `.claude/settings.local.json` under `ODOO_TEST_BASE_CMD` for `odoo-local-test-harness`.
7. If you prefer to keep placeholders, mentally substitute `<ODOO_DOCS_ROOT>` and `<ODOO_SOURCE_ROOT>` when reading skill references.
```

- [ ] **Step 4: Re-run the Odoo path docs test and verify it passes**

Run:

```bash
python3 -m unittest tests.unit.test_reference_docs.ReferenceDocsTests.test_odoo_path_docs_scope_project_setup_to_local_repositories -v
```

Expected: PASS

- [ ] **Step 5: If the user asked for a commit in this session, create it**

```bash
git add docs/reference/odoo-paths.md docs/authoring/odoo-paths.md tests/unit/test_reference_docs.py
git commit -m "docs: scope odoo path setup to local repos"
```

### Task 5: Run focused verification, then repo-level validation

**Files:**
- Modify: none expected
- Verify: `README.md`, new docs, updated Python files, updated tests

- [ ] **Step 1: Run the focused test suite for every touched contract**

Run:

```bash
python3 -m unittest \
  tests.unit.test_plugin_foundation \
  tests.unit.test_build_plugin \
  tests.unit.test_install_plugin \
  tests.unit.test_setup_local \
  tests.unit.test_reference_docs \
  -v
```

Expected: PASS

- [ ] **Step 2: Run repo validation**

Run:

```bash
odoo-skills-verify
```

Expected: exit code 0

- [ ] **Step 3: Read the top of `README.md` and both new docs once more as a first-time user sanity check**

Check these exact points before declaring success:

```text
1. First command sequence starts with clone + pip install, not marketplace build.
2. Plugin install appears before any `project-setup` instruction.
3. `project-setup` is explicitly optional and local-only.
4. README links to both `docs/install.md` and `docs/project-setup.md`.
5. Legacy `tooling.setup_local` language is clearly deprecated.
```

Expected: all five checks pass without further edits.

- [ ] **Step 4: If the user asked for a final commit in this session, create it**

```bash
git add README.md docs/install.md docs/project-setup.md docs/reference/odoo-paths.md docs/authoring/odoo-paths.md tooling/build_plugin.py tooling/install_plugin.py tooling/setup_local.py tests/unit/test_plugin_foundation.py tests/unit/test_build_plugin.py tests/unit/test_install_plugin.py tests/unit/test_setup_local.py tests/unit/test_reference_docs.py
git commit -m "docs: clarify plugin install and project setup"
```

## Self-review against spec

### Spec coverage
- **README global-user-first:** Task 1 rewrites `README.md` and locks order in `test_plugin_foundation.py`.
- **Detailed install doc:** Task 1 creates `docs/install.md`.
- **Detailed project setup doc:** Task 1 creates `docs/project-setup.md`.
- **Runtime bundle README alignment:** Task 2 updates `tooling/build_plugin.py` and locks it in `test_build_plugin.py`.
- **CLI/help text alignment:** Task 3 updates `tooling/install_plugin.py` and `tooling/setup_local.py`, with focused tests.
- **Other docs mention project setup as optional/local-only:** Task 4 updates both Odoo path docs and locks the wording.
- **Validation and no behavior change:** Task 5 runs focused tests and `odoo-skills-verify`.

### Placeholder scan
- No `TODO`, `TBD`, or “implement later” markers remain.
- Each code-changing step includes exact code or exact replacement text.
- Each validation step includes an exact command and expected outcome.

### Type and naming consistency
- Command surface is consistent throughout the plan: `odoo-skills install-plugin`, `odoo-skills project-setup`, `python3 -m tooling.install_plugin`, `python3 -m tooling.cli project-setup`.
- File names are consistent throughout the plan: `docs/install.md`, `docs/project-setup.md`.
- The wording target is consistent throughout the plan: `project-setup` is optional and only for local Odoo repositories.
