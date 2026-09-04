---
name: product-ui-design-baseline
description: Apply a reusable product UI baseline to Figma and frontend work while preserving the current project's design system.
---

# Product UI Design Baseline

Use this skill for product interface structure, components, variants, responsive behavior, accessibility and visual QA.

1. Read the current project components, tokens and design instructions first; they are the source of truth.
2. If no project system exists, use Arco Design as the primary structure and visual baseline. Use Ant Design only for complex enterprise interaction patterns.
3. Do not mix visual tokens from multiple systems on one page.
4. Build in this order: Foundations, atomic components, composed components, business components, page templates, page instances.
5. Before promoting a layer, verify variants, Auto Layout, long text, loading/empty/error/disabled states, keyboard access and screenshot QA.
6. Preserve product decisions from the product owner; return `ROUTE_BACK` when a missing business decision changes the outcome.

Read [references/ui-visual-design-baseline.md](references/ui-visual-design-baseline.md) before implementation.
