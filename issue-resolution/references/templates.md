# Report Templates

All templates for issue resolution documentation.

## Repro Report

```markdown
# Reproduction: <Issue>

## Method
☐ Test: `<command>`
☐ Manual: <steps>

## Error Captured
<Exact error/trace>

## Code Path
1. Entry: `<file>:<line>` - <fn>
2. Calls: `<file>:<line>` - <fn>
3. Fails: `<file>:<line>` - <reason>

## Recent Changes
- <commit>: <summary>
```

## Impact Report

```markdown
# Impact: <Issue>

## Blast Radius

### Direct
- <File/function changed>

### Callers
- <From get_references>

### Related
- <Similar patterns>

## Regression Risk
**Level**: HIGH/MEDIUM/LOW
**Reason**: <why>

## Test Coverage
- Existing: <list>
- To add: <list>

## Validation
☐ Spike done: `.spikes/<id>/`
☐ Approach validated
```

## Fix Bead

```markdown
# Fix: <Issue>

**Type**: bug | **Priority**: 0-4 | **Fixes**: <issue>

## Root Cause
<From RCA>

## Fix Implementation
<What to change>

## Files
- `<file>`: <change>

## Acceptance Criteria
- [ ] Regression test passes
- [ ] Original symptom gone
- [ ] No new failures
- [ ] check-types passes
- [ ] build passes
```
