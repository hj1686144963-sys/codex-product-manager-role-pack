# Product workflow checks

## Product planning and requirements

- Confirm the target user, current friction, intended outcome, and success signal.
- Compare viable paths and state trade-offs when more than one path is reasonable.
- Define scope, dependencies, permission boundaries, risks, and rollback.
- Distinguish product behavior from implementation guesses.

## Concise PRD handoff

Use this order: change location, desired effect, core rule, key states, acceptance criteria, open questions. Do not repeat the same link or background in several sections.

## Interaction review

Check the complete state model: entry, default, hover or focus when relevant, loading, success, empty, error, permission denied, retry, cancellation, and recovery. Ensure the user always knows what happened and what to do next.

## Model evaluation

- Freeze input samples and scoring definitions.
- Separate model, prompt, structured fields, preprocessing, postprocessing, and UI presentation.
- Change one variable per comparison whenever possible.
- Preserve raw outputs and failure cases; do not report an average without sample coverage and variance.

## Agent and Skill efficiency

- Define trigger, input, output, permissions, cost, maintenance owner, observability, and rollback.
- Prefer small routable Skills over one oversized prompt.
- Record real use, corrections, adopted results, and failure reasons before claiming efficiency gains.
