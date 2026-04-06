# Chart and Layout Rules

Use this file when deciding what the dashboard should contain and how charts should behave.

## 1. Dashboard Mode

Default to a presentation-oriented dashboard unless the user explicitly wants investigation tooling.

| Mode | Goal | UX bias | Typical UI |
| --- | --- | --- | --- |
| Presentation-oriented | Notice status, compare against a benchmark, decide whether action is needed | Fast reading, low interaction cost | KPI cards, a few filters, summary charts, notes |
| Exploratory | Find differences, identify causes, dig deeper | Richer controls, drill-down, more panels | Detailed filters, cross-highlighting, dense tables |

For this skill, prefer presentation-oriented design. That matches the official guidebook's primary emphasis.

## 2. Layout Translation for Web

Translate the guidebook's "left-top overview, right-bottom detail" principle into responsive frontend structure.

- Desktop:
  - start with summary cards or status blocks in the first visible row
  - place filters at the top or left edge
  - place supporting charts after the KPI row
  - reserve the lowest-priority detail for the lower half of the page
- Mobile:
  - collapse to a single column under `768px`
  - keep the first screen useful even without scrolling
  - move filters into a compact stack or drawer if they dominate the page

Translate the guidebook's 16:9 six-way split into a web-friendly grid:

- use a 12-column desktop grid
- use `24px` to `32px` section gaps on desktop
- use `16px` to `24px` card padding
- use `8px`, `24px`, and `64px` as the core spacing hierarchy

## 3. Comparison Context

If a number alone is hard to act on, add a comparison target.

Common comparison companions:

- goal or target
- previous period
- year-over-year
- average
- peer group or benchmark

Do not show a lone metric if the reader cannot tell whether it is good, bad, or unusual.

## 4. Chart Selection

Choose the simplest chart that expresses the question.

| User question or intent | Default chart | Notes |
| --- | --- | --- |
| How is this changing over time? | Line chart | Use time on the horizontal axis |
| Which category is larger? | Bar chart | Start at `0`; sort meaningfully |
| How does composition change over time? | Stacked area or stacked bar | Use only when part-to-whole matters |
| What is the current headline value? | KPI card | Add unit and comparison context if needed |
| What share does each part occupy? | Pie or donut only when the total is obvious and the category count is low | In most other cases, prefer bar |
| What are the details behind the summary? | Table or detail card | Keep it below or after the summary block |

If the user asks for scatter plots, treemaps, heatmaps, sankeys, or other advanced visuals, justify them explicitly instead of using them by default.

## 5. Do's and Don'ts for Review

Use these rules both while coding and while reviewing generated UI.

### Do

- show the overall KPI first and the detail after it
- order items meaningfully, for example by magnitude, update date, or business priority
- keep titles short but specific
- include the data type in titles when ambiguity is possible, for example "月次推移" or "累計"
- keep legends next to the corresponding chart
- reduce visual noise, grid lines, and redundant text
- use one highlighted series and a restrained supporting palette
- add direct labels or markers when color contrast is insufficient
- include source, update date, as-of date, and notes when the dashboard is public or operationally important

### Don't

- use 3D effects, bevels, glows, or decorative chart chrome
- use too many colors
- separate legends far from the chart
- crop or distort axes to exaggerate differences
- depend only on color to distinguish categories
- fill a page with controls before the reader sees the key answer

## 6. Accessibility and Honesty

- Maintain at least `3:1` contrast for non-text chart elements against their background.
- Maintain at least `4.5:1` contrast for chart text and metadata.
- If chart fills cannot meet contrast expectations, place values near the mark or reveal them on hover and keyboard focus.
- Add non-color distinctions for multi-series charts:
  - markers
  - stroke dashes
  - direct labels
  - patterns or texture for fills when appropriate

## 7. Metadata Block

Most frontend dashboards should have a small metadata block near the end of the page or at the bottom of a card.

Recommended fields:

- data source
- updated at
- as-of date or time window
- note or caveat

Keep metadata visually quieter than the charts, but do not hide it.

## 8. Performance Bias

The guidebook explicitly values quick display and response.

- Prefer the smallest chart primitive that answers the question.
- Avoid over-animating live or operational dashboards.
- Avoid rendering hidden tabs or panels until needed.
- Avoid loading heavy geo or interaction packages unless the dashboard actually needs them.
