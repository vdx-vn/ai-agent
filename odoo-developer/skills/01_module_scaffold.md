# Skill: Odoo Module Scaffold

## Goal
Generate a clean Odoo module skeleton with proper manifest and structure.

## Output
- addon folder structure
- __manifest__.py
- init files
- security placeholders
- basic views/action/menu placeholders

## Structure
my_module/
  __init__.py
  __manifest__.py
  models/
    __init__.py
    my_model.py
  views/
    my_model_views.xml
  security/
    ir.model.access.csv
    security.xml (optional)
  data/
    sequence.xml (optional)

## Manifest Rules
- Use correct depends list
- Include data files in order: security then views then data
- Set application/category if app module

## Guardrails
- Don't forget `installable: True`
- Keep version consistent with Odoo major version

## Example Prompt
"Create a module to manage internal approvals with a model approval.request and basic menu."
