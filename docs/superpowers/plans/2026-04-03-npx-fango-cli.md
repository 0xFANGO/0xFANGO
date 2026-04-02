# npx fango CLI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publish an npm package `fango` that renders an interactive terminal business card via `npx fango`.

**Architecture:** Ink 5 + React 18 terminal app with component-based layout. A centralized `data.ts` holds all personal content. Components render header, work experience, projects, and an interactive link selector. tsup bundles everything (including deps) into a single ESM file with shebang for `npx` execution.

**Tech Stack:** TypeScript, Ink 5, React 18, ink-select-input, open, tsup

**Spec:** `docs/superpowers/specs/2026-04-02-npx-fango-card-design.md`

---

## File Map

All files are created in a new project at `/Users/fango/coding/fango/fango-cli/`.

| File | Responsibility |
|------|---------------|
| `package.json` | Package metadata, deps, scripts, bin entry |
| `tsconfig.json` | TypeScript config with JSX support for Ink |
| `tsup.config.ts` | Build config: ESM, shebang banner, bundle all deps |
| `source/data.ts` | All personal data: profile, experiences, projects, links + type definitions |
| `source/components/header.tsx` | Renders name (bold white), title (cyan), tagline (dim) |
| `source/components/experience.tsx` | Round-bordered section with work history entries |
| `source/components/projects.tsx` | Round-bordered section with project list |
| `source/components/links.tsx` | Interactive link selector with open/debounce/feedback |
| `source/app.tsx` | Root component composing all sections in outer box |
| `source/cli.tsx` | Entry point: imports App, calls `render(<App/>)` |

---

## Task 1: Project Scaffold

**Files:**
- Create: `package.json`
- Create: `tsconfig.json`
- Create: `tsup.config.ts`

- [ ] **Step 1: Create project directory and init**

```bash
mkdir -p /Users/fango/coding/fango/fango-cli
cd /Users/fango/coding/fango/fango-cli
git init
```

- [ ] **Step 2: Create package.json**

```json
{
  "name": "fango",
  "version": "1.0.0",
  "description": "Fango's terminal business card — run npx fango",
  "type": "module",
  "bin": {
    "fango": "./dist/cli.js"
  },
  "files": [
    "dist"
  ],
  "engines": {
    "node": ">=18"
  },
  "scripts": {
    "build": "tsup",
    "dev": "tsx source/cli.tsx",
    "prepublishOnly": "pnpm build"
  },
  "keywords": [
    "cli",
    "card",
    "terminal",
    "npx"
  ],
  "license": "MIT"
}
```

- [ ] **Step 3: Create tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "dist",
    "rootDir": "source"
  },
  "include": ["source"]
}
```

- [ ] **Step 4: Create tsup.config.ts**

```ts
import {defineConfig} from 'tsup';

export default defineConfig({
	entry: ['source/cli.tsx'],
	format: ['esm'],
	target: 'node18',
	banner: {js: '#!/usr/bin/env node'},
	noExternal: [/(.*)/],
});
```

- [ ] **Step 5: Install dependencies**

```bash
cd /Users/fango/coding/fango/fango-cli
pnpm add ink@^5 react@^18 ink-select-input@^6 open@^10
pnpm add -D tsup@^8 tsx@^4 typescript@^5 @types/react@^18
```

- [ ] **Step 6: Create .gitignore**

```
node_modules/
dist/
```

- [ ] **Step 7: Verify build toolchain works**

Create a minimal `source/cli.tsx`:

```tsx
console.log('fango-cli scaffold works');
```

Run: `cd /Users/fango/coding/fango/fango-cli && pnpm build`
Expected: `dist/cli.js` is created with shebang `#!/usr/bin/env node` at top.

Run: `node dist/cli.js`
Expected: prints "fango-cli scaffold works"

- [ ] **Step 8: Commit**

```bash
git add -A
git commit -m "init: scaffold fango-cli with Ink + React + tsup"
```

---

## Task 2: Data Layer

**Files:**
- Create: `source/data.ts`

- [ ] **Step 1: Create data.ts with types and all personal data**

```ts
export interface Experience {
	company: string;
	location: string;
	title: string;
	from: string;
	to: string;
}

export interface Project {
	name: string;
	description: string;
}

export interface Link {
	label: string;
	href: string;
	display: string;
}

export const profile = {
	name: 'Fango',
	title: 'Full Stack Engineer & AI Builder',
	tagline: 'The 0x is intentional — hex enthusiast.',
};

export const experiences: Experience[] = [
	{
		company: 'MarsWave AI',
		location: 'Beijing',
		title: 'Full Stack Engineer',
		from: '2025',
		to: 'Present',
	},
];

export const projects: Project[] = [
	{name: 'fango-cli', description: 'This terminal card you\'re looking at'},
];

export const links: Link[] = [
	{label: 'GitHub', href: 'https://github.com/0xFANGO', display: 'github.com/0xFANGO'},
	{label: 'Website', href: 'https://fango.dev', display: 'fango.dev'},
];
```

Note: Fango will fill in real data later. Use placeholder entries that are structurally correct.

- [ ] **Step 2: Verify it compiles**

Run: `cd /Users/fango/coding/fango/fango-cli && pnpm build`
Expected: builds without type errors.

- [ ] **Step 3: Commit**

```bash
git add source/data.ts
git commit -m "feat: add data layer with types and placeholder content"
```

---

## Task 3: Header Component

**Files:**
- Create: `source/components/header.tsx`

- [ ] **Step 1: Create header.tsx**

```tsx
import {Box, Text} from 'ink';
import type {FC} from 'react';

interface HeaderProps {
	name: string;
	title: string;
	tagline: string;
}

export const Header: FC<HeaderProps> = ({name, title, tagline}) => (
	<Box flexDirection="column" paddingBottom={1}>
		<Text bold color="white">
			{name}
		</Text>
		<Text color="cyan">{title}</Text>
		<Text dimColor>{tagline}</Text>
	</Box>
);
```

- [ ] **Step 2: Verify it compiles**

Run: `cd /Users/fango/coding/fango/fango-cli && pnpm build`
Expected: no errors (component is not yet wired to cli.tsx — that's fine, tsup only bundles the entry point).

- [ ] **Step 3: Commit**

```bash
git add source/components/header.tsx
git commit -m "feat: add Header component"
```

---

## Task 4: Experience Component

**Files:**
- Create: `source/components/experience.tsx`

- [ ] **Step 1: Create experience.tsx**

A helper `truncate` function is needed by this and other components. Define it inline here (it's 3 lines, not worth a separate file).

```tsx
import {Box, Text} from 'ink';
import type {FC} from 'react';
import type {Experience as ExperienceType} from '../data.js';

function truncate(str: string, max: number): string {
	return str.length > max ? str.slice(0, max - 1) + '…' : str;
}

interface ExperienceProps {
	experiences: ExperienceType[];
}

export const Experience: FC<ExperienceProps> = ({experiences}) => (
	<Box
		flexDirection="column"
		borderStyle="round"
		paddingX={1}
	>
		<Box marginBottom={1}>
			<Text bold color="red">
				Experience
			</Text>
		</Box>
		{experiences.map((exp) => (
			<Box key={`${exp.company}-${exp.from}`} flexDirection="column" marginBottom={1}>
				<Box justifyContent="space-between">
					<Text bold>{truncate(exp.company, 20)}</Text>
					<Text>{truncate(exp.title, 22)}</Text>
				</Box>
				<Box justifyContent="space-between">
					<Text dimColor>{exp.location}</Text>
					<Text dimColor>
						{exp.from} – {exp.to}
					</Text>
				</Box>
			</Box>
		))}
	</Box>
);
```

- [ ] **Step 2: Verify it compiles**

Run: `cd /Users/fango/coding/fango/fango-cli && pnpm build`
Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add source/components/experience.tsx
git commit -m "feat: add Experience component with truncation"
```

---

## Task 5: Projects Component

**Files:**
- Create: `source/components/projects.tsx`

- [ ] **Step 1: Create projects.tsx**

```tsx
import {Box, Text} from 'ink';
import type {FC} from 'react';
import type {Project} from '../data.js';

function truncate(str: string, max: number): string {
	return str.length > max ? str.slice(0, max - 1) + '…' : str;
}

interface ProjectsProps {
	projects: Project[];
}

export const Projects: FC<ProjectsProps> = ({projects}) => (
	<Box
		flexDirection="column"
		borderStyle="round"
		paddingX={1}
	>
		<Box marginBottom={1}>
			<Text bold color="red">
				Projects
			</Text>
		</Box>
		{projects.map((proj) => (
			<Box key={proj.name} gap={1}>
				<Text bold>{proj.name}</Text>
				<Text dimColor>·</Text>
				<Text dimColor>{truncate(proj.description, 30)}</Text>
			</Box>
		))}
	</Box>
);
```

- [ ] **Step 2: Verify it compiles**

Run: `cd /Users/fango/coding/fango/fango-cli && pnpm build`
Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add source/components/projects.tsx
git commit -m "feat: add Projects component"
```

---

## Task 6: Links Component (Interactive)

**Files:**
- Create: `source/components/links.tsx`

This is the most complex component — handles interaction, debounce, open with fallback, and success feedback.

- [ ] **Step 1: Create links.tsx**

```tsx
import {Box, Text, useInput} from 'ink';
import type {FC} from 'react';
import {useState, useCallback, useRef} from 'react';
import open from 'open';
import type {Link} from '../data.js';

function truncate(str: string, max: number): string {
	return str.length > max ? str.slice(0, max - 1) + '…' : str;
}

interface LinksProps {
	links: Link[];
}

export const Links: FC<LinksProps> = ({links}) => {
	const [selectedIndex, setSelectedIndex] = useState(0);
	const [successHint, setSuccessHint] = useState(false);
	const [failedUrl, setFailedUrl] = useState<string | null>(null);
	const lastOpenTime = useRef(0);

	const handleSelect = useCallback(async () => {
		const now = Date.now();
		if (now - lastOpenTime.current < 500) return;
		lastOpenTime.current = now;

		const link = links[selectedIndex]!;
		try {
			await open(link.href);
			setSuccessHint(true);
			setFailedUrl(null);
			setTimeout(() => setSuccessHint(false), 1000);
		} catch {
			setSuccessHint(false);
			setFailedUrl(link.href);
		}
	}, [links, selectedIndex]);

	useInput((input, key) => {
		if (key.upArrow) {
			setSelectedIndex((i) => (i > 0 ? i - 1 : links.length - 1));
			setSuccessHint(false);
		} else if (key.downArrow) {
			setSelectedIndex((i) => (i < links.length - 1 ? i + 1 : 0));
			setSuccessHint(false);
		} else if (key.return) {
			void handleSelect();
		}
	});

	return (
		<Box flexDirection="column" paddingTop={1}>
			<Text dimColor>Use ↑↓ arrows to select, Enter to open:</Text>
			<Box flexDirection="column" paddingTop={1}>
				{links.map((link, index) => {
					const isSelected = index === selectedIndex;
					return (
						<Box key={link.label} gap={1}>
							<Text color={isSelected ? 'cyan' : undefined}>
								{isSelected ? '❯' : ' '}
							</Text>
							<Text bold={isSelected} color={isSelected ? 'cyan' : undefined}>
								{link.label}
							</Text>
							<Text dimColor>{truncate(link.display, 28)}</Text>
							{isSelected && successHint && (
								<Text dimColor> Opened!</Text>
							)}
						</Box>
					);
				})}
			</Box>
			{failedUrl && (
				<Box paddingTop={1}>
					<Text dimColor>Could not open — copy this URL: </Text>
					<Text color="yellow">{failedUrl}</Text>
				</Box>
			)}
		</Box>
	);
};
```

- [ ] **Step 2: Verify it compiles**

Run: `cd /Users/fango/coding/fango/fango-cli && pnpm build`
Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add source/components/links.tsx
git commit -m "feat: add interactive Links component with debounce and feedback"
```

---

## Task 7: App Component + CLI Entry Point

**Files:**
- Create: `source/app.tsx`
- Modify: `source/cli.tsx` (replace scaffold placeholder)

- [ ] **Step 1: Create app.tsx**

```tsx
import {Box, useApp, useInput} from 'ink';
import type {FC} from 'react';
import {profile, experiences, projects, links} from './data.js';
import {Header} from './components/header.js';
import {Experience} from './components/experience.js';
import {Projects} from './components/projects.js';
import {Links} from './components/links.js';

export const App: FC = () => {
	const {exit} = useApp();

	useInput((input) => {
		if (input === 'q') {
			exit();
		}
	});

	return (
		<Box
			flexDirection="column"
			borderStyle="round"
			paddingX={2}
			paddingY={1}
			width={54}
		>
			<Header
				name={profile.name}
				title={profile.title}
				tagline={profile.tagline}
			/>
			<Experience experiences={experiences} />
			<Projects projects={projects} />
			<Links links={links} />
		</Box>
	);
};
```

- [ ] **Step 2: Replace cli.tsx with real entry point**

```tsx
import {render} from 'ink';
import {App} from './app.js';

render(<App />);
```

- [ ] **Step 3: Build and test**

Run: `cd /Users/fango/coding/fango/fango-cli && pnpm build`
Expected: builds without errors, `dist/cli.js` is created.

Run: `node dist/cli.js`
Expected: the full card renders in terminal with header, experience, projects, and interactive links. Arrow keys navigate. `q` exits.

- [ ] **Step 4: Also test with dev mode**

Run: `cd /Users/fango/coding/fango/fango-cli && pnpm dev`
Expected: same output as above, using tsx for direct execution.

- [ ] **Step 5: Commit**

```bash
git add source/app.tsx source/cli.tsx
git commit -m "feat: wire up App and CLI entry point — card is fully functional"
```

---

## Task 8: Manual QA & Polish

No new files. This task validates the acceptance criteria from the spec.

- [ ] **Step 1: Test card rendering**

Run: `cd /Users/fango/coding/fango/fango-cli && node dist/cli.js`

Verify:
- Header shows name (bold white), title (cyan), tagline (dim)
- Experience section has round border with red title
- Projects section has round border with red title
- Links section shows with arrow indicator
- Card width is 54 characters
- Resize terminal to exactly 54 columns wide and confirm no visual breakage or broken borders

- [ ] **Step 2: Test interaction**

While the card is running:
- Press ↑/↓ — verify selected link changes with cyan highlight
- Press Enter — verify browser opens the selected URL
- Press Enter quickly twice — verify only one browser tab opens (debounce)
- Press `q` — verify clean exit
- Press `Ctrl+C` — verify clean exit (relaunch card first)

- [ ] **Step 3: Test edge case — open failure**

Temporarily modify a link's href to an invalid value like `not-a-url`, rebuild, run, select it, press Enter. Verify the raw href is printed as feedback instead of "Opened!". Revert the change after testing.

- [ ] **Step 4: Fix any visual issues**

If spacing, alignment, or colors look off, adjust the components and rebuild. Common things to tweak:
- `paddingX`, `paddingY`, `marginBottom` values in components
- `gap` spacing between elements
- `width` on the outer box

- [ ] **Step 5: Commit any fixes**

```bash
git add -A
git commit -m "fix: polish card layout and spacing"
```

(Skip this commit if no changes were needed.)

---

## Task 9: README & Publish Prep

**Files:**
- Create: `README.md`

- [ ] **Step 1: Create README.md**

```markdown
# fango

My terminal business card.

## Usage

```
npx fango
```

## Development

```bash
pnpm install
pnpm dev
```

## Build

```bash
pnpm build
node dist/cli.js
```
```

- [ ] **Step 2: Verify prepublishOnly works**

Run: `cd /Users/fango/coding/fango/fango-cli && rm -rf dist && pnpm publish --dry-run`
Expected: `prepublishOnly` triggers `pnpm build`, then the dry-run succeeds showing the package contents include `dist/cli.js`.

- [ ] **Step 3: Check npm name availability**

Run: `npm view fango`
If the name is taken, the user needs to choose an alternative (e.g., `@0xfango/card`, `fango-card`). Flag this to the user before publishing.

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add README"
```

- [ ] **Step 5: Publish (requires user action)**

The user needs to run:
```bash
cd /Users/fango/coding/fango/fango-cli
npm login   # if not already logged in
pnpm publish
```

Then verify: `npx fango` works from any directory.

**Important:** This step requires the user's npm credentials. Do not attempt to publish automatically.
