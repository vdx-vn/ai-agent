# Doc Mapping Conventions

Target file conventions for documentation updates.

## Common Target Files

| File | Purpose | When to Update |
|------|---------|----------------|
| `AGENTS.md` | Project context, tool prefs | After tooling/workflow changes |
| `docs/ARCHITECTURE.md` | System design | After structural changes |
| `docs/API.md` | API documentation | After API changes |
| `docs/SETUP.md` | Setup instructions | After config changes |
| `.claude/skills/*/SKILL.md` | Skill instructions | After skill updates |

## Structure Discovery

```bash
# Get overview
mcp__gkg__repo_map on docs/, .claude/skills/

# Find existing mentions
Grep "topic keyword" docs/ AGENTS.md
```

## Update Principles

1. **Read first** - Understand existing structure
2. **Match voice** - Follow existing style
3. **Surgical changes** - Don't rewrite wholesale
4. **Preserve context** - Don't remove relevant info
5. **Add citations** - Link to source files

## Mermaid Diagrams with Citations

```json
{
  "code": "flowchart LR\n  A[Client] --> B[RetryPolicy]",
  "citations": {
    "Client": "file:///src/api/client.ts#L10",
    "RetryPolicy": "file:///src/api/retry.ts#L45"
  }
}
```

## Section Insertion Points

Look for existing markers:
- `## Related Topics`
- `## See Also`
- `<!-- ADD NEW HERE -->`

If none exist, add after most related section.
