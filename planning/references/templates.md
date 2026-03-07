# Planning Templates

Copy-paste templates. See `examples.md` for worked examples.

## Discovery Report

```markdown
# Discovery: <Feature>

## Feature Summary
<1-2 sentences>

## Architecture Snapshot
| Package | Purpose | Key Files |
|---------|---------|-----------|
| ...     | ...     | ...       |

## Existing Patterns
| Feature | Location | Pattern |
|---------|----------|---------|
| ...     | ...      | ...     |

## Technical Constraints
- Node: >=18
- Key deps: ...

## Open Questions
- [ ] ...
```

## Approach Document

```markdown
# Approach: <Feature>

## Gap Analysis
| Component | Have | Need | Gap |
|-----------|------|------|-----|

## Recommended Approach
<Description>

## Risk Map
| Component | Risk | Verification |
|-----------|------|--------------|
| ...       | HIGH | Spike        |

## Spike Requirements
1. Spike: <question> - 30 min
```

## Spike Bead

```markdown
# Spike: <Question>

Type: spike | Priority: 0 | Time-box: 30 min
Output: .spikes/<feature>/<id>/

## Question
Can we <specific question>?

## Success Criteria
- [ ] Working code
- [ ] Answer: YES/NO

## On Completion
br close <id> --reason "YES: <approach>"
```

## Feature Bead with Learnings

```markdown
# <Action Title>

Type: task | Priority: <0-4> | Depends on: br-X

## Learnings from Spikes
> From br-<id>:
> - <learning 1>

## Requirements
<What to implement>

## Acceptance Criteria
- [ ] <criterion 1>
- [ ] Passes type-check, build

## File Scope
- packages/domain/src/...
```

## Execution Plan

```markdown
# Execution Plan: <Feature>

## Tracks
| Track | Agent    | Beads         | File Scope     |
|-------|----------|---------------|----------------|
| 1     | BlueLake | br-10 → br-11 | packages/sdk/**|

## Cross-Track Dependencies
- Track 2 starts after br-11

## Key Learnings
- <learning 1>
```


