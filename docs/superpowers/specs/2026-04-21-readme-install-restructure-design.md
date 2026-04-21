# README and install guidance restructure design

## Summary

Restructure repository documentation so global Claude Code users can install `odoo-skills` from this repository without first understanding local Odoo project setup. Make `README.md` global-user-first, move local Odoo project configuration into dedicated docs, and align CLI/help text so `project-setup` is clearly optional and only for users integrating local Odoo repositories.

## Problem

Current documentation mixes three audiences in one path:
- global users who want to install plugin from this repository
- local Odoo developers who want project-specific path and test setup
- maintainers working on plugin packaging and validation

This creates avoidable confusion:
- `README.md` starts with a fast install path that uses `odoo-skills-build` before the README explains how that command becomes available
- README framing makes `project-setup` feel mandatory for everyone
- user install flow and local Odoo project setup flow are interleaved
- deprecated setup shim still competes with primary path in user mental model

## Audience and success target

### Primary audience
Global Claude Code users who want to install `odoo-skills` from this repository.

### Secondary audience
Team members who also want optional local Odoo project integration.

### Success target
A first-time global user can read the top of `README.md`, run the documented commands in order, install the plugin successfully, verify the installation, and understand that `project-setup` is optional unless they are wiring the plugin into a local Odoo repository.

## Design decisions

1. Keep one primary `README.md` as landing page and quickstart.
2. Reorder README so first-time install comes before project-local setup and maintainer workflows.
3. Add focused secondary docs for details that do not belong in the landing path.
4. Align CLI/help text and legacy wording with the same install story.
5. Do not change packaging, plugin metadata, or runtime build behavior.

## Proposed documentation structure

### README.md
Reframe `README.md` around user onboarding.

Proposed order:
1. short description of what `odoo-skills` provides
2. recommended quickstart for global users
3. verify installation worked
4. optional local Odoo `project-setup` section
5. common workflows
   - install plugin
   - use direct `claude --plugin-dir .` development mode
   - uninstall
6. maintainer and development commands
7. deprecated and legacy commands

Key wording changes:
- remove opening that depends on preinstalled entrypoints
- replace current three-phase framing with install-first framing
- explicitly say users do not need to copy skills into each Odoo project
- explicitly say `project-setup` is optional and only needed for local Odoo project integration

### docs/install.md
Create detailed installation reference for global users.

Contents:
- prerequisites
- clone repository
- `python3 -m pip install -e .`
- plugin install commands using primary entrypoints first
- verification commands
- troubleshooting for missing `claude`, missing PATH entrypoints, and virtualenv fallback
- uninstall flow

Purpose:
Keep README concise while preserving a stable reference page for detailed onboarding and troubleshooting.

### docs/project-setup.md
Create focused guide for optional local Odoo project integration.

Contents:
- when `odoo-skills project-setup` is needed
- required inputs: docs root, source root, version, `odoo-bin`, config
- files written: `.claude/settings.local.json`, `.claude/odoo-skill-paths.json`
- custom addons repo example
- `--force` rerun guidance
- short note on `ODOO_TEST_BASE_CMD` and local harness relationship

Purpose:
Separate local Odoo repository configuration from plugin installation so global users do not mistake it for required bootstrap.

### Optional docs/development.md
Only add this file if README remains too long after moving user-facing detail into dedicated docs.

Contents, if needed:
- verify, build, smoke-install, test suite, direct plugin validation, direct plugin source usage

Purpose:
Move maintainer-only detail out of README without losing reference value.

## Repo and CLI wording changes

### tooling/install_plugin.py
Keep behavior unchanged. Tighten success messaging so it says:
- plugin install is complete
- CLI entrypoints may still need `pip install -e .` if missing
- `odoo-skills project-setup` is optional and only for local Odoo repos

### tooling/setup_local.py
Keep deprecation shim behavior unchanged. Tighten deprecation output so it no longer reads like a normal starting point. It should clearly state that it is a legacy compatibility command and direct users to:
- `python3 -m tooling.install_plugin` or `odoo-skills install-plugin` for plugin install
- `odoo-skills project-setup` only when configuring a local Odoo repository

### Other docs
If other repo docs mention local setup as universal requirement, rewrite them to preserve the new split:
- plugin installation for everyone
- project setup only for local Odoo repo integration

## Command surface guidance

Preferred command examples in user docs:
- `odoo-skills install-plugin`
- `odoo-skills project-setup`
- `odoo-skills verify`
- `odoo-skills build`
- `odoo-skills smoke-install`

Fallback command examples remain documented, but secondary:
- `python3 -m tooling.install_plugin`
- `python3 -m tooling.cli project-setup`
- `python3 -m tooling.cli verify`
- `python3 -m tooling.cli build`
- `python3 -m tooling.cli smoke-install`

Reason:
Users should see one stable command family first. Module-invocation fallbacks remain available for environments where entrypoints are unavailable.

## Non-goals

- no change to packaged public skill inventory
- no change to runtime marketplace subset behavior
- no change to build, verify, smoke-install, or install semantics
- no new distribution channel beyond current repo-based install flow
- no attempt to make `project-setup` run during plugin installation

## Risks and mitigations

### Risk: README still too long
Mitigation: move detail to `docs/install.md` and `docs/project-setup.md`, keep README command path short.

### Risk: command examples drift across files
Mitigation: use one recommended command family consistently and keep module invocation labeled as fallback only.

### Risk: legacy setup text continues to confuse users
Mitigation: rewrite deprecation wording to call it legacy compatibility path, not setup entrypoint.

## Acceptance criteria

1. A brand-new global user can follow the top of `README.md` to successful plugin install without prior repository knowledge.
2. The first command sequence in `README.md` does not depend on entrypoints that the README has not yet explained how to install.
3. `README.md` clearly states that `project-setup` is optional and only for local Odoo project integration.
4. Detailed local Odoo setup guidance lives outside the main install flow.
5. Legacy `tooling.setup_local` is documented only as deprecated compatibility behavior.
6. User-facing wording in README and CLI messages does not contradict the install story.

## Validation plan

1. Read the new README from top to bottom as a first-time user.
2. Confirm documented command order is executable without hidden prerequisites.
3. If CLI strings change, run affected unit tests or add small targeted tests only where needed.
4. Run `odoo-skills-verify` if documentation references or repo validation surface are affected.
5. Avoid broader packaging or smoke-install changes unless documentation cleanup reveals a real mismatch.

## Expected implementation scope

Likely files:
- `README.md`
- `docs/install.md`
- `docs/project-setup.md`
- optional `docs/development.md`
- `tooling/install_plugin.py`
- `tooling/setup_local.py`
- tests only if existing assertions cover user-facing text or docs layout

## Rollout note

This is a clarity and onboarding improvement, not a behavior change. Existing users can continue to use current commands. Documentation should steer new users toward the recommended path without breaking compatibility.