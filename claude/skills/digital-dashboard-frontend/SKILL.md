---
name: digital-dashboard-frontend
description: >
  Build frontend dashboards from Digital Agency dashboard guidance and assets. Use when the user asks
  for dashboard design, KPI cards, chart selection, filter layout, Japan map visualization, or frontend
  graph implementation in React, Vue, TypeScript, or plain web UI, especially for "デジタル庁っぽい"
  dashboards. This skill is for web frontend delivery, not Power BI authoring.
---

# Digital Dashboard Frontend

Use this skill when dashboard work should follow the Digital Agency dashboard guidebook and design system,
but the output is web frontend code rather than Power BI files.

## Scope

- Prefer official Digital Agency rules for layout, chart choice, color, spacing, typography, and metadata.
- Treat `policy-dashboard-assets` as a source of tokens and examples, not as a Power BI requirement.
- Keep the work inside the target repo's existing frontend stack and design system whenever one already exists.
- Read [references/source-map.md](references/source-map.md) first when you need to confirm which source covers which rule.
- Read [references/chart-and-layout-rules.md](references/chart-and-layout-rules.md) for design decisions.
- Read [references/frontend-implementation.md](references/frontend-implementation.md) before writing code.
- Read [references/design-tokens.md](references/design-tokens.md) when you need colors, spacing, layout, typography, or reusable CSS variables.
- Read [references/recharts-patterns.md](references/recharts-patterns.md) when the repo uses Recharts or when you plan to add it.
- Read [references/echarts-patterns.md](references/echarts-patterns.md) when the repo uses ECharts or when you need a denser charting engine.
- Read [references/japan-map-data.md](references/japan-map-data.md) only when the dashboard needs prefecture or municipality maps.

## Workflow

1. Identify the dashboard mode.
   - Default to a presentation-oriented dashboard unless the user clearly wants exploratory analysis tooling.
   - Presentation-oriented dashboards should optimize for quick situation awareness, anomaly detection, and action cues.
2. Inspect the codebase and keep the existing stack.
   - Reuse the chart library already present in the repo.
   - If the repo has no chart stack and you must pick one, default to Recharts for standard React dashboards, ECharts for complex mixed charts or map layers, and Chart.js for small standalone embeds.
3. Translate the guidebook into frontend structure.
   - Start with overview KPIs or status cards at the upper-left or first visible block.
   - Place filters at the top or left; place affected charts below or to the right.
   - Move from overall context to detail.
4. Apply chart rules before writing code.
   - Time trend -> line
   - Category comparison -> bar
   - Part-to-whole over time -> stacked area or stacked bar
   - Compact share-of-total with a clear total -> pie or donut; otherwise prefer bar
   - Single KPI -> metric card
5. Apply accessibility and honesty rules.
   - Keep bar chart baselines at `0` unless the user explicitly asks for and justifies an exception.
   - Keep legends adjacent to the chart.
   - Use one to five colors for normal comparisons and emphasize one primary series.
   - Do not rely on color alone; add markers, stroke styles, labels, or direct values when needed.
   - Include data source, update date, time basis, notes, or disclaimers when the dashboard is user-facing.
6. Use bundled assets only as starters.
   - [assets/dashboard-theme.css](assets/dashboard-theme.css) provides CSS variables and layout tokens.
   - [assets/dashboard-tokens.ts](assets/dashboard-tokens.ts) provides frontend-friendly theme data and defaults.
   - [assets/react-dashboard-starter.tsx](assets/react-dashboard-starter.tsx) provides a React shell with no chart-library lock-in.
   - [assets/recharts-dashboard-starter.tsx](assets/recharts-dashboard-starter.tsx) provides a Recharts-oriented page template.
   - [assets/echarts-dashboard-starter.tsx](assets/echarts-dashboard-starter.tsx) provides an ECharts-oriented React host and option builders.
   - Adapt these to the host repo instead of copying blindly.

## Output Expectations

- Produce responsive frontend code, not Power BI instructions.
- Keep copy concise and explicit: title, unit, time basis, source.
- Avoid glossy BI decoration: 3D effects, heavy shadows, oversized gradients behind charts, excessive legends, or rainbow palettes.
- If the user asks for a dashboard from scratch, explain the chosen dashboard mode, chart choices, and theme briefly in the final answer.

## Source Handling

- Official Digital Agency sources take precedence over all secondary summaries.
- Use the ota2000 article only as a pattern for what to keep or discard when converting a long guidebook into a practical skill.
- When copying raw palette values, map data, or other upstream assets into a project, consult [references/source-map.md](references/source-map.md) for the relevant source and attribution note.
