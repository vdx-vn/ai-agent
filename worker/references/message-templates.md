# Worker Message Templates

Agent Mail message formats for bead execution.

## Bead Complete → Orchestrator

```bash
mcp__mcp_agent_mail__send_message \
  to=["<OrchestratorName>"] \
  thread_id="<epic-id>" \
  subject="[<bead-id>] COMPLETE"
```

```markdown
## Completed: <bead-id>

### What Was Done
- <bullet points>

### Files Modified
- <file list>

### Next Bead
- <next-bead-id>: <brief plan>

### Track Progress
- Completed: X/Y beads
```

---

## Save Context → Self (Track Thread)

```bash
mcp__mcp_agent_mail__send_message \
  to=["<AgentName>"] \
  thread_id="track:<AgentName>:<epic-id>" \
  subject="<bead-id> Complete - Context for Next"
```

```markdown
## Bead Complete: <bead-id>

### Key Changes
- <what was implemented>

### Learnings
- <patterns discovered>

### Gotchas
- <things to watch out for>

### For Next Bead (<next-bead-id>)
- <recommendations>

### Files to Reference
- <key files for next bead>
```

---

## Report Blocker → Orchestrator

```bash
mcp__mcp_agent_mail__send_message \
  to=["<OrchestratorName>"] \
  thread_id="<epic-id>" \
  subject="[<bead-id>] BLOCKED: <reason>" \
  importance="high" \
  ack_required=true
```

```markdown
Blocked by: <explanation>

Need: <what you need to proceed>
```

---

## Interface Change → Other Workers

```bash
mcp__mcp_agent_mail__send_message \
  to=["<Worker1>", "<Worker2>"] \
  thread_id="<epic-id>" \
  subject="[<bead-id>] Interface Change: <what>" \
  importance="high"
```

```markdown
Changed <interface> from X to Y.

Update your code accordingly.
```

---

## Track Complete → Orchestrator

```bash
mcp__mcp_agent_mail__send_message \
  to=["<OrchestratorName>"] \
  thread_id="<epic-id>" \
  subject="[Track N] COMPLETE"
```

```markdown
## Track N Complete

### Beads Completed
- <bead-1>: <summary>
- <bead-2>: <summary>

### Track Summary
- <overall accomplishment>

### Key Learnings
- <insights for future>

### Files Modified
- <comprehensive list>
```
