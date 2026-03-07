# Odoo Planning Templates

Copy-paste templates for Odoo requirement normalization and planning.

## Requirements Document

```markdown
# Requirements: <Feature Name>

## Source
- Type: notebooklm | prompt
- Notebook: <name or empty>
- Summary: <short summary>

## Business Requirements
- <normalized requirement 1>
- <normalized requirement 2>

## Models
### <Model Name>
- Purpose: <business purpose>
- Main fields: <field list>
- Workflow states: <states if any>
- Buttons: <button list>
- Tabs: <tab list>
- Security: <groups, ACL, record rules>

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

## Discovery Report

```markdown
# Discovery: <Feature>

## Feature Summary
<1-2 sentences>

## Relevant Modules
| Module | Purpose | Key Files |
|--------|---------|-----------|
| ...    | ...     | ...       |

## Existing Patterns
| Feature | Location | Pattern |
|---------|----------|---------|
| ...     | ...      | ...     |

## Odoo Constraints
- Module dependencies: ...
- Security constraints: ...
- View inheritance constraints: ...

## Open Questions
- [ ] ...
```

## Approach Document

```markdown
# Approach: <Feature>

## Requirement Summary
- <key requirement>

## Gap Analysis
| Component | Have | Need | Gap |
|-----------|------|------|-----|

## Target Design
### Models
- <model>: <purpose>

### Views
- Form: <summary>
- List/Search: <summary>
- Notebook tabs: <summary>

### Security
- ACL: <summary>
- Record rules: <summary>

## Risk Map
| Component | Risk | Verification |
|-----------|------|--------------|
| ...       | HIGH | Prototype/check docs |
```

## Work Package Template

```markdown
# Work Package: <Title>

## Scope
<what this package covers>

## Affected Areas
- models/
- views/
- security/

## Dependencies
- <dependency>

## Risks
- <risk>

## Validation
- <how to verify>
```

## Execution Plan

```markdown
# Execution Plan: <Feature>

## Order
1. <first item>
2. <second item>
3. <third item>

## Parallel Candidates
- <item A>
- <item B>

## Dependency Notes
- Views depend on model fields existing
- Record rules depend on final ownership logic
- Reports depend on final model schema

## Key Risks
- <risk>
```
