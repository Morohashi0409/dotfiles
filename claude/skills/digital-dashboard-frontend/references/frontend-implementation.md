# Frontend Implementation

Use this file right before writing code.

## 1. Start With the Host Repo

Before copying anything from this skill:

1. inspect the existing frontend stack
2. inspect the existing chart library
3. inspect the existing design system or token layer
4. preserve those patterns unless the user asked for a new dashboard system

If the repo already has dashboard primitives, adapt the Digital Agency rules into those components instead of importing the bundled assets wholesale.

## 2. Library Choice

Prefer the chart library already present in the project.

If you must choose:

| Situation | Default choice | Why |
| --- | --- | --- |
| Standard React dashboard with KPI cards and common charts | Recharts | Fast to compose, readable JSX |
| Geo layers, mixed axes, dense enterprise charts | ECharts | Better map and multi-axis support |
| Small self-contained chart embeds | Chart.js | Small footprint for simple cases |

Do not introduce D3 from scratch unless the requested interaction or geometry truly needs custom rendering.

## 3. Recommended Page Structure

Use a structure close to this:

1. page title and short lead
2. compact filter bar
3. KPI row
4. primary chart row
5. secondary detail row
6. table or explanatory notes
7. metadata block

The bundled React starter mirrors this structure without coupling to a specific chart package.

## 4. Component Contracts

### Filter bar

- keep filters few and obvious
- top placement is the default
- left placement is acceptable when filters are stable and always visible

### KPI cards

- label
- value
- optional delta or comparison
- optional helper text for unit or benchmark

### Chart cards

- title
- optional subtitle for period or definition
- chart area
- legend close to the chart
- optional footer note or source fragment

### Metadata block

- data source
- updated at
- as-of
- note

## 5. Translation Rules for Specific Libraries

### Recharts

- use `LineChart`, `BarChart`, `AreaChart`, or `ComposedChart`
- use CSS variables or the bundled token file for colors
- keep custom legends and tooltips simple
- add direct labels for one to three series when space allows
- keep `accessibilityLayer` enabled
- use `ReferenceLine` for targets or policy baselines
- read [recharts-patterns.md](recharts-patterns.md)

### ECharts

- disable glossy emphasis states and strong shadows
- keep `axisPointer` and tooltip styling restrained
- prefer SVG renderer when accessibility or crisp text matters
- maps belong here when the dashboard genuinely needs prefecture or municipality geometry
- use tree-shakeable imports from `echarts/core`
- import `AriaComponent` and set `aria.show: true`
- use `dataset` unless the chart shape strongly resists it
- read [echarts-patterns.md](echarts-patterns.md)

### Chart.js

- use HTML legends when the built-in legend is too far from the chart
- keep line smoothing conservative
- avoid canvas-only metadata; render source and notes in normal DOM

## 6. Bundled Assets

- [assets/dashboard-theme.css](../assets/dashboard-theme.css)
  - starter CSS variables and utility classes
- [assets/dashboard-tokens.ts](../assets/dashboard-tokens.ts)
  - theme and layout tokens for TypeScript projects
- [assets/react-dashboard-starter.tsx](../assets/react-dashboard-starter.tsx)
  - React shell components with no chart-library dependency
- [assets/recharts-dashboard-starter.tsx](../assets/recharts-dashboard-starter.tsx)
  - Recharts-oriented starter page with KPI, line, bar, and donut patterns
- [assets/echarts-dashboard-starter.tsx](../assets/echarts-dashboard-starter.tsx)
  - ECharts registration, React host, and option builders for line, bar, and donut charts

Use these when the target repo has no better local equivalent.

## 7. Review Checklist Before Finishing

- bars start at `0` unless there is a documented reason not to
- legends sit near the corresponding chart
- titles state what is being measured
- color count stays restrained
- a primary series is visually obvious
- data source and update date are visible somewhere appropriate
- layout still works below `768px`
- chart information is still understandable without color-only distinctions
