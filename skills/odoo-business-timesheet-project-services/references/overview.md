# Overview

Paths below are relative to:
- Docs repo: current Odoo documentation repository checkout
- Source repo: current Odoo CE source repository checkout

## Project-local path resolution
Before using docs or source anchors, search upward from the current working directory for `.odoo-skills/project.json`. If it exists, read `docsRoot` as the Odoo docs tree and `sourceRoot` as the Odoo CE source tree. Prefer `.odoo-skills/project.json` over Docker Compose files, module READMEs, or ad hoc filesystem searches. If the config is absent, use the materialized placeholders above or ask for explicit roots.

## Primary routing rule
Use this skill only when the primary business entrypoint is project, task, timesheet, helpdesk, planning, or service delivery.

Set both roots to your local current Odoo and current Odoo CE checkouts. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Explain Odoo service-delivery flows across project, task, timesheet, planning, helpdesk, and sales invoicing links.

## Primary artifact
Service-delivery process map with task, time, billing, and cross-app impacts.

## Key checks
- Identify service entrypoint: project, task, helpdesk, field service, or timesheet.
- Trace time capture to invoicing and analytics.
- Mention sale_project, hr_timesheet, or helpdesk links when relevant.
- Call out approval and billable/non-billable effects.

## Key docs anchors
- `content/applications/services/` (subdirectory; services.rst is a thin toctree stub in v19)
- `content/applications/services/timesheets.rst`
- `content/applications/sales/sales.rst`

## Key source anchors
- `addons/project`
- `addons/hr_timesheet/models/hr_timesheet.py`
- `addons/sale_project`

## Frequent sibling skills
- `odoo-business-sales`
- `odoo-business-hr`
- `odoo-business-accounting`
