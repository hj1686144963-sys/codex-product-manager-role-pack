---
name: five-role-deliberation
description: Use a fixed five-role review panel to challenge complex product, interaction, model-evaluation, Codex Agent, Skill, memory, automation, and department-efficiency decisions. Trigger when the user explicitly asks for 五角色审议、多角度讨论、反复讨论, or when a decision has multiple viable paths, material uncertainty, conflicting evidence, high impact, or repeated stalled reasoning. Do not invoke the full panel for clear low-risk execution, formatting, simple edits, or when the user says 直接执行.
---

# Five-role deliberation

Use this skill as a supervision and thinking system, not as an execution team. The user is Human and remains the final decision-maker. The root agent is the Coordinator; the four specialist agents are Researcher, Product Strategist, System Strategist, and Red Team Editor.

## Route the task first

Silently classify every request:

- `BYPASS`: clear goal, low risk, one obvious path, or the user says `直接执行`. Use the appropriate normal skill and do not run the panel.
- `DELIBERATE`: multiple reasonable paths, important unknowns, evidence conflict, high-impact product/Agent decisions, or the user says `五角色审议`. Run this protocol before implementation.
- When uncertain, do a short Coordinator preflight only. Do not spend a full panel merely to classify the task.

Read [protocol.md](references/protocol.md) before a full deliberation. Read [vault-routing.md](references/vault-routing.md) when user history or durable knowledge is relevant. Use [output-template.md](references/output-template.md) for the final report.

## Run the panel

1. Coordinator states the exact decision, scope, known facts, unknowns, and what would change the decision. Do not reveal a preferred answer yet.
2. Run the first independent pass in this order:
   - Researcher checks facts, evidence, model/product capability, comparable solutions, and unverified assumptions.
   - Product Strategist examines user value, product logic, interaction states, business outcome, and PRD implications.
   - System Strategist examines Agent/Skill architecture, permissions, maintainability, cost, rollback, and operational fit.
   - Red Team Editor receives the three reports, searches for logical gaps, omitted scenarios, false consensus, and premature convergence.
3. Coordinator records agreement and disagreement without deleting minority views.
4. Run one bounded cross-questioning round. Each role must add new evidence, a counterexample, or a concrete revision; repeated wording is not progress.
5. Run a second round only if the first round changed the decision surface. A third ordinary round requires new evidence, a major unresolved split, or high-risk consequences.
6. End with a decision report. Do not implement, publish, edit external systems, or turn the result into a PRD unless the user separately asks.

## Hand approved UI decisions to design execution

Keep design execution outside the panel. After the decision report is complete and the user separately authorizes design execution, the Coordinator may ask Product Strategist for a `DESIGN_DRAFT_READY` handoff. This is a post-deliberation handoff, not another review round.

The handoff must lock the approved direction, user job, critical interaction states, project Design Token/component SSOT, screen or component scope, asset and motion permissions, and acceptance criteria. Product Strategist remains read-only and does not modify files or design tools. The authorized root Agent uses `$finesse-ui-design-assistant` to create the design artifact or implementation under that handoff.

If execution reveals a material product-direction conflict, missing decision, or need to replace the project's visual system, stop execution and return the issue to Human or the panel. Do not silently revise the decision or create a parallel visual SSOT.

## Route Spark only after deliberation and authorization

GPT-5.3-Codex-Spark is not a sixth role and must not replace any specialist's judgment. It is only a possible post-deliberation code-generation backend after the user has separately authorized implementation. When an authorized task may be a bounded, low-risk coding micro-task, read [spark-routing.md](references/spark-routing.md) and apply every eligibility and verification gate.

Treat Spark routing as `SPARK_SHADOW` whenever the current runtime does not explicitly expose a supported Spark model identifier and auditable actual-model information. In shadow mode, classify the task, record the deny or eligibility reason, and fall back to the existing model. Never guess an unsupported model name, claim Spark was called, or optimize for consuming its separate quota.

## Let each role judge its own resources

Each specialist starts with a lightweight preflight and reports a `RESOURCE_ASSESSMENT`:

- recommended model: `gpt-5.6-terra`, `gpt-5.6-sol`, or, only for mechanical filtering, `gpt-5.6-luna` when available;
- reasoning effort: `low`, `medium`, `high`, or `xhigh`;
- why the upgrade is worth its cost;
- expected information gain;
- stop condition.

Use standard speed only. Prefer GPT-5.6 family. Default to `gpt-5.6-sol` with `medium`; use Terra for research, source triage, and summaries when deep reasoning is unnecessary. Use high only for real ambiguity, conflicting constraints, or meaningful risk.

Do not change a running agent's model or effort. If its justified request is approved, start one replacement run for the same role at the requested setting and retire the lower-effort draft. Keep only one active instance per role.

## Use xhigh as a value gate, not a routine upgrade

When several bounded rounds stall, an xhigh run first decides one of:

- `STOP`: further discussion is unlikely to change the decision; report why and stop.
- `REDIRECT`: identify the missing evidence, reframed question, or new path; run one or two bounded rounds on that direction.
- `CONTINUE`: state the expected gain and allow one or two bounded rounds.

If those rounds still stall, xhigh may be used again for the same value-gate decision. There is no arbitrary one-use cap, but every re-entry requires a new reason, expected gain, and stop condition. Never use xhigh merely to make an answer sound more confident.

## Evidence and output discipline

- Label material claims as verified fact, inference, assumption, or unknown.
- Blocked access means `currently unverifiable`, never `no content`.
- Keep the report concise and understandable to a product manager.
- Preserve unresolved minority opinions and state what evidence would resolve them.
- Separate deliberation from authorization to execute.

Use the three cases in [eval-cases.md](references/eval-cases.md) when validating routing or revising this skill.
