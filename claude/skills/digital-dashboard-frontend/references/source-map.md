# Source Map

Use official sources first. Use the secondary article only for compression heuristics.

## Official Sources

### 1. ダッシュボードデザインの実践ガイドブック

- Resource page: `https://www.digital.go.jp/resources/dashboard-guidebook`
- 2026-03-31 text export used during skill creation:
  `https://www.digital.go.jp/assets/contents/node/basic_page/field_ref_resources/1948e3cd-736a-4378-9e31-039b08d11106/e7f7ad2f/20260331_resources_dashboard-guidebook_guidebook_02.txt`
- Use for:
  - presentation-oriented vs exploratory dashboard framing
  - 5W1H requirement framing
  - overview-to-detail layout and filter placement
  - chart selection rules
  - chart Do's and Don'ts
  - metadata, update date, source, notes
  - accessibility expectations around contrast and non-color cues
- Usually ignore for frontend implementation:
  - PowerPoint prototyping workflow
  - Power BI操作説明
  - Excel checklist mechanics

### 2. policy-dashboard-assets

- Repo: `https://github.com/digital-go-jp/policy-dashboard-assets`
- README: `https://raw.githubusercontent.com/digital-go-jp/policy-dashboard-assets/main/README.md`
- Theme JSON README:
  `https://raw.githubusercontent.com/digital-go-jp/policy-dashboard-assets/main/powerbi-templates/powerbi-theme-json/README.md`
- Theme JSON directory:
  `https://github.com/digital-go-jp/policy-dashboard-assets/tree/main/powerbi-templates/powerbi-theme-json`
- Map README:
  `https://raw.githubusercontent.com/digital-go-jp/policy-dashboard-assets/main/data/map/README.md`
- Use for:
  - seven palette sequences
  - surface and neutral defaults carried by the official template
  - map file names and join keys
  - supported dashboard component inventory in the Power BI template
- Translate for web instead of reproducing Power BI settings literally.

### 3. デジタル庁デザインシステム

- Color: `https://design.digital.go.jp/dads/foundations/color/color-palette/`
- Typography: `https://design.digital.go.jp/dads/foundations/typography/`
- Layout: `https://design.digital.go.jp/dads/foundations/layout/`
- Spacing: `https://design.digital.go.jp/dads/foundations/spacing/`
- Use for:
  - web typography defaults
  - breakpoint and column-grid decisions
  - spacing scale and hierarchy
  - contrast expectations

## Secondary Source

### ota2000 article

- `https://ota2000.com/blog/dashboard-design-guidebook-as-skill/`
- Use only for:
  - deciding what parts of the guidebook are worth encoding into a skill
  - keeping the skill focused on code-affecting rules
  - separating design-principle guidance from implementation mechanics
- If the article conflicts with the official guidebook or repo, the official source wins.

## Keep vs Drop When Converting to a Skill

Keep content that changes code, layout, chart choice, review comments, or copy.

- Keep:
  - chart selection rules
  - layout direction
  - accessibility and contrast rules
  - metadata requirements
  - palette values and layout tokens
- Drop or summarize heavily:
  - meeting facilitation advice
  - Power BI import steps
  - PowerPoint-only instructions
  - generic process descriptions that do not affect implementation

## Attribution and License Notes

These are source notes, not legal advice. Check the linked READMEs before shipping copied upstream assets.

- The `policy-dashboard-assets` README states that dashboard themes and Power BI templates are under PDL1.0 and gives separate guidance for edited/derived use versus unmodified publication.
- The same repo states that the map files are derived from MLIT administrative boundary data and are published under CC BY 4.0; keep attribution when redistributing the map files.
- If you are only translating palette values and layout ideas into project code, keep an internal source note in code comments, docs, or the PR description unless the user asks for a different practice.
