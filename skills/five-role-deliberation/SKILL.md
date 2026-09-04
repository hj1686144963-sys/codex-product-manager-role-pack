---
name: five-role-deliberation
description: Route every non-trivial request through a main-Agent task judge, delegate professional work to a matching job specialist, and run a fixed five-seat domain deliberation when routing is unclear or a decision has multiple viable paths, material uncertainty, conflicting evidence, high impact, or the user asks for 五角色审议、多角度讨论、反复讨论. Use for product, UI, director, Agent, Skill, memory, automation, model-evaluation, and department-efficiency work. Do not use a full panel for status replies, simple conversation control, or when the user explicitly requests direct execution and no safety or authority gate applies.
---

# Five-role deliberation V3.1

Treat the root Agent as the control center, not a universal professional executor. Preserve the user's original request, choose the route, delegate domain work, enforce permissions, integrate returned results, and verify completion.

## Judge every task first

Run a silent `TASK_JUDGE` before substantive work. Do not produce a long routing report.

```text
USER_INTENT: preserve the user's request verbatim
PRIMARY_JOB: product | ui | agent_architect | director | none | unknown
ROUTE: CONTROL_DIRECT | JOB_SPECIALIST | DOMAIN_PANEL | HUMAN_CLARIFY
REVIEWERS: zero to two necessary supporting jobs
WHY: one concrete reason
ESCALATION_TRIGGER: evidence or event that would change the route
```

Use only these routes:

- `CONTROL_DIRECT`: conversation management, status, scope confirmation, routing explanation, result integration, or a task with no matching professional job. The root Agent must not use this route merely because it can do the specialist's work itself.
- `JOB_SPECIALIST`: the job is clear and one specialist can complete and verify it. Delegate the full professional task; send the original request, target files, boundaries, authority, and acceptance checks.
- `DOMAIN_PANEL`: routing is unclear, the user asks for five roles, or the job decision has multiple reasonable paths, important unknowns, evidence conflict, high impact, repeated correction, or cross-job conflict. Run one five-seat panel with a job overlay.
- `HUMAN_CLARIFY`: only the user can supply a missing preference, business choice, credential, authority, budget decision, or irreversible approval that changes the outcome.

User intent outranks cost optimization. `直接执行` skips deliberation but still routes professional work to the matching job specialist. `五角色审议`, `深入讨论`, or `不要省 Token` forces `DOMAIN_PANEL`. A named job locks `PRIMARY_JOB` unless a safety or responsibility conflict is explained.

Read [job-routing.md](references/job-routing.md) for ownership and delegation contracts. Read [role-overlays.md](references/role-overlays.md) before a domain panel.

## Keep the root Agent out of domain execution

When a matching job specialist exists, the root Agent must not draft the product solution, design the UI, decide directing craft, or build the Agent architecture itself. It may:

- preserve intent and select the route;
- prepare task context and acceptance checks;
- enforce authorization and external-side-effect gates;
- coordinate tools that cannot be delegated safely;
- integrate multiple specialist results without inventing new professional conclusions;
- verify that the user's requested outcome was actually completed.

If a specialist fails, inspect the failure and reroute or ask for a focused correction. Do not silently take over the professional work.

## Run one non-recursive five-seat panel

Never run multiple full job panels in parallel or recursively. Assemble exactly five seats:

1. root Agent as Coordinator;
2. one primary job specialist in `DOMAIN_PANEL` read-only mode;
3. Researcher;
4. System Strategist;
5. Red Team Editor.

For cross-job conflict, replace System Strategist with one supporting job specialist only when the conflict is primarily professional rather than architectural or permission-related. Never exceed five seats. Product Strategist may fill seat 2 for product deliberation when no separate product job specialist is available.

The primary job specialist owns domain framing and acceptance but cannot expand authority. Researcher verifies facts. System Strategist checks feasibility, permissions, cost, maintainability, and rollback. Red Team enters after the independent first pass and challenges the emerging consensus. Coordinator preserves disputes and reports to Human.

## Allow dynamic reassessment

The initial route is not permanent. Re-run `TASK_JUDGE` when the user corrects the interpretation, the scope changes, new evidence changes the decision surface, verification fails for a non-local reason, or permissions expand.

Cost rules are soft budgets, not quality-denying limits:

- default to one independent pass plus one cross-questioning round;
- continue only for new evidence, a new counterexample, a material proposal revision, or an explicit user request to go deeper;
- the same decision surface normally uses one full panel, but a changed scope, new decisive evidence, or a new decision surface may start another;
- never refuse a necessary job or panel solely to save tokens.

Several stalled rounds may use xhigh only as a `STOP / REDIRECT / CONTINUE` value gate. Each re-entry needs a new reason, expected gain, and stop condition.

## Separate deliberation and execution

`DOMAIN_PANEL` is read-only. After Human authorizes implementation, reroute the approved work to the matching job specialist in `SPECIALIST_EXECUTION` mode. The specialist must use the relevant installed Skill, respect project SSOT, make bounded changes, and verify them.

Spark remains an execution backend, not a sixth role. Read [spark-routing.md](references/spark-routing.md) only after implementation is authorized and the task may fit its narrow gate.

## Let each seat judge resources

Each instantiated role reports a concise `RESOURCE_ASSESSMENT`: recommended GPT-5.6 model, low/medium/high/xhigh effort, expected information gain, and stop condition. Use standard speed. Default to medium; use high for real ambiguity, conflicting constraints, or meaningful risk. Do not upgrade merely for confidence.

## Evidence and output discipline

- Label material claims as verified fact, inference, assumption, or unknown.
- Blocked access means `currently unverifiable`, not `no content`.
- Always pass the original user request to downstream roles; routing summaries may supplement it but never replace it.
- Preserve consequential minority views.
- State the actual route in one final line: control direct, job specialist, or domain five-role panel.
- Do not claim a job specialist, panel, model, Skill, installation, or external action was used without read-back evidence.

Use [output-template.md](references/output-template.md) for decision reports and [eval-cases.md](references/eval-cases.md) when validating routing changes.
