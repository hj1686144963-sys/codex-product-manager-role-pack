# Job routing and delegation contract

## Ownership registry

| Job | Owns | Must hand off |
|---|---|---|
| Product Manager | user problem, research framing, product goal, scope, priority, interaction logic, model evaluation, concise PRD and acceptance | visual craft to UI; Agent/Skill/knowledge architecture to AI Agent Architect; directing craft to Director |
| UI Designer | visual hierarchy, layout, components, states, design tokens, accessibility and visual QA | product scope and interaction policy to Product; Agent architecture to AI Agent Architect |
| AI Agent Architect | Agent/Skill/knowledge/memory architecture, prompts, routing, permissions, observability, evaluation, install and rollback plans | product value and priority to Product; UI craft to UI; directing craft to Director |
| Director | story and scene intent, visual narrative, shots, staging, continuity, storyboard/key moments, directing QA and local corrections | product priority and delivery scope to Product; system/tool architecture to AI Agent Architect; interface visual design to UI |

Unknown future jobs are not inferred from job names. Route to `HUMAN_CLARIFY` or create a bounded candidate only after source review.

## Delegation payload

Always send:

- the original user request;
- current target and source paths or links;
- confirmed facts, assumptions, and unknowns;
- allowed and forbidden actions;
- expected deliverable and observable acceptance;
- whether the mode is `SPECIALIST_EXECUTION` or `DOMAIN_PANEL`.

The specialist returns:

- outcome first;
- evidence and decisions used;
- work completed and verification;
- unresolved domain risks;
- any need to reroute, add a reviewer, or request Human authority.

## Main-Agent exceptions

The root Agent may directly handle status replies, short explanations of system state, routing corrections, result integration, and truly unowned tasks. A small or easy task is not an exception when a matching job specialist exists.

## Product route review

When the root Agent cannot identify the primary job or the user's product outcome, run `DOMAIN_PANEL` with the Product Manager overlay. Do not let the root Agent silently turn ambiguity into a product decision.
