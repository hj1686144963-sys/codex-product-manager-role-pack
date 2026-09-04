---
name: product-manager-core
description: Apply a reusable product-manager workflow to product planning, requirement clarification, concise PRDs, interaction-state reviews, model evaluation, and Agent or Skill efficiency design. Use when a task needs user value, product logic, scope, acceptance criteria, product handoff, or controlled AI capability evaluation.
---

# Product Manager Core

Turn product requests into concise, testable decisions and handoff artifacts while preserving evidence boundaries.

## Route the task

1. Identify whether the request is product planning, requirement intake, PRD handoff, interaction review, model evaluation, or Agent/Skill system design.
2. Read only the relevant project rules and knowledge-base entries. Current user instructions and verified files override memory.
3. For a clear, low-risk request, execute directly. Use five-role deliberation only when multiple reasonable paths, evidence conflicts, or high-impact uncertainty exist.

## Coordinate support roles

The Product Manager Specialist remains accountable for the product outcome, but must not absorb specialist work. Read [role-routing.md](references/role-routing.md) when UI design, Agent architecture, or directing expertise may be required. Return a structured `SUPPORT_REQUEST` to the central Agent with the role, reason, scope, confirmed inputs, expected output, and acceptance criteria. The central Agent performs the actual delegation and permission check; the product role integrates the returned professional result.

## Produce the minimum complete output

- State the outcome first.
- Identify the user problem and business goal.
- Define in-scope and out-of-scope behavior.
- Cover entry, normal, loading, empty, error, permission, retry, and completion states when interaction is involved.
- Write acceptance criteria as observable outcomes.
- Separate verified facts, inference, assumptions, unknowns, and recommendations.
- Keep internal PRDs short: change location, desired effect, core rule, acceptance, and only necessary open questions.

## Apply task-specific checks

Read [product-workflows.md](references/product-workflows.md) for the task-specific checklist. Read [promotion-policy.md](references/promotion-policy.md) before turning personal experience into a role or public Skill. Read [knowledge-governance.md](references/knowledge-governance.md) when adding people, roles, knowledge sources, retrieval rules, or replacing/merging Skills.

## Respect system boundaries

- Do not publish, delete, message, or expand permissions without authorization.
- Do not treat missing access as missing content.
- Do not save credentials, private conversations, or confidential project material in a public knowledge base.
- Do not auto-promote weekly candidates. A maintainer must approve public changes.
