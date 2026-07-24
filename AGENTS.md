# Repository Guidelines

## Project Structure & Module Organization

This repository powers the GitHub profile for `bgreenwell`; `README.md` is the primary deliverable.

- `README.md`: profile copy, book showcase, project grid, and external links.
- `profile/projects.json`: source data for featured project cards.
- `profile/cards/`: generated light- and dark-theme SVG cards. Do not edit these files by hand.
- `profile/books/`: locally stored book-cover images used by the README.
- `scripts/render_project_cards.py`: dependency-free Python card generator and verifier.
- `.github/workflows/verify-project-cards.yml`: pull-request check for generated-card drift.

There is no application runtime or conventional test directory.

## Build, Test, and Development Commands

Run commands from the repository root:

```bash
python3 scripts/render_project_cards.py
```

Regenerates every SVG after changing `profile/projects.json` or the renderer.

```bash
python3 scripts/render_project_cards.py --check
git diff --check
```

The first command verifies committed cards without modifying them; the second detects whitespace errors. Both should pass before committing.

## Coding Style & Naming Conventions

Use four-space indentation in Python and two-space indentation in JSON. Keep the renderer compatible with the Python standard library; avoid adding dependencies for simple generation tasks. Use lowercase kebab-case asset names, with theme suffixes such as `doxx-light.svg` and `doxx-dark.svg`.

Keep README HTML accessible: provide meaningful image `alt` text, preserve paired light/dark `<picture>` sources, and use relative paths for repository assets. Keep prose concise and avoid duplicating projects across sections.

## Testing Guidelines

There is no unit-test framework or coverage target. Treat deterministic generation as the test contract. After changing project metadata, regenerate cards and run `--check`. Visually inspect affected SVGs in both themes and verify new external links resolve.

## Commit & Pull Request Guidelines

Recent commits use concise Conventional Commit-style prefixes: `feat:`, `docs:`, and `style:`. Write imperative, focused subjects, for example `docs: update teaching focus`.

Pull requests should explain the visible profile change, list validation commands run, and include a rendered screenshot for layout or asset changes. Keep generated SVGs in the same commit as their manifest or renderer changes. Do not reintroduce scheduled workflows that commit volatile statistics to the repository.
