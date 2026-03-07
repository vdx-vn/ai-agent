---
name: odoo-planning
description: Odoo feature planning pipeline with NotebookLM requirement extraction, structured requirements normalization, and Odoo model/view/action design. Use when planning Odoo modules, models, views, workflows, or turning business requirements into implementation-ready specifications.
version: 0.1.0
---

# Odoo Planning Pipeline

Copies the core `planning` workflow but adds a requirement-ingestion stage for Odoo work.


## Primary Goal

Turn either:
1. a plain user prompt, or
2. a named NotebookLM notebook containing requirements

into:
- a normalized `requirements.md` document
- an Odoo-aware solution design
- an implementation-ready planning package

## Entry Decision

Before planning, determine which input path applies.

```text
User mentions a NotebookLM notebook by name?
├── YES → Load `notebooklm-project` and fetch the full requirement set from that notebook
└── NO  → Use the user prompt as the initial requirement source
```

### Notebook Detection Rules

Treat it as a notebook-directed request when the user explicitly provides a notebook name or clearly says the requirements are stored in NotebookLM.

Examples:
- "Plan this from notebook Sales Approval Flow"
- "Use NotebookLM notebook Odoo HR Spec"
- "Lấy requirement từ notebooklm tên Purchase Custom"

If the notebook name is ambiguous, clarify before continuing.

## Phase 0: Requirement Ingestion

### Path A: NotebookLM Source

If the user provided a NotebookLM notebook name:
1. Load the `notebooklm-project` skill
2. Locate the notebook
3. Query it for the complete requirement set
4. Extract all functional rules, entities, fields, states, buttons, tabs, permissions, validations, reports, and integrations
5. Consolidate the result into `requirements.md`

Recommended NotebookLM query goals:
- Summarize all business requirements without dropping detail
- List every model, field, workflow state, user action, permission, and validation rule
- Separate explicit requirements from assumptions
- Preserve source wording when the requirement is sensitive or ambiguous

### Path B: Plain Prompt Source

If the user did not provide a notebook name:
1. Restate the request
2. Expand the requirement set from the prompt only
3. Identify missing business details
4. Record assumptions explicitly in `requirements.md`

## Required Output: `requirements.md`

After Phase 0, always create `requirements.md` containing:
1. full normalized requirement text
2. a JSON definition block for implementation planning
3. explicit assumptions and open questions

The JSON must be implementation-oriented, not just a summary.

## Requirements JSON Structure

Use this shape as the baseline and extend it when needed for Odoo.

```json
{
  "feature_name": "string",
  "source": {
    "type": "notebooklm|prompt",
    "notebook_name": "string",
    "summary": "string"
  },
  "models": [
    {
      "model_name": "x_model_name",
      "technical_name": "x_module.model",
      "description": "string",
      "inherit": "string",
      "rec_name": "string",
      "order": "string",
      "fields": [
        {
          "field_name": "string",
          "label": "string",
          "data_type": "char|text|html|integer|float|monetary|boolean|date|datetime|selection|many2one|one2many|many2many|binary|json|reference",
          "required": true,
          "readonly": false,
          "copy": true,
          "tracking": false,
          "index": false,
          "default": "string",
          "compute": "string",
          "store": false,
          "depends": ["field_a", "field_b"],
          "related": "string",
          "domain": "string",
          "context": "string",
          "help": "string",
          "description": "string",
          "logic": "define field behavior, validation, and lifecycle logic here",
          "reference_table": "target model for relational fields, else empty",
          "ondelete": "restrict|cascade|set null|set default|",
          "selection_options": [
            { "value": "draft", "label": "Draft" }
          ],
          "security": {
            "groups": ["base.group_user"],
            "editable_states": ["draft"],
            "readonly_states": ["approved"]
          }
        }
      ],
      "buttons": [
        {
          "button_name": "action_submit",
          "label": "Submit",
          "button_type": "object|action",
          "context": "string",
          "domain": "string",
          "visible_states": ["draft"],
          "invisible_conditions": ["state != 'draft'"],
          "groups": ["base.group_user"],
          "logic": "what the button does, validations, and side effects"
        }
      ],
      "tabs": [
        {
          "tab_name": "details",
          "label": "Details",
          "purpose": "business purpose of the notebook/page in the form view",
          "groups": ["base.group_user"],
          "fields": ["name", "partner_id"],
          "editable_states": ["draft"],
          "readonly_states": ["approved"]
        }
      ],
      "actions": [
        {
          "action_type": "create|write|unlink|server_action|window_action|report|cron",
          "name": "string",
          "trigger": "manual|state_change|scheduled|automated",
          "conditions": ["if model is in state in_approve_process, user cannot edit"],
          "logic": "business rule and expected behavior",
          "security": {
            "groups": ["base.group_user"],
            "record_rule_notes": "string"
          }
        }
      ],
      "states": [
        {
          "value": "draft",
          "label": "Draft",
          "transitions": ["submitted"],
          "entry_logic": "string",
          "exit_logic": "string"
        }
      ],
      "views": {
        "form": true,
        "list": true,
        "search": true,
        "kanban": false,
        "activity": false,
        "graph": false,
        "pivot": false,
        "calendar": false
      },
      "security": {
        "access_rights": [
          {
            "group": "base.group_user",
            "read": true,
            "write": true,
            "create": true,
            "unlink": false
          }
        ],
        "record_rules": [
          {
            "name": "Own documents only",
            "domain": "[('user_id', '=', user.id)]"
          }
        ]
      }
    }
  ],
  "reports": [],
  "menus": [],
  "open_questions": [],
  "assumptions": []
}
```

## Odoo-Specific Planning Rules

Use `odoo-knowledge` whenever requirements mention Odoo concepts that need confirmation:
- model field types
- relational field behavior
- computed/inverse/related fields
- state/statusbar behavior
- form/list/search/kanban views
- notebook tabs (`<notebook><page .../>`)
- ACLs, record rules, groups
- actions, server actions, reports, cron, chatter

### Odoo Design Expectations

For each model, define at minimum:
- business purpose
- field list
- relational mapping
- states/status flow if applicable
- form view layout
- list/search views if users need navigation/filtering
- buttons and server-side logic
- create/write/unlink restrictions
- security groups and record rules

## Planning Phases

## Phase 1: Discovery

Launch parallel exploration:
- Existing Odoo modules and naming patterns
- Similar business workflows already in the codebase
- Manifest, dependencies, security, and XML structure constraints
- Official Odoo references when field/view semantics need confirmation

Save to `history/<feature>/discovery.md`.

## Phase 2: Synthesis

Produce:
- gap analysis between requirements and existing modules
- risk map
- target model/view/security architecture
- requirement-to-implementation mapping

Save to `history/<feature>/approach.md`.

Risk guide:
- LOW: direct reuse of existing model/view patterns
- MEDIUM: variation of existing workflow or views
- HIGH: new approval engine, security-sensitive rules, external integration, accounting/stock side effects

## Phase 3: Verification

For HIGH risk items, define verification tasks in the plan:
- approval-state transitions
- computed monetary logic
- access rights and record rules
- XML inheritance strategy
- external API synchronization

Time-box each verification item and capture expected output in the plan.

## Phase 4: Decomposition

Break the implementation plan into concrete work packages.

Prefer decomposition by Odoo layer:
- models
- business methods
- security
- views
- menus/actions
- data/demo/sequence
- reports
- tests

For each work package, include:
- scope
- affected files or directories
- prerequisites
- risks
- validation approach

## Phase 5: Plan Validation

Validate that each planned model has:
- required fields defined
- view coverage defined
- button/state rules defined
- ACL/record-rule considerations defined
- assumptions separated from confirmed requirements

## Phase 6: Execution Order

Produce an execution order showing:
- what should be built first
- which items can run in parallel
- which steps depend on prior model, security, or view work

Save to `history/<feature>/execution-plan.md`.

## Tool Selection

| Need | Tool |
|------|------|
| Notebook requirement retrieval | `notebooklm-project` skill + NotebookLM MCP |
| Odoo semantics and examples | `odoo-knowledge` skill |
| Codebase structure | Glob + Grep + Read |
| Requirement normalization | `requirements.md` + `references/requirements-schema.md` |

## Common Mistakes

- Planning from a vague prompt without normalizing requirements first
- Missing `requirements.md`
- Defining fields without field type semantics
- Forgetting notebook tabs/pages in form views
- Omitting button visibility or state restrictions
- Omitting ACL and record-rule implications
- Mixing assumptions with confirmed requirements

## References

- `references/requirements-schema.md` - Odoo requirements structure and field definitions
- `references/templates.md` - Odoo discovery, approach, work package, and execution templates
- `references/examples.md` - Odoo planning examples
- `../odoo-knowledge/references/orm-patterns.md` - Odoo ORM and field patterns
- `../odoo-knowledge/references/view-examples.md` - Odoo form/list/search/notebook patterns
