# GPT-5.3-Codex-Spark conditional routing

## Status and responsibility boundary

Spark is a model backend, not a sixth role. It has no independent product, research, architecture, risk, or authorization responsibility. Five-role deliberation remains read-only by default; Spark can only be considered after the user has authorized implementation.

No task is guaranteed error-free. The objective is to use Spark only where an independent verifier can detect and block material errors before acceptance.

If the current runtime does not explicitly expose a supported Spark model identifier and auditable actual-model information, the only allowed Spark state is `SPARK_SHADOW`: classify, log, and fall back without calling Spark.

## Capability profile

Verified from OpenAI's February 12, 2026 product announcement:

- research-preview, smaller real-time coding model;
- more than 1000 tokens per second on its low-latency serving path;
- 128k context and text-only;
- designed for targeted edits, reshaping logic, and refining interfaces;
- default style is lightweight and minimally targeted;
- does not automatically run tests;
- uses a separate rate limit during the preview.

Inference: these properties support fast iteration on tightly scoped code changes, but do not establish higher correctness or lower end-to-end cost.

## State machine

1. `NOT_ELIGIBLE`: any eligibility gate is missing or any deny rule matches. Use the existing model and workflow.
2. `SPARK_SHADOW`: the task fits, but Spark is unavailable, its actual identity is not auditable, or the route is still under evaluation. Do not call Spark; record the classification and fall back.
3. `READY_FOR_SPARK`: task fit, runtime support, implementation authorization, locked verifier, and rollback baseline are all present. Display or record the scope and validation card before execution.
4. `RUN_AND_VERIFY`: Spark may produce a candidate patch. The outer executor applies scope and verification gates.
5. `FALLBACK`: discard the candidate and restart from the original baseline with the existing model when any gate fails.

Define task fit separately from runtime availability:

`task_eligible = implementation_authorized && task_fit && low_risk_semantics && bounded_scope && text_only && deterministic_validator && no_deny_hit`

`spark_runnable = task_eligible && runtime_supported && actual_model_auditable`

## Allowlist

Every gate must pass:

- one clear implementation objective with no unresolved product or architecture decision;
- target files, symbols, allowed area, and forbidden area are enumerated before the call;
- local, reversible code edit that follows an existing pattern;
- examples include a reproducible small bug fix, behavior-preserving local refactor, private-interface adaptation, or UI-code refinement using the existing design system;
- required context is fully representable as text;
- failure has no external side effect and can be discarded from a known baseline;
- an independent, pre-existing verifier can check the requested behavior;
- the expected verification and review cost is lower than using the existing model directly.

File count and diff size may be logged as scope observations, but never override semantic risk rules.

## Deny list

Any match makes the task ineligible:

- authentication, authorization, permissions, secrets, privacy, cryptography, payments, money, or security boundaries;
- database schema, migrations, persistence formats, destructive transforms, deletion safeguards, or production data;
- concurrency, transactions, idempotency, distributed consistency, cache invalidation, or resource lifecycle;
- dependencies, lockfiles, build systems, generated artifacts, CI/CD, deployment, infrastructure, production configuration, or feature-flag defaults;
- public APIs, protocols, cross-service contracts, shared configuration, or architecture boundaries;
- external side effects such as sending, publishing, charging, uploading, mutating remote state, or irreversible operations;
- ambiguous requirements, competing goals, evidence conflicts, or a need for research or Human judgment;
- large unfamiliar-codebase exploration before scope can be defined;
- images, screenshots, audio, video, visual-state inspection, or other non-text evidence;
- missing, weak, model-authored, or mutable acceptance criteria;
- a need to alter tests, snapshots, golden files, fixtures, schemas, build configuration, or the verifier itself;
- any task selected only to consume Spark quota.

## Verifier ownership and acceptance

The non-Spark main executor or existing default model must define and lock before the call:

- allowed and forbidden files;
- validation commands;
- pass/fail criteria;
- validator coverage and known limits;
- rollback baseline and fallback condition.

Spark may not weaken or modify them. Its output is always a candidate patch. Acceptance requires:

1. scope check against the authorized file and diff boundary;
2. syntax/type/lint/build checks that are relevant to the change;
3. targeted behavior tests using the locked verifier;
4. adjacent regression checks proportional to semantic risk;
5. review by the non-Spark path for hidden interface, security, and user-change conflicts.

A passing command is not sufficient if the verifier lacks the ability to detect the requested failure.

## Retry and fallback

Allow at most one Spark correction, and only when all are true:

- the first patch stayed in scope;
- the failure is deterministic, local, and mechanically actionable;
- the locked verifier is unchanged;
- the correction does not expand scope or semantic risk.

Any out-of-scope change, security signal, requirement misunderstanding, multiple non-local failures, validator change, second failure, unavailable model, quota exhaustion, or unauditable actual model triggers immediate fallback. Discard the Spark candidate and restart from the original baseline; do not build further work on an untrusted partial state.

## Quota and success metrics

Separate quota is a capacity constraint, not a target. Never route work merely to use it up.

Prioritize metrics in this order:

1. severe escaped-defect and out-of-scope rate;
2. independently verified success rate;
3. human rework;
4. end-to-end time to a verified result;
5. fallback rate and total inference cost.

Calls, tokens, and quota utilization are diagnostic only.

## Shadow evaluation and graduation

Start with shadow classification and a preregistered replay set. Include counterexamples where a one-line edit has high semantic risk: authentication, deletion conditions, amount/date calculations, migration guards, idempotency, and tests that pass while the requirement remains wrong.

Only consider a narrow canary after the runtime exposes Spark and actual model identity can be audited. Graduate a task class only when comparison against the existing baseline shows no worse severe escaped-defect rate, acceptable verified success, and a material reduction in end-to-end time or total cost. Any preview capability, identifier, quota, or behavior change returns the route to `SPARK_SHADOW`.

Minimum log fields: route state, task class, semantic risk class, eligibility results, deny reason, requested model, actual model, runtime support, implementation authorization, allowed/forbidden scope, locked verifier, validation results, attempts, fallback reason, patch accepted, latency, router version, and policy version. Do not log secrets or unnecessary source content.
