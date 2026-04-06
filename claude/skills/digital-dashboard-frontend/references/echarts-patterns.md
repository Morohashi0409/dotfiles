# ECharts Patterns

Read this file when the host repo already uses ECharts, or when you need a more configurable chart engine than Recharts.

## Why ECharts Fits This Skill

Prefer ECharts when the dashboard needs:

- denser chart configuration
- multi-axis or mixed chart layouts
- stronger control over legend, tooltip, and dataset wiring
- SVG or Canvas renderer selection
- future map work or more advanced chart types

Use it carefully. The Digital Agency dashboard style still prefers calm, readable charts over feature density.

## Official Behaviors Worth Keeping

From the official Apache ECharts handbook:

- prefer `dataset` so data stays separate from chart config
- when using the tree-shakeable API, explicitly import and register the chart types, components, and renderer you need
- choose `CanvasRenderer` or `SVGRenderer` explicitly
- SVG rendering is supported and is often a good fit for crisp text and accessible dashboard output
- `aria.show` is off by default and requires importing `AriaComponent`

## Recommended ECharts Defaults

- use `echarts/core` plus explicit `echarts.use([...])`
- default to `SVGRenderer` for frontend dashboards unless you have a concrete Canvas reason
- enable `aria.show: true`
- keep `dataset.source` as plain object rows when possible
- keep legends near the plot area
- keep grid margins modest and `containLabel: true`
- keep tooltip styling white, thin-border, and quiet

## Suggested Option Patterns

### Trend line

- `tooltip.trigger = "axis"`
- `axisPointer.type = "line"`
- `xAxis.type = "category"`
- `yAxis.min = 0` when the metric semantics require it

### Ranked bar

- horizontal bars for long category labels
- `xAxis.type = "value"`
- `yAxis.type = "category"`
- `axisPointer.type = "shadow"` for bar hover

### Donut

- use only when the total is obvious and category count is small
- keep legend adjacent, not detached
- show percent or value labels only when legibility survives

## Accessibility Notes

- import `AriaComponent` and set `aria.show = true`
- use decal patterns or direct labels when color alone is not enough
- avoid low-contrast fill-on-fill combinations

## Guardrails

- do not let ECharts defaults make the dashboard glossy
- avoid bold emphasis animations, large shadows, or oversized hover effects
- do not ship every option in a single giant object when a few small builders are clearer
- keep renderer choice explicit in code

## Bundled Asset

- [assets/echarts-dashboard-starter.tsx](../assets/echarts-dashboard-starter.tsx)
  - registers minimal chart modules
  - provides a React host component
  - includes line, bar, and donut option builders
