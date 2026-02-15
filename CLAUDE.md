# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**Note**: This project uses [AGENTS.md](AGENTS.md) files for detailed guidance.

## Package Manager

This project uses **Bun v1.3.3+** as the package manager. Always use `bun` or `bunx` instead of `npm`/`npx`/`pnpm`/`pnpx`.

## Common Commands

```bash
# Install dependencies
bun install

# Build all packages
bun run build

# Run tests and linting
bun run test
bun run stylecheck

# Watch mode for development
bun run watch

# Clean build artifacts (if build fails)
bun run clean
```

### Package-Specific Commands

```bash
# Build specific package
bunx turbo run make --filter='<package-name>'

# Watch specific package
bunx turbo watch make --filter='<package-name>'

# Run tests in specific package
cd packages/<package-name>
bun test
```

## Repository Architecture

This is a **monorepo** with 100+ packages managed by Turbo. Key architectural concepts:

### Core Packages
- `packages/core` - Main `remotion` package with React components, hooks, and video config
- `packages/renderer` - Video rendering orchestration (Puppeteer, FFmpeg)
- `packages/cli` - Command-line interface
- `packages/player` - Video player component
- `packages/studio` - Visual editor

### Supporting Systems
- `packages/bundler` - Vite-based bundling for Remotion projects
- `packages/compositor` - Rust-based video compositing (FFmpeg wrapper)
- `packages/media-parser` - Media parsing (WebCodecs, MP3, etc.)
- `packages/lambda` - AWS Lambda rendering integration
- `packages/webcodecs` - Browser-based video encoding

### Package Dependencies
- The `make` task has a `dependsOn: ["^make"]` dependency graph
- When building a package, all upstream dependencies build first
- Check `turbo.json` for task dependency relationships

### Testing
- `bun test` in package directories runs tests using Bun's test runner
- `packages/it-tests` - Integration tests
- `packages/example` - Main testbed for manual testing (`bun run dev`)
- `packages/player-example` - Player testbed

## Versioning

The current Remotion version is in `packages/core/src/version.ts`.

When bumping versions, increment the patch version by 1 (e.g., `4.0.422` → `4.0.423`).

## Commit and PR Conventions

Pull request titles should follow the format:
```
[package-name]: [commit-message]
```

Example: `@remotion/player: Add new feature`

## Before Committing

1. Run `bun run build` to verify all packages build
2. Run `bun run stylecheck` to ensure CI passes
3. Include `bun.lock` when dependencies change

## TypeScript Configuration

- Uses project references (see `tsconfig.json`)
- Each package has its own `tsconfig.json`
- Build command: `tsc -d` (declaration generation enabled)

## Linting and Formatting

- Prettier: Auto-formats on save in VS Code
- ESLint: `@remotion/eslint-config-internal` for internal rules
- Run `bun run stylecheck` to verify before committing

## Documentation

Documentation is in `packages/docs` using Docusaurus. To run:
```bash
cd packages/docs
bun run start
```

When adding new docs pages, run `bun render-cards.ts` to generate social media preview cards.

## License Note

Remotion has a commercial license - see `LICENSE.md`. By contributing, you agree that changes can be used in a commercial context.
