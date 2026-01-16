---
name: odoo-developer
description: Odoo development pack: module analysis, scaffold, ORM/models, views/actions, security, workflows, integrations, migrations, testing, performance, debugging, docker ops, SQL reporting.
version: 0.1.0
---

# Odoo Developer (Global Skill)

## When to activate
Use this skill for any Odoo addon work: analyzing an existing module, implementing a feature, debugging, refactor, migration, security, performance.

## How to work
When user asks to analyze a module (e.g. vdx_manage_promo), do this:

1) Locate addon root (manifest, init, dependencies)
2) List structure:
   - models/, views/, security/, data/, wizards/, report/, static/
3) Read __manifest__.py:
   - name, depends, data order, external deps
4) Map functionality:
   - models: key business objects + fields + overrides
   - workflows: state machine + action methods
   - views/actions/menus: UI entry points
   - security: ACL + record rules coverage
   - cron/server actions: automation + safe_eval
5) Find risks:
   - security holes (missing ACL/rules)
   - ORM smells (N+1, search in loops, sudo abuse)
   - upgrade risks (hardcoded ids, fragile xpath)
   - performance hotspots (stored computes, read_group missing)
6) Output:
   - Module summary (what it does)
   - File map (what to read first)
   - Issues + fixes (patch suggestions)
   - Verify commands (update module + key flows)

## Local reference files
You may load and follow the detailed checklists from:
- ./skills/00_odoo_core.md
- ./skills/01_module_scaffold.md
- ./skills/02_models_orm.md
- ./skills/03_views_actions.md
- ./skills/04_security_access.md
- ./skills/05_workflows.md
- ./skills/06_api_integration.md
- ./skills/07_migrations.md
- ./skills/08_testing.md
- ./skills/09_performance.md
- ./skills/10_debugging.md
- ./skills/11_docker_ops.md
- ./skills/12_sql_reporting.md
- ./skills/13_best_practices.md
EOF
