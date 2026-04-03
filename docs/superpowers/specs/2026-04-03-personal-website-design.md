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

The landing page and default route. Contains:

1. **Intro paragraph** — brief self-introduction
2. **Stack section** — tech stack listed with `>>` markers, grouped by category:
   - Frontend: TypeScript, React, Next.js, Vue, Tailwind
   - AI: Anthropic, OpenAI, Gemini
   - Infra: Node.js, Python, Docker, Cloudflare, Git
3. **Work section** — current role, the "0x prefix" note

### Page: Projects (`/projects`)

Simple list layout, each project entry contains:

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

Fork or submodule zola-hacker, then override:

1. **`sass/_default_colors.scss`** — replace `$amber: #ffbf00` with `$amber: #50c878` (the theme uses `$amber` as the primary accent variable throughout, so renaming is unnecessary — just change the value)
2. **`config.toml`** — configure site metadata, navigation menu, social links
3. **Content files** — write About and Projects pages in Markdown

### Key Config Changes (config.toml)

```toml
base_url = "https://fango.blog"
title = "0xFANGO"
description = "Full Stack Engineer × AI Builder"
theme = "hacker"

[extra]
menu = [
  { url = "about", name = "About" },
  { url = "projects", name = "Projects" },
]
social_links = [
  { icon = "github", url = "https://github.com/0xFANGO", ... },
  # etc.
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
│   ├── _index.md          # redirect or landing
│   └── pages/
│       ├── about.md       # About page (homepage)
│       └── projects.md    # Projects page
├── static/
│   └── favicon.svg
├── sass/
│   └── _default_colors.scss   # emerald color override
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
