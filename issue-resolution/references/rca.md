# Root Cause Analysis

Find WHY, not just WHERE.

## RCA Framework

```
Generate hypotheses (3-5)
    │
    ▼
Gather evidence for/against
    │
    ▼
Eliminate hypotheses
    │
    ▼
Confirm root cause
```

## Bug Type → Strategy

| Type | Strategy | Tools |
|------|----------|-------|
| Regression | Find breaking change | git bisect, blame |
| Edge case | Analyze boundaries | Type inspection |
| Race condition | Trace async | Timing logs |
| Data corruption | Trace state | Data flow |
| External dep | Check versions | Changelogs |

## Oracle Prompts

**Hypothesis Generation:**
```
oracle(
  task: "Generate root cause hypotheses",
  context: """
    Symptom: <error>
    Code path: <trace>
    Recent changes: <git log>

    Generate 3-5 hypotheses ranked by likelihood.
    What evidence would support/refute each?
  """
)
```

**Validation:**
```
oracle(
  task: "Validate hypothesis",
  context: """
    Hypothesis: <proposed cause>
    Evidence: <gathered>

    1. Does evidence support/refute?
    2. Explain causal chain
    3. What would confirm?
  """
)
```

## RCA → Repro Loop

```
IN RCA: "Need timing logs"
    │
    ▼
BACK TO REPRO:
• Add instrumentation
• Run with conditions
• Capture evidence
    │
    ▼
RETURN TO RCA
```

## RCA Report Template

```markdown
# RCA: <Issue>

## Iteration: N

## Hypotheses

### Hypothesis A: <Description>
- **Likelihood**: HIGH/MEDIUM/LOW
- **Supporting**: ...
- **Refuting**: ...
- **Verdict**: ✓ CONFIRMED / ✗ ELIMINATED

## Root Cause (Confirmed)

**Cause**: <Clear statement>

**Causal chain**:
1. <Step> →
2. <Step> →
3. <Symptom>

## Why This Happened
<Underlying reason>

## Fix Approach
- **Immediate**: <change>
- **Preventive**: <prevention>
```
