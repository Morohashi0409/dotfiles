# Design Tokens

Use this file when you need web-facing defaults derived from the Digital Agency dashboard guidance and assets.

## Typography

The Digital Agency design system site uses `Noto Sans JP` and `Noto Sans Mono` on the web. The Power BI theme JSON itself uses `Arial` defaults in some places, so do not copy the font stack literally into a frontend.

Recommended web stack:

- Sans: `"Noto Sans JP", system-ui, sans-serif`
- Mono: `"Noto Sans Mono", ui-monospace, SFMono-Regular, monospace`

Recommended dashboard subset inferred from the DADS typography scale and the Power BI template defaults:

| Token | Use | Web suggestion |
| --- | --- | --- |
| `metric-value` | main KPI value | `700 32px/1.5` |
| `section-title` | section heading | `700 24px/1.5` |
| `card-title` | chart or card heading | `700 16px/1.7` |
| `body` | ordinary copy | `400 16px/1.7` |
| `dense-label` | axes, legends, filter text | `400 14px/1.3` |
| `meta` | source, update date, notes | `400 14px/1.5` using mono or tabular numerals |

## Layout

Use the Digital Agency layout and spacing foundations as web defaults.

| Token | Value | Source / rationale |
| --- | --- | --- |
| `max-width` | `1440px` | DADS layout wrapper |
| `breakpoint-md` | `768px` | DADS example breakpoint |
| `grid-columns` | `12` | DADS layout guidance |
| `space-1` | `8px` | DADS spacing base unit |
| `space-2` | `16px` | comfortable dense spacing |
| `space-3` | `24px` | standard section gap |
| `space-4` | `32px` | roomy desktop gap |
| `space-6` | `64px` | section hierarchy gap |
| `card-radius` | `12px` | consistent with modern DADS component corners |

Use `8px`, `24px`, and `64px` as the primary hierarchy. Reach for `16px` and `32px` only to smooth the layout.

## Palette Sequences From policy-dashboard-assets

The theme JSON files expose eight `dataColors`. The first five usually form the main hue scale, the last three are helper colors from the official template.

- Blue:
  - `#0017C1`, `#3460FB`, `#7096F8`, `#C5D7FB`, `#E8F1FE`, `#FE3939`, `#FFBBBB`, `#F8F8FB`
- Light Blue:
  - `#0055AD`, `#008BF2`, `#57B8FF`, `#C0E4FF`, `#F0F9FF`, `#FE3939`, `#FFBBBB`, `#F8F8FB`
- Cyan:
  - `#006F83`, `#00A3BF`, `#2BC8E4`, `#99F2FF`, `#E9F7F9`, `#666666`, `#CCCCCC`, `#F8F8FB`
- Green:
  - `#115A36`, `#259D63`, `#51B883`, `#9BD4B5`, `#E6F5EC`, `#666666`, `#CCCCCC`, `#F8F8FB`
- Orange:
  - `#AC3E00`, `#FB5B01`, `#FF8D44`, `#FFC199`, `#FFEEE2`, `#666666`, `#CCCCCC`, `#F8F8FB`
- Red:
  - `#CE0000`, `#FE3939`, `#FF7171`, `#FFBBBB`, `#FDEEEE`, `#666666`, `#CCCCCC`, `#F8F8FB`
- Solid Gray:
  - `#4D4D4D`, `#767676`, `#999999`, `#CCCCCC`, `#F2F2F2`, `#3460FB`, `#FE3939`, `#F8F8FB`

### Recommended Role Mapping

This mapping is a web-friendly inference, not an official token definition.

| Derived role | Recommended source |
| --- | --- |
| `accent-strong` | `series-1` |
| `accent` | `series-2` |
| `accent-soft` | `series-4` |
| `accent-surface` | `series-5` |
| `aux-1` | `series-6` |
| `aux-2` | `series-7` |
| `canvas` | `series-8` |

Important: `series-6` and `series-7` are not semantically stable across all themes. In blue themes they behave like alert colors; in several other themes they behave like neutrals. Treat them as helper colors, not always as error states.

## Contrast Guidance

The guidebook requires:

- `3:1` for non-text chart marks against the background
- `4.5:1` for chart text and metadata

Practical frontend translation:

- Use `accent-strong` or darker for thin lines and small marks.
- Use `accent-soft` or `accent-surface` for fills and background highlights.
- If filled areas still fail contrast, add adjacent values or accessible hover/focus details.

## Numeric and Metadata Styling

Use tabular numerals for:

- KPI cards
- axis values
- table measures
- update timestamps

This is why the bundled assets expose a mono stack and set `font-variant-numeric: tabular-nums`.
