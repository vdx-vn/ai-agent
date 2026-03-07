# UI Component Workflow

shadcn/ui component discovery and installation.

## Search Components

```bash
mcp__shadcn__search_items_in_registries \
  registries=["@shadcn"] \
  query="<component>"
```

## View Component Details

```bash
mcp__shadcn__view_items_in_registries \
  items=["@shadcn/<component>"]
```

## Get Usage Examples

```bash
mcp__shadcn__get_item_examples_from_registries \
  registries=["@shadcn"] \
  query="<component>-demo"
```

## Install Component

```bash
mcp__shadcn__get_add_command_for_items \
  items=["@shadcn/<component>"]
```

Then run returned command:
```bash
npx shadcn@latest add button
```

## Verify Installation

```bash
mcp__shadcn__get_audit_checklist \
  reason="Verify <component> installation"
```

## Common Components

| Component | Search Query |
|-----------|--------------|
| Button | `button` |
| Dialog | `dialog` |
| Form | `form` |
| Table | `table` |
| Toast | `toast` |
| Dropdown | `dropdown-menu` |
| Select | `select` |
| Input | `input` |
| Card | `card` |
| Tabs | `tabs` |
