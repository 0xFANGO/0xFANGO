# npx fango — Terminal Business Card

**Date:** 2026-04-02
**Status:** Approved

## Overview

Create an npm package `fango` that renders an interactive terminal business card when anyone runs `npx fango`. Combines structured resume content (work experience, projects) with interactive link selection, built with Ink + React.

Inspired by `npx litomore` (Ink + React resume) and `npx sindresorhus` (interactive links).

## Goals

- Run `npx fango` to display a polished terminal card with personal info, work experience, projects, and interactive links
- Data-driven: all personal content in a single `data.ts` file for easy updates
- Component-based with Ink + React for maintainability and future extensibility

## Non-Goals (Future)

- Tinker ASCII art avatar
- Tab-switchable panels
- `--json` flag for machine-readable output

## Technical Stack

- **TypeScript** — type safety
- **Ink 5 + React 18** — terminal UI rendering
- **ink-select-input** — interactive link selection
- **open** — open links in default browser
- **tsup** — build & bundle

## Project Structure

This is a **new standalone project** (separate from the 0xFANGO profile repo).

```
fango-cli/
├── source/
│   ├── cli.tsx              # Entry point: #!/usr/bin/env node, render(<App/>)
│   ├── app.tsx              # Root component, composes all sections
│   ├── components/
│   │   ├── header.tsx       # Name + title + tagline
│   │   ├── experience.tsx   # Work experience section
│   │   ├── projects.tsx     # Projects section
│   │   └── links.tsx        # Interactive link selector
│   └── data.ts              # All personal data in one place
├── package.json
├── tsconfig.json
└── README.md
```

## Terminal Layout

```
╭──────────────────────────────────────────────────╮
│                                                  │
│   Fango                                          │
│   Full Stack Engineer & AI Builder               │
│   The 0x is intentional — hex enthusiast.        │
│                                                  │
│ ╭─ Experience ─────────────────────────────────╮ │
│ │                                              │ │
│ │  MarsWave AI          Full Stack Engineer    │ │
│ │  Beijing              2025 - Present         │ │
│ │                                              │ │
│ │  Previous Co.         Frontend Engineer      │ │
│ │  Somewhere            2023 - 2025            │ │
│ │                                              │ │
│ ╰──────────────────────────────────────────────╯ │
│                                                  │
│ ╭─ Projects ──────────────────────────────────╮  │
│ │                                              │ │
│ │  project-name    ·  A short description      │ │
│ │  another-proj    ·  Does cool things         │ │
│ │                                              │ │
│ ╰──────────────────────────────────────────────╯ │
│                                                  │
│   Use ↑↓ arrows to select, Enter to open:       │
│                                                  │
│   ❯ GitHub       github.com/0xFANGO             │
│     Twitter      @...                            │
│     Website      fango.dev                       │
│     Email        ...                             │
│                                                  │
╰──────────────────────────────────────────────────╯
```

## Color Scheme

| Element | Style |
|---------|-------|
| Name | bold + bright white |
| Title | cyan |
| Section titles (Experience / Projects) | red bold |
| Company / project names | bold white |
| Dates / descriptions | dim gray |
| Active link | cyan bold |
| Box borders | round style, default terminal color |

## Interaction

- All content renders immediately on launch
- Bottom links area supports up/down arrow key navigation
- Press Enter to open selected link in default browser
- Press `q` or `Ctrl+C` to exit

## Data Layer (`data.ts`)

All personal content is centralized in one file. Updating the card means editing only this file:

```ts
export const profile = {
  name: 'Fango',
  title: 'Full Stack Engineer & AI Builder',
  tagline: 'The 0x is intentional — hex enthusiast.',
};

export const experiences: Experience[] = [
  { company: 'MarsWave AI', location: 'Beijing', title: 'Full Stack Engineer', from: '2025', to: 'Present' },
  // ... more entries
];

export const projects: Project[] = [
  { name: 'project-name', description: 'A short description' },
  // ... more entries
];

export const links: Link[] = [
  { label: 'GitHub', value: 'https://github.com/0xFANGO' },
  { label: 'Twitter', value: 'https://x.com/...' },
  { label: 'Website', value: 'https://fango.dev' },
  // ... more entries
];
```

## Component Design

### `<Header>`
Renders name (bold white), title (cyan), and tagline (dim). No border — sits at the top of the outer box.

### `<Experience experiences={[...]}/>`
Round-bordered box with "Experience" title in red bold. Each entry shows company + title on the left, location + date range on the right, using `justifyContent: 'space-between'`.

### `<Projects projects={[...]}/>`
Round-bordered box with "Projects" title in red bold. Each entry shows project name (bold) followed by a dot separator and description (dim).

### `<Links links={[...]}/>`
Uses `ink-select-input` for arrow-key navigation. Each item shows label (bold when selected) and URL. On select, calls `open(url)` to launch browser.

### `<App/>`
Wraps everything in an outer `<Box>` with round border, `flexDirection: 'column'`, and padding. Composes Header, Experience, Projects, Links in order.

## package.json

```json
{
  "name": "fango",
  "version": "1.0.0",
  "description": "Fango's terminal business card — run npx fango",
  "type": "module",
  "bin": {
    "fango": "./dist/cli.js"
  },
  "files": ["dist"],
  "scripts": {
    "build": "tsup source/cli.tsx --format esm --target node18",
    "dev": "tsx source/cli.tsx"
  },
  "keywords": ["cli", "card", "terminal", "npx"],
  "license": "MIT"
}
```

## Build & Publish

1. Build: `pnpm build` (tsup compiles TypeScript to dist/)
2. Test locally: `node dist/cli.js` or `pnpm dev`
3. Publish: `npm publish` (requires npm account with `fango` name available)
4. Anyone can then run: `npx fango`
