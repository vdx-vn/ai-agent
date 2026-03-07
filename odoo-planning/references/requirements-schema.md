# Odoo Requirements Schema

Use this reference when converting NotebookLM or plain-text requirements into `requirements.md`.

## Purpose

`requirements.md` should act as both:
1. a human-readable business requirement document
2. a machine-friendly planning payload for Odoo implementation

## Recommended Document Structure

```markdown
# Requirements: <Feature Name>

## Source
- Type: notebooklm | prompt
- Notebook: <name or empty>
- Summary: <summary>

## Business Requirements
- <full normalized requirement list>

## Assumptions
- <assumption>

## Open Questions
- <question>

## JSON Definition
```json
{
  "feature_name": "..."
}
```
```

## Model Definition Guidance

### Model
For each model, capture:
- `model_name`: business-facing model name
- `technical_name`: Odoo technical name such as `x_approval.request`
- `description`: business purpose
- `inherit`: inherited model if any
- `rec_name`: display name field
- `order`: default ordering

### Fields
Recommended Odoo-oriented metadata for each field:
- `field_name`
- `label`
- `data_type`
- `required`
- `readonly`
- `copy`
- `tracking`
- `index`
- `default`
- `compute`
- `store`
- `depends`
- `related`
- `domain`
- `context`
- `help`
- `description`
- `logic`
- `reference_table`
- `ondelete`
- `selection_options`
- `security`

### Buttons
Buttons typically map to form header actions or object/action buttons. Capture:
- `button_name`
- `label`
- `button_type`
- `visible_states`
- `invisible_conditions`
- `groups`
- `logic`

### Tabs
Tabs correspond to Odoo form notebook pages (`<notebook><page ...>`). Capture:
- `tab_name`
- `label`
- `purpose`
- `groups`
- `fields`
- `editable_states`
- `readonly_states`

### Actions
Capture business and technical action behavior:
- create/write/unlink restrictions
- window actions
- server actions
- reports
- cron jobs
- automated state changes

## Odoo Notes

### Common Relational Types
- `many2one`: stores a single related record reference
- `one2many`: inverse collection, must point to inverse field
- `many2many`: many-to-many relation table managed by Odoo

### Common View Coverage
Most business models need:
- form view
- list view
- search view

Optional depending on use case:
- kanban
- activity
- graph
- pivot
- calendar

### Common Action Restrictions
Examples:
- draft only: editable only in `draft`
- submitted/approved: no delete after submission
- only manager group can approve/reject
- record owner can edit before approval but not after

## Quality Checklist

Before finalizing `requirements.md`, verify:
- every model has a purpose
- every field has a type
- every relational field has `reference_table`
- every stateful model has transitions
- every button has visibility logic
- every tab has a purpose
- every restricted action identifies conditions and groups
- assumptions are separated from confirmed requirements
