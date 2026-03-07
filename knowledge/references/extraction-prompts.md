# Extraction Prompt Templates

## Task Agent Prompt

```
Read these threads using read_thread with goal 'Extract topics, decisions, and changes'.

Threads: [T-xxx, T-yyy, T-zzz]

Return JSON only:
{
  "topics": [
    {
      "name": "short topic name",
      "threads": ["T-xxx"],
      "summary": "1-2 sentences",
      "decisions": ["decision made"],
      "patterns": ["pattern established"],
      "changes": ["what changed"]
    }
  ]
}

Be precise. Only extract what's explicitly discussed.
```

## Oracle Synthesis Prompt

```
Cluster these extractions into unified topics.
Deduplicate. Resolve conflicts (latest thread wins).
Output consolidated topic list with source threads.

Extractions:
[paste Task outputs]
```

## Oracle Reconciliation Prompt

```
Compare:
1. TOPICS: [extracted knowledge]
2. CODE: [verified state with file paths]
3. DOCS: [current documentation content]

Identify:
- GAPS: Knowledge in topics not in docs
- STALE: Docs that contradict current code
- CONFLICTS: Topics vs docs disagreements

Output JSON:
{
  "gaps": [{"topic": "...", "target_file": "..."}],
  "stale": [{"file": "...", "issue": "..."}],
  "updates": [
    {
      "file": "path/to/doc.md",
      "action": "add|update|remove",
      "section": "section name",
      "content": "what to write"
    }
  ]
}
```

## read_thread Goal Templates

### Architecture
```
Extract architectural decisions, patterns established,
design rationale, and trade-offs. Include file paths.
```

### Feature
```
Extract feature requirements, implementation approach,
API surface, usage examples, and configuration options.
```

### Refactor
```
Extract what was refactored, motivation, approach,
pattern changes, and migration guidance.
```

### Bug Fix
```
Extract bug description, root cause, fix approach,
and patterns to prevent recurrence.
```
