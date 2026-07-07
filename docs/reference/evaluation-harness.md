# Evaluation Harness

## Per-skill production gates
- Validate frontmatter and naming rules.
- Confirm the description is narrow, trigger-rich, and names the primary artifact or entrypoint.
- Confirm `SKILL.md` stays lean and pushes detail into `references/`.
- Confirm the primary routing rule names the requested output artifact or business entrypoint.
- For task skills, confirm the checklist output section mirrors the `SKILL.md` output contract.
- Confirm mixed prompts produce an explicit boundary decision with `Primary skill`, `Composed siblings`, and `Deferred scope`.
- For `odoo-review`, `odoo-test`, and `odoo-ship`, confirm evidence status is explicit: `reasoned review only`, `executed`, `planned`, or `blocked`.
- Test at least 3 positive prompts, 2 negative prompts, and 1 tie-breaker prompt.
- Check the closest neighboring skills for overlap and handoff clarity.

## Top collision prompts
1. "What could break if we change sale order confirmation?"
   - Primary: `odoo-think`
   - Why: asks for impact and risks, not steps
2. "Create implementation plan for portal invoice approval."
   - Primary: `odoo-plan`
   - Why: asks for ordered steps and execution artifact
3. "Add the computed margin field and update the form view."
   - Primary: `odoo-build`
   - Why: asks for changed code and XML
4. "Inspect this diff for likely regressions before merge."
   - Primary: `odoo-review`
   - Why: asks for findings on an existing artifact
5. "Validate this checkout change in install, update, and key workflows."
   - Primary: `odoo-test`
   - Why: asks for current-change validation evidence
6. "Which Odoo test class should I use for checkout behavior?"
   - Primary: `odoo-testing-reference`
   - Why: asks for framework guidance, not current validation
7. "Are we ready to deploy this schema change?"
   - Primary: `odoo-ship`
   - Why: asks for go or no-go release readiness
8. "What does -u sale_stock actually do on Odoo.sh staging?"
   - Primary: `odoo-delivery-ops`
   - Why: asks for command and environment semantics
9. "Can portal users escalate access through this controller?"
   - Primary: `odoo-security`
   - Why: exposure and trust boundary are central
10. "Should this checkout template use xpath inheritance or a full QWeb override?"
    - Primary: `odoo-view-ui`
    - Why: asks for template mechanics, not customer journey meaning

## Manual production check
1. Read the skill description only. Decide which skill should trigger for each collision prompt.
2. Read `references/examples.md` only for ambiguous cases.
3. Verify the expected output shape, boundary decision, and evidence-status wording for the changed skill.
4. Tighten descriptions, exclusions, or examples if two skills still plausibly own the same prompt.
5. Re-run quick validation on each changed skill directory.
