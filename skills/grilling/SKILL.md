---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Before asking anything, explore: the current implementation (relevant files, models, existing behavior) and, if this touches Odoo, the Odoo source base (base ORM, relevant addons) for how it already handles this. Use this exploration to eliminate questions that exploration alone can answer, and to sharpen the remaining ones with concrete specifics (field names, existing constraints, current behavior) instead of asking in the abstract.

After exploring, give a short estimate of how many questions you expect to ask and why (e.g., "~6 questions: 2 on data model, 3 on business rules, 1 on UI"), before asking the first one.

Interview me relentlessly about every aspect of this until we reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking me. The *decisions*, though, are mine — put each one to me and wait for my answer.

Do not act on it until I confirm we have reached a shared understanding.
