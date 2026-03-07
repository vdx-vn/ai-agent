# Search Strategy

## Local References First

Check these files before online search:

```python
REFERENCE_MAP = {
    'orm': 'orm-patterns.md',
    'field': 'orm-patterns.md',
    'computed': 'orm-patterns.md',
    'api': 'api-decorators.md',
    '@api': 'api-decorators.md',
    'view': 'view-examples.md',
    'form': 'view-examples.md',
    'xpath': 'view-examples.md',
    'security': 'security-guide.md',
    'acl': 'security-guide.md',
    'manifest': 'module-structure.md',
    'controller': 'controllers-web.md',
    'http': 'controllers-web.md',
    'owl': 'owl-frontend.md',
    'javascript': 'owl-frontend.md',
    'cron': 'automation-workflow.md',
    'workflow': 'automation-workflow.md',
    'qweb': 'qweb-reports.md',
    'report': 'qweb-reports.md',
    'test': 'testing.md',
    'sale': 'sale-module.md',
    'invoice': 'accounting-invoice.md',
    'account': 'accounting-invoice.md',
    'stock': 'stock-inventory.md',
    'picking': 'stock-inventory.md',
}
```

## Online Search

When local refs don't contain answer:

**Documentation**:
```bash
WebSearch "site:odoo.com/documentation/18.0 [query]"
WebReader <url>
```

**Codebase**:
```bash
WebSearch "repo:odoo/odoo extension:py [query]"
```

## Return Format

```markdown
## Answer
[Explanation]

## Code Example
```python
[code from core modules]
```

## References
- Docs: https://www.odoo.com/documentation/18.0/[path]
- Code: https://github.com/odoo/odoo/blob/18.0/[path]
```
