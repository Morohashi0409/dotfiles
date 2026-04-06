---
name: note-impact-checker
description: Use when reviewing or optimizing a note article for open rate, read completion, saves, trust, and follow-through; especially for RASHISA note drafts that should feel natural on note rather than X or SEO-only media.
---

# note Impact Checker

Analyze a note draft and improve it for how note articles actually get opened and read.

This is the note-native counterpart to `x-impact-checker`.
It does **editorial scoring**, not algorithm prediction.

Use it to:

- judge whether a note article will feel clickable and readable
- fix weak titles and slow openings
- reduce “AI slop” and topic diffusion
- make RASHISA articles feel like note articles instead of landing pages or X posts

## Tone Baseline

Default tone should feel close to the note article created in this thread:

- friendly
- explanatory
- useful before clever
- not overhyped
- still note-native enough to compete with articles on note

For RASHISA, favor:

- one theme per article
- self/other gap insights
- hidden strengths
- one type, one misunderstanding, one utility angle
- honest curiosity over bait

## Scoring System (100 points)

### Tier 1: Entry / Open Rate (30 points)

How likely someone is to open the article from timeline, search, or profile.

| Factor | Max | Scoring Guide |
|--------|-----|---------------|
| Title Clarity & Value | 12 | 12: value and topic instantly clear, 7: partially clear, 2: vague |
| Keyword Front-Load | 8 | 8: main keyword appears early, 4: present but late, 0: buried |
| Opening 3 Lines Hook | 10 | 10: pain/value/self-relevance instantly clear, 5: moderate, 1: slow intro |

### Tier 2: Read Retention (30 points)

How likely the reader is to keep reading once they open.

| Factor | Max | Scoring Guide |
|--------|-----|---------------|
| Single-Theme Discipline | 10 | 10: one clear theme, 5: mild drift, 0: scattered |
| Section Flow | 8 | 8: sections build logically, 4: some jumps, 0: choppy |
| Paragraph Rhythm | 6 | 6: mobile-friendly line breaks, 3: uneven, 0: walls of text |
| Visual Pacing | 6 | 6: images support flow, 3: weak or uneven, 0: missing or noisy |

### Tier 3: Save Value & Trust (25 points)

How likely the article is to be remembered, saved, or treated as credible.

| Factor | Max | Scoring Guide |
|--------|-----|---------------|
| Specificity & Evidence | 10 | 10: concrete examples / grounded claims, 5: mixed, 0: generic |
| Takeaway / Bookmark Value | 8 | 8: readers can use or revisit it, 4: mild value, 0: disposable |
| note Tone Fit | 7 | 7: natural note voice, 4: partly off, 0: feels like ad or X thread |

### Tier 4: Continuation & Conversion (15 points)

How well the article leads to the next relationship step.

| Factor | Max | Scoring Guide |
|--------|-----|---------------|
| Profile Curiosity | 4 | 4: makes readers want to know the author/context, 2: mild, 0: none |
| Follow / Series Potential | 4 | 4: makes future articles feel worth following, 2: some, 0: one-off |
| CTA Quality | 4 | 4: relevant and non-pushy, 2: weak, 0: absent or salesy |
| Link Utility | 3 | 3: links help the reader continue naturally, 1: weak, 0: clutter |

### Penalties (subtract from total)

| Risk | Range | Trigger |
|------|-------|---------|
| Theme Diffusion | -5 to -15 | Too many topics in one article |
| Clickbait / Overpromise | -5 to -15 | Title raises expectations body cannot satisfy |
| AI Slop / Genericity | -5 to -15 | Safe but empty writing, vague claims, interchangeable phrasing |
| Unsupported Certainty | -5 to -20 | Strong claims without evidence or proper framing |

## Grades

| Score | Grade |
|-------|-------|
| 90-100 | S |
| 75-89 | A |
| 60-74 | B |
| 45-59 | C |
| 30-44 | D |
| 0-29 | F |

## Output Format

Keep the report structured and concise.

### Progress Tracking

If `TodoWrite` is available, use these steps:

1. `Read the article and detect the theme`
2. `Score title, opening, structure, and trust signals`
3. `Generate top 5 editorial fixes`
4. `Produce optimized note package`

If `TodoWrite` is unavailable, provide short textual progress updates instead.

### Report Structure

1. `🎯 XX/100 (Grade: X)`
2. breakdown table
3. top 5 priority improvements
4. optimized note package

Use this table shape:

```markdown
| Category | Factor | Score | Max | Assessment |
|----------|--------|-------|-----|------------|
| **🪝 Entry / Open Rate** | | | 30 | |
| | Title Clarity & Value | X/12 | 12 | [reason] |
| | Keyword Front-Load | X/8 | 8 | [reason] |
| | Opening 3 Lines Hook | X/10 | 10 | [reason] |
| **📚 Read Retention** | | | 30 | |
| | Single-Theme Discipline | X/10 | 10 | [reason] |
| | Section Flow | X/8 | 8 | [reason] |
| | Paragraph Rhythm | X/6 | 6 | [reason] |
| | Visual Pacing | X/6 | 6 | [reason] |
| **💾 Save Value & Trust** | | | 25 | |
| | Specificity & Evidence | X/10 | 10 | [reason] |
| | Takeaway / Bookmark Value | X/8 | 8 | [reason] |
| | note Tone Fit | X/7 | 7 | [reason] |
| **🔁 Continuation & Conversion** | | | 15 | |
| | Profile Curiosity | X/4 | 4 | [reason] |
| | Follow / Series Potential | X/4 | 4 | [reason] |
| | CTA Quality | X/4 | 4 | [reason] |
| | Link Utility | X/3 | 3 | [reason] |
| **⚠️ Penalties** | | | | |
| | Theme Diffusion | -X | | [reason] |
| | Clickbait / Overpromise | -X | | [reason] |
| | AI Slop / Genericity | -X | | [reason] |
| | Unsupported Certainty | -X | | [reason] |
| **🏆 TOTAL** | | **XX/100** | | **Grade: X** |
```

### Optimized note Package

Always include:

1. **best title**
2. **2 alternate title options**
3. **rewritten opening 3 lines**
4. **section-order recommendation**
5. **CTA rewrite**

If the input article is short enough, also include a **full optimized version**.
If the input is long, include one **sample rewritten section** instead of rewriting everything unless the user explicitly asks for a full rewrite.

## Detailed Heuristics

### Title Clarity & Value

Strong titles for note:

- reveal the point instead of hiding it
- start with the keyword or problem
- make the benefit legible on first glance
- can be longer if that improves clarity

Weak titles:

- diary-like vagueness
- “〜とは？” mystery without payoff
- broad service names without a reader reason to care

### Opening 3 Lines Hook

Strong openings do one or more of:

- say “this is about you”
- name a frustration or blind spot
- tell the reader what they will get
- create honest curiosity

Weak openings:

- long warmup
- self-introduction before reader value
- generic scene-setting

### Single-Theme Discipline

For RASHISA especially, penalize drafts that mix:

- service intro
- MBTI explanations
- love-type explanation
- strengths explanation
- 360-degree value proposition

inside one short article without a clear spine.

### note Tone Fit

Strong note-native tone:

- sounds like a thoughtful person, not a campaign
- explains instead of shouting
- stays honest about limits
- feels saveable and revisit-worthy

Weak note-native tone:

- X thread energy pasted into long form
- SEO-only keyword stuffing
- LP-style CTA pressure every section

## RASHISA Defaults

Good article angles:

- `ISTPが恋愛で誤解されやすい理由`
- `自己分析を1人でやるとズレる理由`
- `他己分析で強みが見えやすくなる瞬間`
- `360度評価は怖いだけではない`
- `エンジニア素養を他者評価で見る意味`

If the article is trying to do more than one of these, recommend splitting it.

## Common Mistakes

- title is generic while body is specific
- opening starts too far from the reader’s problem
- too many themes in one piece
- images are decorative but not explanatory
- CTA sounds like an ad instead of a natural next step
- the article says little beyond what the reader already assumed
