# fango.blog — Personal Website Design Spec

## Overview

A minimalist personal website for Fango (0xFANGO), built with Zola using the zola-hacker theme as a base, customized with an emerald green color scheme. Deployed to Cloudflare Pages at fango.blog.

## Goals

- Simple, fast, static personal homepage
- Hacker terminal aesthetic with a refined emerald green palette
- Two pages: About (homepage) and Projects
- Social links in footer

## Tech Stack

- **Static site generator:** Zola
- **Base theme:** zola-hacker (en9inerd/zola-hacker)
- **Deployment:** Cloudflare Pages
- **Domain:** fango.blog

## Color Scheme

Override zola-hacker's default amber palette with emerald green:

| Role | Color | Hex |
|------|-------|-----|
| Background | Cod grey | `#151515` |
| Primary accent | Emerald | `#50c878` |
| Body text | Gallery | `#eaeaea` |
| Secondary text | Light grey | `#999999` |
| Links | Light blue | `#63c0f5` |
| Code inline | Bouquet on dark | `#dbbda3` on `#2b2c2f` |
| Blockquote border | Dove grey | `#666666` |

## Typography

- **Font:** JetBrains Mono (monospace), same as zola-hacker default
- **Body:** 16px, line-height 1.5
- **Headings:** emerald with subtle glow (`text-shadow: 0 0 5px rgba(80,200,120,0.15)`)

## Visual Elements

- **Site title prefix:** `./ ` (terminal prompt style)
- **List markers:** `>> ` in emerald (zola-hacker default style)
- **Borders:** 1px dashed in emerald
- **Links:** light blue with blue glow on hover
- **Social links:** subtle opacity, colored glow on hover per platform

## Site Structure

### Header (shared)

```
./ 0xFANGO
Full Stack Engineer × AI Builder

     About   Projects
```

- Site title in emerald with glow
- Subtitle in light grey
- Centered navigation links in blue
- Bottom border: 1px dashed emerald

### Page: About (Homepage, `/`)

The landing page and default route. Content lives in `content/_index.md` directly — this is how Zola serves the root `/` path. Contains:

1. **Intro paragraph** — brief self-introduction
2. **Stack section** — tech stack listed with `>>` markers, grouped by category:
   - Frontend: TypeScript, React, Next.js, Vue, Tailwind
   - AI: Anthropic, OpenAI, Gemini
   - Infra: Node.js, Python, Docker, Cloudflare, Git
3. **Work section** — current role, the "0x prefix" note

### Page: Projects (`/projects`)

A single Markdown page at `content/projects.md` with manually written project entries. This keeps it simple — no need for a Zola section with individual project files, since the list is short and curated.

Each project entry contains:

- **Project name** — clickable link (blue with glow)
- **Language/tech tag** — right-aligned in grey
- **Description** — one line in secondary text

Entries separated by dashed emerald borders. Projects to include (initial):
- fango-cli (TypeScript)
- fango-slides (Vue / Slidev)
- fango-media (Media)
- 0xFANGO (Profile)

### Footer (shared)

- Social links: GitHub, X, LinkedIn (expandable)
- Copyright: `© 2026 0xFANGO`
- Top border: 1px dashed emerald

## Implementation Approach

### Theme Customization

Add zola-hacker as a git submodule, then override at the project level. Zola allows overriding theme SASS files by placing identically named files in the project's `sass/` directory — these take precedence over the theme's versions.

1. **`sass/_default_colors.scss`** — place in project root `sass/` to override the theme's version. Change `$amber: #ffbf00` to `$amber: #50c878`. The theme uses `$amber` as the primary accent variable throughout, so just changing the value is sufficient.
2. **`sass/_custom.scss`** — add heading glow (`text-shadow`) and any other emerald-specific CSS tweaks. Import this from a project-level `sass/main.scss` that first imports the theme's main.scss, then appends custom styles.
3. **`config.toml`** — configure site metadata, navigation menu, social links.
4. **Content files** — write About (`_index.md`) and Projects page in Markdown.

**Note:** If Zola's SASS override doesn't work cleanly with the theme's `@import` chain, fall back to forking the theme repo and modifying files directly.

### Key Config Changes (config.toml)

```toml
base_url = "https://fango.blog"
title = "0xFANGO"
description = "Full Stack Engineer × AI Builder"
theme = "hacker"

[extra]
menu = [
  { url = "/", name = "About" },
  { url = "projects", name = "Projects" },
]
social_links = [
  { icon = "github", url = "https://github.com/0xFANGO", color = "/EAEAEA", shadow = "#EAEAEA" },
  { icon = "x", url = "https://x.com/...", color = "/EAEAEA", shadow = "#EAEAEA", size = "18" },
  { brand = "linkedin", url = "https://linkedin.com/in/...", color = "/0A66C2", shadow = "#0A66C2" },
]
```

### Cloudflare Pages Deployment

- Connect GitHub repo to Cloudflare Pages
- Build command: `zola build`
- Output directory: `public`
- Custom domain: fango.blog

## File Structure

```
fango.blog/
├── config.toml
├── content/
│   ├── _index.md          # About page (homepage at /)
│   └── projects.md        # Projects page (at /projects)
├── static/
│   └── favicon.svg        # Simple emerald-themed SVG favicon
├── sass/
│   ├── _default_colors.scss   # Override theme colors (emerald)
│   └── _custom.scss           # Heading glow, extra tweaks
└── themes/
    └── hacker/            # zola-hacker as git submodule
```

## What's NOT in Scope

- Blog / posts functionality
- Dark/light mode toggle (dark only)
- Analytics
- Contact form
- i18n / multi-language
- Custom JavaScript beyond what the theme provides
