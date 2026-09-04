# Product UI visual baseline

## Priority

1. Current user instruction.
2. Existing project components, variables and tokens.
3. Arco Design as the default baseline when no system exists.
4. Ant Design patterns only for complex enterprise interactions.

## Construction order

`Foundations -> atoms -> compositions -> business components -> templates -> instances`

Each layer must pass variant coverage, Auto Layout, long-text, responsive, keyboard, contrast and screenshot checks before the next layer becomes authoritative.

## Token boundary

Use one source for color, typography, spacing, radius, shadow, density and component states on a page. References from another system may inform an interaction pattern, but must not silently introduce a second visual token set.

## Evidence

Do not claim that a UI is implemented or accepted from a static specification alone. Verify the actual file or rendered interface and preserve the evidence path in the task result.
