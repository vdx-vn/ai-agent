# Planning Examples

Worked examples for reference.

## Example 1: Stripe Billing (Complex, Beads)

### Request
"Add billing with Stripe for subscriptions"

### Phase 1: Discovery

```
Agent A: Find entity patterns in packages/domain/src/entities/
Agent B: Search for existing payment code (none found)
Agent C: Check package.json (no Stripe SDK)
```

**Discovery Report:**
```markdown
# Discovery: Billing Module

## Architecture
- Entity pattern: packages/domain/src/entities/user.ts
- Port pattern: packages/domain/src/ports/
- Use case pattern: packages/application/src/usecases/

## Patterns
- No existing billing code
- User entity can map to Stripe customer

## Constraints
- Node 20, Bun, Drizzle ORM
- No Stripe SDK installed

## External
- Stripe SDK: `stripe` npm package
- Webhooks need raw body for signature
```

### Phase 2: Synthesis

**Risk Map:**
| Component | Risk | Verification |
|-----------|------|--------------|
| Stripe SDK | HIGH | Spike |
| Webhooks | HIGH | Spike |
| Entity | LOW | Follow User pattern |

### Phase 3: Spikes

```bash
br create "Spike: Billing" -t epic -p 0
br create "Spike: Stripe SDK import" -t task --blocks <epic>
br create "Spike: Webhook signature" -t task --blocks <epic>
```

**Spike Results:**
```
br close <id> --reason "YES: SDK imports cleanly"
br close <id> --reason "YES: Use stripe.webhooks.constructEvent()"
```

### Phase 4: Beads

```bash
br create "Epic: Billing" -t epic -p 1
br create "Create Subscription entity" -t task --blocks <epic>
br create "Create Stripe webhook handler" -t task --blocks <epic> --deps <entity>
```

**Bead with Learnings:**
```markdown
# Implement Stripe webhook handler

## Learnings from Spike
> - MUST use raw body (not parsed JSON)
> - Use stripe.webhooks.constructEvent()
> - Webhook secret from STRIPE_WEBHOOK_SECRET

## Acceptance Criteria
- [ ] Endpoint at /api/webhooks/stripe
- [ ] Signature verification implemented
- [ ] Handles: checkout.session.completed, invoice.paid
```

---

## Example 2: User Avatar (Simple, No Spikes)

### Request
"Add avatar upload for profiles"

### Phase 1: Discovery (Lightweight)

```
Agent: Find user entity and update patterns
Found: user.ts, update-user.ts, S3 utility exists
```

### Phase 2: Synthesis

**Risk Map:**
| Component | Risk | Reason |
|-----------|------|--------|
| Add avatarUrl field | LOW | Follow existing |
| S3 upload | MEDIUM | Variation of existing |
| Image resize | MEDIUM | New but standard |

No HIGH risk → Skip spikes.

### Phase 3: Beads

```bash
br create "Epic: User Avatar" -t epic -p 2
br create "Add avatarUrl to User entity" -t task --blocks <epic>
br create "Add avatar upload endpoint" -t task --blocks <epic> --deps <entity>
br create "Add avatar to profile UI" -t task --blocks <epic> --deps <api>
```

---

## Decision Tree: When to Spike

```
Pattern in codebase?
├── YES → LOW risk, no spike
└── NO →
    External dependency?
    ├── YES → HIGH risk, SPIKE
    └── NO →
        Affects >5 files?
        ├── YES → HIGH risk, SPIKE
        └── NO → MEDIUM risk, sketch only
```

## Planning Path

```
Beads pipeline
Discovery → Synthesis → Spikes → Beads → Validate → Tracks
```
