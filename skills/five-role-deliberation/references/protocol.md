# Deliberation protocol

## Fixed roles

| Role | Primary lens | Must not do |
|---|---|---|
| Coordinator | Frame the decision, control rounds, preserve disputes, synthesize | Lead with a preferred answer or erase dissent |
| Researcher | Facts, sources, benchmarks, model capability, evidence quality | Set product direction or write the final PRD |
| Product Strategist | User value, product logic, interaction, business goal, handoff clarity | Treat implementation guesses as facts or execute design during deliberation |
| System Strategist | Agent/Skill architecture, feasibility, permissions, cost, maintenance, rollback | Build or modify systems during deliberation |
| Red Team Editor | Independent challenge, omissions, false consensus, evidence gaps | Rewrite disagreement into artificial consensus |

## Role report contract

Every specialist returns:

1. `POSITION`: current recommendation in one sentence.
2. `EVIDENCE`: verified facts and source boundaries.
3. `REASONING`: inferences and assumptions.
4. `CHALLENGE`: strongest objection to its own position.
5. `QUESTIONS`: at most three questions for other roles.
6. `REVISION_CONDITIONS`: what would change its view.
7. `RESOURCE_ASSESSMENT`: model, effort, reason, expected gain, stop condition.

## Round controls

- Round 1 is independent; roles must not anchor on each other.
- Cross-questioning targets contradictions and uncovered areas, not agreement for its own sake.
- A new round must produce new evidence, a counterexample, or a changed proposal.
- Ordinary maximum is two rounds; a third needs explicit justification.
- Stalled rounds enter the xhigh value gate described in `SKILL.md`.
- Coordinator may summarize a majority view, but must keep consequential minority views visible.

## Resource baseline

| Situation | Model | Effort |
|---|---|---|
| Source triage, known facts, concise summary | GPT-5.6 Terra | low or medium |
| Product or Agent decision with uncertainty | GPT-5.6 Sol | medium |
| Conflicting constraints or high-impact decision | GPT-5.6 Sol | high |
| Several stalled rounds needing STOP/REDIRECT/CONTINUE gate | GPT-5.6 Sol | xhigh |

Speed is always standard. The panel must not optimize for token use so aggressively that it converges prematurely, but it must state why extra reasoning is expected to change the result.

## Post-deliberation UI handoff

After Human authorizes design execution, Product Strategist may be recalled once in read-only `DESIGN_DRAFT_HANDOFF` mode. It returns a `DESIGN_DRAFT_READY` packet containing:

- approved decision and unresolved constraints;
- primary user, job, and success outcome;
- entry, happy path, empty, loading, error, success, and cancel states;
- confirmed project Design Token/component SSOT;
- screens, components, files, and viewports in scope;
- visual intent and explicit exclusions;
- asset and motion permission status;
- functional, visual, responsive, accessibility, and performance acceptance.

The root Agent, not the deliberation subagent, performs authorized writes through `finesse-ui-design-assistant`. A material direction change returns to Human or a new bounded deliberation.
