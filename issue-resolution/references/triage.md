# Triage Phase

Normalize different input types to Issue Brief.

## Input Types

| Type | Strategy |
|------|----------|
| Vague report | Clarify → Explore → Reproduce |
| Stack trace | Parse → Locate → Reproduce |
| Failing test | Run → Extract → Trace |

## Vague Report Triage

```
"Login is broken"
    │
    ▼
Ask:
• What error?
• When did it start?
• What triggers it?
• Specific user/env?
    │
    ▼ (if unclear)
Explore:
• search_codebase_definitions for auth
• git log recent changes
• Check logs
```

## Stack Trace Triage

```
Parse trace:
• Extract file:line
• get_definition on functions
• Read context
    │
    ▼
Identify repro:
• What input caused this?
• Can we write a test?
```

## Failing Test Triage

```bash
bun test <file> --filter "<test>"
# Read test for setup/assertions
# git log: was it passing before?
```

## Severity Classification

| Severity | Repro Required |
|----------|----------------|
| CRITICAL (prod, security) | Test REQUIRED |
| REGRESSION | Test REQUIRED |
| RACE CONDITION | Test REQUIRED |
| LOGIC BUG | Test PREFERRED |
| UI/VISUAL | Manual + screenshot OK |
| QUICK FIX | Manual OK |

## Issue Brief Template

```markdown
# Issue Brief: <Title>

**Severity**: CRITICAL / HIGH / MEDIUM / LOW
**Type**: Regression / Edge case / Race / UI / Performance
**Repro Required**: Test / Manual OK

## Symptom
<What is happening>

## Expected
<What should happen>

## Reproduction
<Steps or test command>

## Evidence
<Error, stack trace, output>

## Affected Area
<Files, modules>

## Timeline
<When started, recent changes>
```
