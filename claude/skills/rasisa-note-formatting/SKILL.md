---
name: rasisa-note-formatting
description: Use when converting a RASHISA article draft or markdown file into a note-ready publish package with title, lead, image placement, captions, links, and CTA adjusted for note reading behavior.
---

# RASHISA note Formatting

Turn a RASHISA draft into a note-ready publish kit.

This skill is for the last-mile editorial conversion step:
- one clear theme per article
- note-friendly title and opening
- image and link placement that survives note workflows
- a publish kit that is usable without re-parsing the draft by hand

Use `/Users/resily0808/rasisa/rasisa/sns/note/articles/2026-03-26_howto_rashisa-service-guide.md` as the tone anchor when the user wants the service-intro style from this thread.

## What This Skill Produces

Default deliverable is a **note publish kit** with:

1. title candidates
2. selected title
3. cover image path
4. note-ready body text
5. inline image plan with captions
6. standalone embed URL plan
7. quote-source plan
8. end CTA and suggested tags

If the user asks to save files, prefer:

```text
sns/note/publish-kit/<article-stem>/
  body_for_note.md
  manifest.json
  publication_checklist.md
```

## Core Rules

### 1. One Theme Per Article

RASHISA note should usually stay on **one topic only**.

Good:
- one MBTI type
- one love type
- one strengths angle
- one question about self-analysis
- one value angle of multi-rater feedback
- one use case of 360-degree feedback

Bad:
- MBTI + love type + strengths + service intro in one article
- service explanation plus three unrelated diagnosis topics
- broad “RASHISAの全て” articles unless the user explicitly wants a launch/introduction piece

### 2. Title Must Explain the Value

Follow note-oriented title patterns:

- say the conclusion instead of hiding it
- front-load the main keyword
- use concrete nouns, numbers, or a clear reader situation
- two-sentence titles are acceptable if the meaning becomes clearer
- do not overpromise

Default title patterns:

```text
結論提示型: 「〇〇は△△だった」
具体化型: 「〇〇な人に向けた、△△の話」
2文要約型: 「〇〇は本当に△△なのか？ 調べたら□□が見えた」
```

### 3. Opening 3 Lines Decide the Read

The first 2-3 lines should do at least two of the following:

- name the reader’s doubt or pain
- tell them what they will learn
- tell them why this matters now
- make the article feel related to their actual life

Do not open with a generic self-introduction unless the user explicitly wants a diary/devlog tone.

### 4. note-Friendly Body Rhythm

- paragraph length: usually 2-4 lines on mobile
- prefer H2 sections that can stand alone in the scroll
- use H3 only when it clarifies a single claim
- put one image every 2-4 sections only if it explains, resets attention, or adds proof
- keep one section = one message
- do not use X-style bait, excessive煽り, or overly hard-sell copy

## note Formatting Constraints

The sumini reference article highlighted several practical note issues:

- Markdown image syntax alone is not enough for note publishing workflows
- captions need their own handling
- inline markdown links are not the same as note embeds
- quote sources often need separate treatment
- inline code should not be relied on as-is

Because of that, this skill separates the work into:

1. **body_for_note.md**
   - title removed from body
   - note-safe body text only
2. **manifest.json**
   - cover image
   - inline image positions and captions
   - standalone embeds
   - quote sources
3. **publication_checklist.md**
   - a human-readable handoff for final paste/post work

## Recommended Workflow

### Step 1. Lock the Angle

Before editing, state the article angle in one sentence.

Examples:
- `ISTPが恋愛で誤解されやすい理由`
- `自己分析を1人でやるとズレる理由`
- `360度評価は怖いだけではない`
- `他己分析で強みが言語化される仕組み`

If the draft is carrying multiple angles, split it before polishing.

### Step 2. Build the Publish Kit

If you have a markdown file, run:

```bash
python3 /Users/resily0808/dotfiles/claude/skills/rasisa-note-formatting/scripts/build_note_publish_package.py /absolute/path/to/article.md
```

Optional:

```bash
python3 /Users/resily0808/dotfiles/claude/skills/rasisa-note-formatting/scripts/build_note_publish_package.py \
  /absolute/path/to/article.md \
  --cover-image /absolute/path/to/header.jpg \
  --out-dir /absolute/path/to/sns/note/publish-kit/article-stem
```

The helper script will:

- extract the title from frontmatter or H1
- remove internal metadata bullets used for drafting
- build note-safe body text
- collect images, captions, standalone embeds, and quote sources
- output a manifest that can be used without reading the whole draft again

### Step 3. Upgrade the Editorial Shape

After the package is built, manually improve:

- title clarity
- opening 3 lines
- section order
- image placement
- closing CTA

For RASHISA, keep the tone:

- friendly
- grounded
- explanatory
- useful before clever

### Step 4. Final note-Specific Checks

Check these before calling it ready:

- title tells the value clearly
- first 3 lines are self-contained and relevant
- one article, one theme
- images have captions where needed
- standalone URLs intended for embeds are isolated on their own lines
- quotes with sources are tracked in the manifest
- CTA does not overpower the article
- keywords are readable from search / timeline previews

## RASHISA-Specific Defaults

When formatting RASHISA note articles, bias toward these themes:

- `MBTI / type detail`
  - one type, one question, or one misunderstanding per article
- `love type`
  - one恋愛傾向, one相性軸, or one見られ方 per article
- `strengths`
  - one hidden strength, one use case, or one interview angle
- `social_360 / engineer_360`
  - one workplace value proposition or one evaluation blind spot
- `service value`
  - one insight about self vs others, hidden strengths, or why multi-rater feedback matters

Avoid broad articles that try to explain every template unless the user explicitly wants a service-introduction piece.

## Output Contract

Return the work in this order:

1. chosen title
2. 2-3 alternate titles
3. cover image path
4. body path or body text
5. inline image list
6. embed list
7. CTA
8. assumptions

If files were saved, give the exact saved paths.

## Common Mistakes

- keeping draft metadata bullets inside the publish body
- leaving markdown links in a form that is awkward in note
- using too many themes in one article
- opening too slowly
- using images without a job
- turning a note article into an ad
