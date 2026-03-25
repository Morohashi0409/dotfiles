---
name: rashisa-share-image-design
description: Design or revise RASHISA share images, OGP/X card images, and header visuals. Use when creating social-card artwork, polishing header graphics, or shipping image changes that must display correctly on X.
---

# RASHISA Share Image Design

## Overview

Use this skill when working on RASHISA share visuals in `/Users/resily0808/rasisa/rasisa`.
It captures both visual design guidance and the operational rules that surfaced while fixing X card image issues and iterating on header artwork.

If the task actually generates or edits image files, use this skill together with `nano-banana`.

## Trigger Situations

Use this skill when the user asks for any of the following:

- X card or OGP images for RASHISA
- share images for results, campaigns, or launch posts
- note header images or social header/key visual assets
- revisions to existing share images after feedback
- fixes where X does not show the expected preview image

## Durable User Preferences

Treat these as standing rules for this repo unless the user explicitly overrides them:

- Commit and push directly to `main`. Do not create worktrees, side branches, or isolated deployment flows unless the user asks for them.
- It is acceptable to commit related design assets together. Do not leave useful image materials uncommitted when they belong to the current task.
- Do not introduce unrelated operational changes while working on share imagery.
- When the user points out a visual issue, treat it as a durable preference and encode it into the next revision instead of reintroducing the same pattern later.

## Design Rules For Share And Header Images

### Composition

- Default social share size is exactly `1200x630`.
- If an image tool outputs a near-match size, normalize it to `1200x630` before publishing.
- Prefer one dominant headline, one clear brand anchor, and a controlled number of supporting characters.
- Keep the visual hierarchy obvious at thumbnail size. The first read should be the headline, then the test name, then the brand.
- For RASHISA share art, a lively "sticker parade" composition works well: central message, MBTI characters around the edges, and the brand asset anchored low.

### Brand Asset Use

- When the user asks for the RASHISA image, use `public/hero-logo.png`.
- Keep the RASHISA hero/logo fully visible and unobstructed.
- If the logo is placed at the bottom, avoid unnecessary bars, chips, or framing shapes behind it unless the user explicitly wants them.
- Make the bottom logo large enough to read at feed-card size, but not so large that it competes with the headline.

### Typography And Messaging

- Use short, emotionally legible Japanese copy that reads cleanly on mobile.
- Avoid adding extra subtitles, helper lines, or descriptive copy unless the user asked for them.
- If the user requests a specific headline, preserve that wording exactly unless they ask for copy changes.
- Decorative type treatment is acceptable, but clarity wins over novelty.

### Character Use

- Use multiple MBTI characters when the concept calls for excitement or variety.
- Scatter characters around the perimeter so they frame the message instead of blocking it.
- Keep enough breathing room around the headline and test name.
- Prefer character placement that still works after export and crop normalization.

## X And OGP Technical Rules

- Use `summary_large_image` for X cards.
- Use absolute HTTPS image URLs for `og:image` and `twitter:image`.
- Use a representative share image, not a favicon or generic logo-only image.
- When the share image changes, bump the image version query parameter so X can fetch the new asset.
- When testing card refreshes, use a versioned or cache-busting share URL when appropriate.
- Existing X posts may continue showing stale cards because of X-side caching. New posts or refreshed URLs are the reliable validation path.

## Implementation Checklist

When shipping a new or revised share image:

1. Create or revise the image with the approved concept.
2. Ensure the final exported asset is exactly `1200x630`.
3. Replace the published image asset, usually `public/ogp/rashisa-share.png`, only after the user-approved visual direction is ready.
4. Bump the share image version string used by metadata generation.
5. Keep metadata changes isolated to the social-card path unless another change is strictly required.
6. Commit and push the image and metadata updates directly to `main`.
7. Deploy the current `main` build if the workflow requires a manual deploy.

## Verification Checklist

- Verify the live HTML returned to `Twitterbot` includes the expected `og:image`, `twitter:image`, `twitter:card`, and `og:url`.
- Verify the live image URL returns `200 OK`.
- Verify the live image dimensions are exactly `1200x630`.
- Run the relevant metadata tests and a production build before claiming success.
- When a user is checking a specific X post, distinguish between a stale cached post and a still-broken live page.

## Common Failure Patterns To Avoid

- Shipping a share image that is not exactly `1200x630`
- Forgetting to bump the cache-busting image version after changing the art
- Using relative image paths, favicon-like assets, or logo-only visuals for X cards
- Adding extra decorative elements that the user has already rejected
- Changing branching or deployment workflow in ways the user explicitly said not to use
- Declaring success based only on local files without checking the live `Twitterbot` response
