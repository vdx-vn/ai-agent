# Monitoring & Completion

Detailed monitoring and completion procedures.

## Monitoring Commands

### Epic Thread Messages

```bash
mcp__mcp_agent_mail__search_messages \
  project_key="<path>" \
  query="<epic-id>" \
  limit=20
```

### Urgent Inbox

```bash
mcp__mcp_agent_mail__fetch_inbox \
  project_key="<path>" \
  agent_name="<OrchestratorName>" \
  urgent_only=true \
  include_bodies=true
```

### Bead Status Graph

```bash
bv --robot-triage --graph-root <epic-id> 2>/dev/null | jq '.quick_ref'
```

## Handling Blockers

### Worker Blocked

```bash
mcp__mcp_agent_mail__reply_message \
  project_key="<path>" \
  message_id="<blocker-msg-id>" \
  sender_name="<OrchestratorName>" \
  body_md="Resolution: ..."
```

### File Conflict

```bash
mcp__mcp_agent_mail__send_message \
  to=["<HolderAgent>"] \
  thread_id="<epic-id>" \
  subject="File conflict resolution" \
  body_md="<Worker> needs <files>. Can you release?"
```

## Epic Completion

### Verify All Done

```bash
bv --robot-triage --graph-root <epic-id> 2>/dev/null | jq '.quick_ref.open_count'
# Should be 0
```

### Completion Message

```bash
mcp__mcp_agent_mail__send_message \
  to=["BlueLake", "GreenCastle", "RedStone"] \
  thread_id="<epic-id>" \
  subject="[<epic-id>] EPIC COMPLETE" \
  body_md="..."
```

### Close Epic

```bash
bd close <epic-id> --reason "All tracks complete"
```

## Completion Message Template

```markdown
## Epic Complete: <title>

### Track Summaries
- Track 1 (BlueLake): <summary>
- Track 2 (GreenCastle): <summary>

### Deliverables
- <what was built>

### Learnings
- <key insights>
```
