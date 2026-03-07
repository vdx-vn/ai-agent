---
name: odoo-knowledge
description: Odoo Librarian - search documentation and codebase for context. Use for Odoo dev tasks, patterns, framework concepts, module examples.
version: 1.0.0
---

# Odoo Knowledge Librarian

Specialized Librarian for searching Odoo 18.0 documentation and codebase.

## Sources

| Source | URL |
|--------|-----|
| Documentation | https://github.com/odoo/documentation/tree/18.0 |
| Codebase | https://github.com/odoo/odoo/tree/18.0 |

## When to Use

- Odoo development tasks
- Understanding framework concepts
- Finding module patterns
- Debugging with official reference

## Pipeline

```
REQUEST → IDENTIFY → LOCAL REF → ONLINE SEARCH → RESPOND
```

## Quick Reference Map

| Topic | Reference File |
|-------|----------------|
| ORM, fields, models | `references/orm-patterns.md` |
| @api decorators | `references/api-decorators.md` |
| Views (form, tree, kanban) | `references/view-examples.md` |
| Security (ACL, rules) | `references/security-guide.md` |
| Module structure | `references/module-structure.md` |
| Controllers, HTTP | `references/controllers-web.md` |
| OWL, frontend | `references/owl-frontend.md` |
| Cron, automation | `references/automation-workflow.md` |
| QWeb, reports | `references/qweb-reports.md` |
| Testing | `references/testing.md` |
| Sale module | `references/sale-module.md` |
| Accounting, invoices | `references/accounting-invoice.md` |
| Stock, inventory | `references/stock-inventory.md` |

## Search Strategy

### 1. Check Local References

```bash
Read references/<topic>.md
```

### 2. Online Search (if local insufficient)

**Documentation**:
```bash
WebSearch "site:odoo.com/documentation/18.0 <query>"
```

**Codebase**:
```bash
WebSearch "repo:odoo/odoo extension:py <query>"
```

### 3. NotebookLM (Optional)

For persistent knowledge storage, use NotebookLM MCP.

## Common Query Types

| Query | Search Location |
|-------|-----------------|
| ORM patterns | Docs → Reference → ORM; Codebase → odoo/fields.py |
| View inheritance | Docs → Views; Codebase → addons/*/views/*.xml |
| Model methods | Docs → ORM; Codebase → odoo/models.py |
| Security | Docs → Security; Codebase → addons/base/security/ |
| API decorators | Docs → API; Codebase → odoo/api/ |

## Return Format

```markdown
## Answer
<explanation>

## Code Example
```python
<code>
```

## References
- Docs: https://www.odoo.com/documentation/18.0/<path>
- Code: https://github.com/odoo/odoo/blob/18.0/<path>
```

## References

All detailed guides in `references/`:
- Core: orm-patterns, api-decorators, security-guide, module-structure, view-examples
- Web: controllers-web, owl-frontend
- Automation: automation-workflow, qweb-reports, testing
- Business: sale-module, accounting-invoice, stock-inventory
