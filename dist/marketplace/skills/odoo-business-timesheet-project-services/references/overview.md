# Overview

Paths below are relative to:
- Docs repo: current Odoo documentation repository checkout
- Source repo: current Odoo CE source repository checkout

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
- `content/applications/services.rst`
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
