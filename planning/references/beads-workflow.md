# Beads Workflow Integration

Detailed guide for planning with Beads CLI (`br`, `bv`).

## Prerequisites

```bash
br --version && bv --version
```

## Discovery Phase

### Parallel Exploration

```
Task() → Agent A: Architecture (Glob, Read key files)
Task() → Agent B: Existing patterns (Grep)
Task() → Agent C: Constraints (package.json)
```

### Discovery Output

Save to `history/<feature>/discovery.md`:

```markdown
# Discovery: <Feature>

## Architecture
- Relevant packages: ...
- Entry points: ...

## Patterns
- Similar: <file> uses <pattern>

## Constraints
- Node version: ...

## Open Questions
- [ ] ...
```

## Synthesis Phase

### Gap Analysis

| Component | Have | Need | Gap |
|-----------|------|------|-----|
| Entity    | User | Invoice | New |

### Risk Classification

```
Pattern exists? ─── YES → LOW
                  └── NO → MEDIUM+

External dep? ─── YES → HIGH
Blast radius >5 files? ─── YES → HIGH
```

## Spike Phase (HIGH Risk Only)

### Create Spike Beads

```bash
br create "Spike: <question>" -t epic -p 0
br create "Spike: Test X" -t task --blocks <spike-epic>
```

### Spike Template

```markdown
# Spike: <question>

Time-box: 30 min
Output: .spikes/<feature>/<id>/

## Question
Can we <specific question>?

## Success Criteria
- [ ] Working throwaway code
- [ ] Answer documented

## On Completion
br close <id> --reason "YES: <approach>"
```

### Execute Spikes

```bash
bv --robot-plan  # Parallelize
```

## Decomposition Phase

### Create Beads

```bash
br create "Epic: <Feature>" -t epic -p 1
br create "Create <Entity>" -t task --blocks <epic>
br create "Implement <Repo>" -t task --blocks <epic> --deps <domain-bead>
```

### Embed Learnings

```markdown
# Implement X

## Learnings from Spike br-12
> - Must use raw body for signature
> - See .spikes/billing/webhook-test/

## Acceptance Criteria
- [ ] Endpoint at /api/x
```

## Validation Phase

```bash
bv --robot-suggest   # Missing deps
bv --robot-insights  # Cycles
br dep add/remove    # Fix issues
```

## Track Planning Phase

```bash
bv --robot-plan | jq '.plan.tracks'
```

### Validation

```bash
bv --robot-insights | jq '.Cycles'  # No cycles
bv --robot-plan | jq '.plan.unassigned'  # All assigned
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `br create/show/close` | Bead lifecycle |
| `br dep add/remove` | Dependencies |
| `bv --robot-plan` | Parallel tracks |
| `bv --robot-suggest/insights` | Validation |

Full templates: `references/templates.md`
