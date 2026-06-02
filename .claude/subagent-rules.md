# Subagent Delegation Rules

  Always delegate to subagents for data-heavy or output-heavy operations
  to protect main context. Return only distilled results to the main agent.

## Delegate to subagents when

- Reading structured files — xlsx, csv, json, logs
- Running scripts / tests — verbose output (pytest, ruff, unit tests)
- Git history / blame — long log output is rarely needed verbatim
- Multi-file exploration — use Explore subagent for open-ended searches
- Writing large artifacts — spec docs, markdown reports, boilerplate code
- Web search + summarization — raw HTML/page content is massive
- Validation loops — linting, Docker builds, Odoo module install/update logs
- Code review passes — spawn code-reviewer or security-reviewer
- Trial-and-error iteration — isolate retry loops, get back only the outcome
- Parallel independent queries — spawn multiple subagents simultaneously

## When NOT to delegate

- Single quick lookups: one grep, one Read on a known path — do inline
- Operations where you need the raw output to reason about next steps

## Model to use

  DEFAULT subagent model = haiku, enforced globally via
  CLAUDE_CODE_SUBAGENT_MODEL=claude-haiku-4-5-20251001 in ~/.claude/settings.json.
  Do NOT pass model: "opus"/"sonnet" unless the task is complex reasoning or
  code generation that genuinely needs it. Every Opus subagent multiplies cost.

  Escalation is opt-in, not default:
  - search / grep / read / format / log-scan / summarize → haiku (default)
  - complex reasoning, architecture, code generation → sonnet
  - opus subagent → almost never; justify before spawning

## General rule of thumb
  >
  > If raw tool output would exceed ~20 lines and you only need a summary,
  > delegate it.

  ---
  memory/feedback_subagent_usage.md (project-level feedback memory):

  Spawn agents only when genuinely needed — not for quick lookups or known paths.

  Why: latest /usage shows 84% of usage from subagent-heavy sessions and 70%
  while 4+ sessions ran in parallel. Each subagent runs its own request loop and
  reloads context (cold cache); each parallel session drains the same shared limit.

  How to apply:

- Use Read, Edit, Bash grep/find directly for known paths or single-file lookups
- Only spawn Explore agent when search spans many files or genuinely open-ended (>3 searches)
- Subagent default model = haiku, enforced via CLAUDE_CODE_SUBAGENT_MODEL in ~/.claude/settings.json
- Never spawn just to protect context from a small result — filter with grep/head instead
- Reuse a running agent via SendMessage instead of fresh-spawning (avoids cold context reload)
- Cap concurrent sessions at 1-2; queue work instead of running 4+ in parallel (they share one limit)
- Heavy superpowers skills (writing-plans, brainstorming) run in the MAIN session = bill at
  session model (Opus). No frontmatter model override exists. Invoke only for genuine
  multi-step features, or run them in a Sonnet session to cut cost.

  ---
  The one-line decision rule: If output > ~20 lines and you only need a summary → delegate. Otherwise, use direct tools inline.
