# Recharts Patterns

Read this file when the host repo already uses Recharts, or when you choose Recharts for a new React dashboard.

## Why Recharts Fits This Skill

Recharts works well for the Digital Agency dashboard style when the dashboard is:

- presentation-oriented
- React-first
- composed from readable JSX rather than large config objects
- mostly line, bar, area, composed, and pie charts

Prefer Recharts when clarity and local component composition matter more than advanced chart density.

## Official Behaviors Worth Keeping

From the official Recharts API:

- `ResponsiveContainer` is the normal wrapper for responsive charts.
- categorical charts such as `LineChart`, `BarChart`, `AreaChart`, and `ComposedChart` support `Legend`, `Tooltip`, `XAxis`, `YAxis`, and reference elements.
- the chart API exposes `syncId` to synchronize tooltip and brush behavior across related charts.
- chart components expose `accessibilityLayer`; keep it enabled.

## Recommended Component Mapping

| Dashboard need | Recharts default |
| --- | --- |
| monthly trend | `LineChart` + `Line` |
| category ranking | `BarChart` + `Bar` |
| composition over time | `AreaChart` + stacked `Area` |
| summary plus target line | `ComposedChart` + `Bar` or `Area` + `ReferenceLine` |
| small part-to-whole | `PieChart` + `Pie` only when categories are few |

## Rules for Recharts Implementations

- wrap every chart in `ResponsiveContainer`
- keep `accessibilityLayer` on
- remove chart junk first:
  - `axisLine={false}`
  - `tickLine={false}`
  - `CartesianGrid` vertical lines off unless they materially help
- keep legend close to the chart, usually `verticalAlign="top"` and `align="left"`
- use `ReferenceLine` for targets, thresholds, or policy baselines
- use `LabelList` or direct labels when color alone is not enough
- use `syncId` for overview and detail charts that should move together

## Guardrails

- bar charts should keep a zero baseline
- avoid more than five simultaneous colors in a normal dashboard view
- do not default to `PieChart` when a ranked bar chart is clearer
- avoid heavy animation on operational dashboards
- prefer `ComposedChart` only when the combined view is actually clearer than two small charts

## Suggested Defaults

- line stroke width: `2`
- point radius: `3` to `4`
- card chart height: `280` to `340`
- use the bundled `dashboard-theme.css` variables or `dashboard-tokens.ts`

## Bundled Asset

- [assets/recharts-dashboard-starter.tsx](../assets/recharts-dashboard-starter.tsx)
  - includes KPI cards
  - line chart with target reference line
  - ranked bar chart
  - small donut chart for limited-share scenarios
