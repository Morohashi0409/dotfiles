# Japan Map Data

Read this file only when the dashboard needs a geographic view of Japan.

## Upstream Files

Source repo:

- `https://github.com/digital-go-jp/policy-dashboard-assets/tree/main/data/map`

Available files:

- `ja_prefecture_area.json`
  - 47 prefectures
  - join key: 2-digit prefecture code
- `ja_municipality_area.json`
  - 1741 municipalities
  - join key: 5-digit municipality code
- `ja_municipality_area_with_pref_boundary.json`
  - municipality geometry with emphasized prefecture boundaries
  - join key: 5-digit municipality code

## When to Use a Map

Use a map only when spatial distribution is itself the message.

Good cases:

- regional concentration
- neighboring-area patterns
- nationwide coverage or gaps

Prefer bar charts or tables instead when the goal is rank comparison, exact value reading, or trend comparison.

## Implementation Guidance

- Keep the choropleth legend simple and readable.
- Limit the number of color steps.
- If the palette does not provide enough contrast, add labels, tooltips, or a companion table.
- Provide the join key conversion explicitly in code; do not rely on fuzzy region names.
- If the map becomes visually dense on mobile, pair it with a ranked list or table.

## Attribution Note

The upstream README says the map data is derived from MLIT administrative boundary data and published under CC BY 4.0. If you redistribute the map files, keep the required attribution from the upstream README.
