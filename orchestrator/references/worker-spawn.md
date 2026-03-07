# Worker Spawn Template

Use when spawning workers via Task tool.

## Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{AGENT_NAME}` | Worker identity | `BlueLake` |
| `{TRACK_NUMBER}` | Track number | `1` |
| `{EPIC_ID}` | Epic bead ID | `bd-42` |
| `{BEAD_LIST}` | Comma-separated beads | `bd-43, bd-44` |
| `{FILE_SCOPE}` | Glob for reservation | `packages/sdk/**` |
| `{PROJECT_PATH}` | Absolute path | `/Users/dev/myproject` |

## Full Template

```
You are agent {AGENT_NAME} working on Track {TRACK_NUMBER} of epic {EPIC_ID}.

## Setup
1. Read {PROJECT_PATH}/AGENTS.md for tool preferences
2. Load the worker skill

## Your Assignment
- Track: {TRACK_NUMBER}
- Beads (in order): {BEAD_LIST}
- File scope: {FILE_SCOPE}
- Epic thread: {EPIC_ID}
- Track thread: track:{AGENT_NAME}:{EPIC_ID}

## Protocol for EACH bead:

### START BEAD
1. mcp__mcp_agent_mail__register_agent (name="{AGENT_NAME}")
2. mcp__mcp_agent_mail__summarize_thread (thread_id="track:{AGENT_NAME}:{EPIC_ID}")
3. mcp__mcp_agent_mail__file_reservation_paths (paths=["{FILE_SCOPE}"], reason="{BEAD_ID}")
4. bd update {BEAD_ID} --status in_progress

### WORK
- Implement bead requirements using preferred tools
- Check inbox periodically

### COMPLETE BEAD
1. bd close {BEAD_ID} --reason "summary"
2. mcp__mcp_agent_mail__send_message to orchestrator: "[{BEAD_ID}] COMPLETE"
3. mcp__mcp_agent_mail__send_message to self: context for next bead
4. mcp__mcp_agent_mail__release_file_reservations

### NEXT BEAD
- Read track thread for context
- Continue with next bead

## When Track Complete
- mcp__mcp_agent_mail__send_message to orchestrator: "[Track {N}] COMPLETE"
- Return summary of all work

## Important
- ALWAYS read track thread before starting each bead
- ALWAYS write context after completing each bead
- Report blockers immediately
```

## Minimal Template (Experienced Workers)

```
Agent: {AGENT_NAME} | Track: {N} | Epic: {EPIC_ID}
Beads: {BEAD_LIST} | Scope: {FILE_SCOPE}

Load worker skill. For each bead:
1. summarize_thread → reserve → claim
2. implement → check inbox
3. close → report → save context → release
4. loop to next

Track done → report "[Track N] COMPLETE"
```
