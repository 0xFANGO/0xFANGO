# fango.blog Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a minimalist personal website at fango.blog using Zola + zola-hacker theme with an emerald green color scheme.

**Architecture:** Static site built with Zola, using en9inerd/zola-hacker as a git submodule theme. Override SASS colors and key templates at the project level. Two content pages: About (homepage) and Projects. Deploy to Cloudflare Pages.

**Tech Stack:** Zola (static site generator), SCSS, HTML (Tera templates), Cloudflare Pages

**Spec:** `docs/superpowers/specs/2026-04-03-personal-website-design.md`

---

## File Map

| Action | File | Responsibility |
|--------|------|---------------|
| Create | `config.toml` | Site metadata, menu, social links, theme config |
| Create | `content/_index.md` | About/homepage content (renders at `/`) |
| Create | `content/projects.md` | Projects page (renders at `/projects`) |
| Create | `sass/_default_colors.scss` | Override theme accent from amber to emerald `#50c878` |
| Create | `sass/_svg-icons.scss` | Copied from theme (Zola can't resolve `../` in SASS imports) |
| Create | `sass/_primary-font.scss` | Copied from theme (same reason) |
| Create | `sass/_custom.scss` | Extra emerald-specific CSS tweaks (reserved for future use) |
| Create | `sass/main.scss` | Import theme SASS + custom overrides (spec deviation: spec only lists `_default_colors` and `_custom`, but `main.scss` is required to control the import chain) |
| Create | `templates/index.html` | Override: render `_index.md` content instead of blog list |
| Create | `templates/partials/footer.html` | Override: remove posts dependency, simple copyright |
| Create | `static/favicon.svg` | Emerald-themed SVG favicon |
| Create | `.gitignore` | Ignore `public/`, `.superpowers/` |
| Submodule | `themes/hacker` | zola-hacker theme |

---

### Task 1: Initialize Project Structure

**Files:**
- Create: `.gitignore`
- Submodule: `themes/hacker` → `https://github.com/en9inerd/zola-hacker.git`

- [ ] **Step 1: Create .gitignore**

```gitignore
public/
.superpowers/
```

- [ ] **Step 2: Add zola-hacker as git submodule**

Run: `cd /Users/fango/coding/fango/0xFANGO && git submodule add https://github.com/en9inerd/zola-hacker.git themes/hacker`

Expected: `themes/hacker/` directory created with theme files, `.gitmodules` updated.

- [ ] **Step 3: Verify theme structure exists**

Run: `ls themes/hacker/sass/_default_colors.scss themes/hacker/templates/base.html`

Expected: Both files exist.

- [ ] **Step 4: Commit**

```bash
git add .gitignore .gitmodules themes/hacker
git commit -m "feat: init zola project with zola-hacker theme submodule"
```

---

### Task 2: Override Color Scheme (SASS)

**Files:**
- Create: `sass/_default_colors.scss`
- Create: `sass/_svg-icons.scss` (copy from theme)
- Create: `sass/_primary-font.scss` (copy from theme)
- Create: `sass/_custom.scss`
- Create: `sass/main.scss`

The theme's `sass/main.scss` imports `_default_colors` as its first dependency. Zola's SASS compiler cannot resolve `../` paths outside the `sass/` directory, so we must copy `_svg-icons.scss` and `_primary-font.scss` from the theme into our project's `sass/` directory. By placing our own `sass/main.scss` at the project level, we take full control of the import chain.

- [ ] **Step 1: Create color override file**

Create `sass/_default_colors.scss`:

```scss
$apple-blossom: #ac4142;
$amber: #50c878;
$alto: #d0d0d0;
$bouquet: #dbbda3;
$chelsea-cucumber: #90a959;
$cod-grey: #151515;
$conifer: #b5e853;
$dove-grey: #666;
$gallery: #eaeaea;
$grey: #505050;
$light-grey: #999;
$gulf-stream: #75b5aa;
$hippie-blue: #6a9fb5;
$potters-clay: #8f5536;
$rajah: #f4bf75;
$raw-sienna: #d28445;
$silver-chalice: #aaa;
```

The key change: `$amber` is now `#50c878` (emerald) instead of `#ffbf00`. Every heading, border, and accent in the theme reads from `$amber`.

- [ ] **Step 2: Copy theme SASS dependencies**

Zola's SASS compiler cannot resolve `../` imports outside the `sass/` directory. Copy these files from the theme:

Run:
```bash
cp themes/hacker/sass/_svg-icons.scss sass/_svg-icons.scss
cp themes/hacker/sass/_primary-font.scss sass/_primary-font.scss
```

- [ ] **Step 3: Create custom styles file**

Create `sass/_custom.scss`:

```scss
// Reserved for future emerald-specific CSS tweaks.
// Heading glow is already handled in main.scss.
```

- [ ] **Step 4: Create project-level main.scss**

Create `sass/main.scss`. This file replaces the theme's `main.scss` entirely. Since we copied `_svg-icons.scss` and `_primary-font.scss` into our `sass/` directory, all imports resolve locally:

```scss
@import "default_colors";
@import "svg-icons";
@import "primary-font";

$body-background: $cod-grey !default;
$body-foreground: $gallery !default;
$header: $amber !default;
$blockquote-color: $silver-chalice !default;
$blockquote-border: $dove-grey !default;
$container-max-width: 1000px;

@mixin media-max-width($max-width) {
  @media (max-width: $max-width) {
    @content;
  }
}

body {
  margin: 0;
  padding: 0;
  background: $body-background 0 0;
  color: $body-foreground;
  font-size: 16px;
  line-height: 1.5;
  font-family: "JetBrains Mono", monospace;
  font-feature-settings:
    "calt" 0,
    "zero" 1,
    "cv12" 1,
    "cv18" 1,
    "cv19" 1,
    "cv20" 1;
}

.container {
  width: 90%;
  max-width: $container-max-width;
  margin: 0 auto;
}

h1, h2, h3, h4, h5, h6 {
  margin: 0 0 20px;
}

li {
  line-height: 1.4;
}

header {
  background: rgba(0, 0, 0, 0.1);
  width: 100%;
  border-bottom: 1px dashed $amber;
  padding: 20px 0;
  margin: 0 0 40px 0;
}

header h1 {
  font-size: 30px;
  line-height: 1.5;
  margin: 0 0 0 -40px;
  font-weight: bold;
  color: $amber;
  text-shadow:
    0 1px 1px rgba(0, 0, 0, 0.1),
    0 0 5px rgba(80, 200, 120, 0.1),
    0 0 10px rgba(80, 200, 120, 0.1);
  letter-spacing: -1px;

  @include media-max-width($container-max-width) {
    margin-left: 0;
  }
}

header h1:before {
  content: "./ ";
  font-size: 24px;
}

header h2 {
  font-size: 18px;
  font-weight: 300;
  color: $light-grey;
}

nav {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
  margin: 30px 0 20px 0;
}

.smaller {
  font-size: 0.95em;
}

main {
  width: 100%;
}

main img {
  max-width: 100%;
}

h1, h2, h3, h4, h5, h6 {
  font-weight: normal;
  color: $header;
  letter-spacing: -0.03em;
  text-shadow:
    0 1px 1px rgba(0, 0, 0, 0.1),
    0 0 5px rgba(80, 200, 120, 0.1),
    0 0 10px rgba(80, 200, 120, 0.1);
}

main h1 { font-size: 30px; }
main h2 { font-size: 24px; }
main h3 { font-size: 18px; }
main h4 { font-size: 16px; }

main h5 {
  font-size: 12px;
  text-transform: uppercase;
  margin: 0 0 5px 0;
}

main h6 {
  font-size: 12px;
  text-transform: uppercase;
  color: $light-grey;
  margin: 0 0 5px 0;
}

dt {
  font-style: italic;
  font-weight: bold;
}

ul li {
  list-style-type: ">> ";

  &::marker {
    color: $amber;
  }
}

blockquote {
  color: $blockquote-color;
  padding-left: 10px;
  border-left: 1px dotted $blockquote-border;
}

code:not(pre code) {
  background: #2b2c2f;
  padding: 0px 3px;
  margin: 0px -3px;
  color: $bouquet;
  border-radius: 2px;
}

pre {
  padding: 1rem;
  overflow: auto;
  border-radius: 2px;

  &[data-linenos] {
    padding: 1rem 0;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 0;

    td {
      padding: 0;

      &:nth-of-type(1) {
        text-align: center;
        user-select: none;
        width: 3.5rem;
      }
    }
  }

  mark {
    display: block;
    background-color: rgba(254, 252, 232, 0.9);
  }
}

table {
  width: 100%;
  margin: 0 0 20px 0;
}

th {
  border-bottom: 1px dashed $amber;
  padding: 5px 10px;
}

td {
  padding: 5px 10px;
}

hr {
  height: 0;
  border: 0;
  border-bottom: 1px dashed $amber;
  color: $amber;
}

.btn {
  display: inline-block;
  background: -webkit-linear-gradient(
    top,
    rgba(40, 40, 40, 0.3),
    rgba(35, 35, 35, 0.3) 50%,
    rgba(10, 10, 10, 0.3) 50%,
    rgba(0, 0, 0, 0.3)
  );
  padding: 8px 18px;
  border-radius: 50px;
  border: 2px solid rgba(0, 0, 0, 0.7);
  border-bottom: 2px solid rgba(0, 0, 0, 0.7);
  border-top: 2px solid rgba(0, 0, 0, 1);
  color: rgba(255, 255, 255, 0.8);
  font-family: Helvetica, Arial, sans-serif;
  font-size: 14px;
  text-decoration: none;
  text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.75);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

.btn:hover {
  background: -webkit-linear-gradient(
    top,
    rgba(40, 40, 40, 0.6),
    rgba(35, 35, 35, 0.6) 50%,
    rgba(10, 10, 10, 0.8) 50%,
    rgba(0, 0, 0, 0.8)
  );
}

.btn .icon {
  display: inline-block;
  width: 16px;
  height: 16px;
  vertical-align: sub;
  margin-right: 8px;
}

.btn-github .icon {
  opacity: 0.6;
  background: url("/images/blacktocat.png") 0 0 no-repeat;
}

a {
  color: #63c0f5;
  text-shadow: 0 0 5px rgba(104, 182, 255, 0.5);
  outline: none;
  text-decoration: none;
}

main, footer {
  a:hover, a:active {
    text-shadow: 0 0 5px rgba(104, 182, 255, 1);
  }

  a.btn:hover, a.btn:active {
    text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.75);
  }
}

#a-title h1 {
  & {
    text-decoration: none;
  }

  &:hover {
    text-shadow:
      0 1px 1px rgba(0, 0, 0, 0.3),
      0 0 5px rgba(80, 200, 120, 0.3),
      0 0 10px rgba(80, 200, 120, 0.3);
  }
}

.page-info {
  margin-bottom: 2em;
}

.page-info span {
  font-weight: normal;
  color: $amber;
  letter-spacing: -0.03em;
  text-shadow:
    0 1px 1px rgba(0, 0, 0, 0.1),
    0 0 5px rgba(80, 200, 120, 0.1),
    0 0 10px rgba(80, 200, 120, 0.1);
}

.pages > .page {
  padding-bottom: 2em;
  margin-bottom: 1.8em;
  border-bottom: 1px dashed $amber;
}

.pages > .page:last-child {
  padding-bottom: 1em;
  border-bottom: none;
}

.page {
  .page-footer {
    text-align: right;
  }

  .read-more {
    text-transform: uppercase;
    margin-left: 15px;
  }
}

.header-container {
  display: flex;
  justify-content: space-between;
}

.improve {
  font-size: 14px;
  white-space: nowrap;
  margin-left: 1.5rem;

  a {
    color: $light-grey;
  }
}

@media screen and (max-width: 568px) {
  .hide-on-mobiles {
    display: none !important;
  }
}

time {
  opacity: 0.6;
}

.page time {
  display: block;
}

time.page-time {
  margin-top: 1em;
}

.pagination {
  padding-top: 20px;
  text-align: center;
  border-top: 1px dashed $amber;
  color: $amber;

  .previous-page {
    margin-right: 2em;
  }

  .next-page {
    margin-left: 2em;
  }
}

footer {
  margin: 3.5rem 0 2rem;
  text-align: center;
}

.copyright {
  color: $light-grey;
  display: block;
  margin-top: 15px;
  font-size: 14px;
}

// Import custom styles last
@import "custom";
```

**Note:** This copies the theme's `main.scss` verbatim with emerald-adjusted `rgba()` glow values (changed from `255, 191, 0` amber to `80, 200, 120` emerald). The `@import "custom"` at the end pulls in our extra tweaks. The `_default_colors.scss` override changes `$amber` to `#50c878`. The `_svg-icons.scss` and `_primary-font.scss` are copied from the theme since Zola can't resolve `../` paths in SASS imports.

- [ ] **Step 5: Verify SASS compiles**

Run: `cd /Users/fango/coding/fango/0xFANGO && zola build 2>&1 | head -20`

Expected: No SASS compilation errors. (Site build may fail due to missing config/content — that's fine at this stage.)

- [ ] **Step 6: Commit**

```bash
git add sass/
git commit -m "feat: add emerald green color scheme overriding theme SASS"
```

---

### Task 3: Write config.toml

**Files:**
- Create: `config.toml`

- [ ] **Step 1: Create config.toml**

```toml
base_url = "https://fango.blog"
title = "0xFANGO"
description = "Full Stack Engineer × AI Builder"
author = "0xFANGO"
compile_sass = true
minify_html = true
theme = "hacker"
generate_feeds = false

[markdown]
render_emoji = true
bottom_footnotes = true
external_links_target_blank = true

[markdown.highlighting]
theme = "github-dark"

[extra]
edit_page = false
language_code = "en-US"
monitor = false
opengraph = true
title_separator = "|"

menu = [
  { url = "/", name = "About" },
  { url = "projects", name = "Projects" },
]

social_links = [
  { platform = "github", user_id = "0xFANGO" },
  { platform = "twitter", user_id = "TODO" },
  { platform = "linkedin", user_id = "TODO" },
]

[extra.github]
username = "0xFANGO"
repo = "0xFANGO"
```

**Important:** The zola-hacker theme uses `platform` + `user_id` format for social links (not `icon`/`url`). Supported platforms are defined in `themes/hacker/data/socials.yml`: email, github, linkedin, twitter, facebook, instagram, pinterest, stackoverflow, youtube, telegram, keyoxide, feed.

Replace `"TODO"` values with actual Twitter and LinkedIn user IDs before deploying.

- [ ] **Step 2: Commit**

```bash
git add config.toml
git commit -m "feat: add zola config with site metadata and menu"
```

---

### Task 4: Override Templates

**Files:**
- Create: `templates/index.html`
- Create: `templates/partials/footer.html`

The theme's default `index.html` renders paginated blog posts. We need it to render `_index.md` content as the About page instead. The theme's `footer.html` calls `get_section(path="posts/_index.md")` which will fail without a posts section — override it with a simple copyright footer.

- [ ] **Step 1: Create templates directory**

Run: `mkdir -p /Users/fango/coding/fango/0xFANGO/templates/partials`

- [ ] **Step 2: Create index.html override**

Create `templates/index.html`:

```html
{%- extends "base.html" %}

{%- block seo -%}
  {{- super() }}

  {%- set title = config.title %}
  {%- if config.description %}
    {%- set title_addition = title_separator ~ config.description %}
  {%- else %}
    {%- set title_addition = "" %}
  {%- endif %}

  {{- macros::seo(title=title, title_addition=title_addition, description=config.description, is_home=true) }}
{%- endblock seo %}

{%- block content %}
<article class="page">
  <div class="entry">
    {{ section.content | safe }}
  </div>
</article>
{%- endblock %}
```

This renders `content/_index.md` body as a simple page — no pagination, no post list, no page-info metadata.

- [ ] **Step 3: Create footer.html override**

Create `templates/partials/footer.html`:

```html
{%- include "partials/svg-icons.html" -%}
<span class="copyright">&copy; {{ now() | date(format="%Y") }} {{ config.author }}</span>
```

This removes the dependency on `posts/_index.md` section and uses a simple year + author copyright line. The `config.author` is set to `"0xFANGO"` in config.toml to match the spec's `© 2026 0xFANGO`.

- [ ] **Step 4: Commit**

```bash
git add templates/
git commit -m "feat: override index and footer templates for static homepage"
```

---

### Task 5: Write Homepage Content

**Files:**
- Create: `content/_index.md`

- [ ] **Step 1: Create _index.md**

Create `content/_index.md`:

```markdown
+++
title = "About"
sort_by = "none"
+++

Hey, I'm Fango. Full stack engineer and AI builder.

I work across the stack — from React frontends to Python backends, with a focus on shipping AI-powered tools. I like building things that work well and look good doing it.

### Stack

- TypeScript
- JavaScript
- React
- Next.js
- Vue.js
- Tailwind CSS
- Vite

- Anthropic
- Google Gemini
- OpenAI

- Node.js
- Python
- pnpm
- Docker
- Cloudflare
- Git

### Work

Full Stack Engineer

`0x` prefix is not a typo. I like hex.
```

- [ ] **Step 2: Commit**

```bash
git add content/_index.md
git commit -m "feat: add about page content as homepage"
```

---

### Task 6: Write Projects Page

**Files:**
- Create: `content/projects.md`

- [ ] **Step 1: Create projects.md**

Create `content/projects.md`:

```markdown
+++
title = "Projects"
path = "projects"

[extra]
no_page_info = true
+++

### [fango-cli](https://github.com/0xFANGO/fango-cli)
TypeScript — A CLI tool for personal workflows and automation.

---

### [fango-slides](https://github.com/0xFANGO/fango-slides)
Vue / Slidev — Presentation slides for talks and interviews.

---

### [fango-media](https://github.com/0xFANGO/fango-media)
Media — Media assets and content collection.

---

### [0xFANGO](https://github.com/0xFANGO)
Profile — GitHub profile and personal branding.
```

The `path = "projects"` frontmatter makes this render at `/projects` instead of `/pages/projects`. `no_page_info = true` hides the date/tags metadata that the theme's `page.html` template shows by default.

- [ ] **Step 2: Commit**

```bash
git add content/projects.md
git commit -m "feat: add projects page"
```

---

### Task 7: Add Favicon

**Files:**
- Create: `static/favicon.svg`

- [ ] **Step 1: Create emerald-themed SVG favicon**

Create `static/favicon.svg`:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="4" fill="#151515"/>
  <text x="16" y="23" font-family="monospace" font-size="20" font-weight="bold" fill="#50c878" text-anchor="middle">F</text>
</svg>
```

Simple: dark background square with an emerald "F" in monospace.

- [ ] **Step 2: Commit**

```bash
git add static/favicon.svg
git commit -m "feat: add emerald SVG favicon"
```

---

### Task 8: Build and Verify Locally

- [ ] **Step 1: Install Zola if not present**

Run: `which zola || brew install zola`

- [ ] **Step 2: Initialize git submodules**

Run: `cd /Users/fango/coding/fango/0xFANGO && git submodule update --init --recursive`

- [ ] **Step 3: Build the site**

Run: `cd /Users/fango/coding/fango/0xFANGO && zola build`

Expected: Clean build with no errors. Output in `public/` directory.

If SASS errors occur, verify that `_svg-icons.scss` and `_primary-font.scss` were correctly copied to the project `sass/` directory in Task 2.

- [ ] **Step 4: Serve locally and verify**

Run: `cd /Users/fango/coding/fango/0xFANGO && zola serve`

Expected: Dev server at `http://127.0.0.1:1111`. Verify:
1. Homepage shows About content with emerald green headings/borders
2. Navigation has "About" and "Projects" links
3. `/projects` page renders correctly
4. Footer shows social icons and copyright
5. `./ ` prefix on site title
6. `>> ` list markers in emerald

- [ ] **Step 5: Fix any issues found during verification**

Common issues to check:
- SASS import paths if compilation fails
- Template variable names if Tera rendering errors
- Social link format mismatch with theme expectations
- Missing font files (JetBrains Mono loaded via `_primary-font.scss`)

- [ ] **Step 6: Commit any fixes**

```bash
git add -A
git commit -m "fix: address build/render issues from local verification"
```

(Skip this step if no fixes were needed.)

---

### Task 9: Cloudflare Pages Setup

This task is done manually in the Cloudflare dashboard, not automated.

- [ ] **Step 1: Push repo to GitHub**

Ensure the repo is pushed to `github.com/0xFANGO/0xFANGO` (or a new repo like `fango-blog`).

- [ ] **Step 2: Create Cloudflare Pages project**

In Cloudflare dashboard → Pages → Create a project → Connect to Git:
- Select the GitHub repository
- Framework preset: None (or Zola if available)
- Build command: `zola build`
- Build output directory: `public`
- Environment variable: `ZOLA_VERSION` = `0.19.2` (or latest)

- [ ] **Step 3: Configure custom domain**

In Cloudflare Pages project settings → Custom domains:
- Add `fango.blog`
- Follow DNS configuration instructions (if domain is already on Cloudflare, this is automatic)

- [ ] **Step 4: Verify deployment**

Visit `https://fango.blog` and verify the site matches local preview.

- [ ] **Step 5: Document deployment in README**

Update project README with deployment info if desired (optional — not required).
