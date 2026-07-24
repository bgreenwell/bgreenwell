#!/usr/bin/env python3
"""Render deterministic light and dark SVG cards for the profile README."""

from __future__ import annotations

import argparse
import html
import json
import sys
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "profile" / "projects.json"
OUTPUT_DIR = ROOT / "profile" / "cards"

THEMES = {
    "light": {
        "background": "#FFFFFF",
        "border": "#D0D7DE",
        "title": "#1F2328",
        "body": "#59636E",
        "muted": "#59636E",
        "pill": "#F6F8FA",
    },
    "dark": {
        "background": "#0D1117",
        "border": "#30363D",
        "title": "#F0F6FC",
        "body": "#9198A1",
        "muted": "#9198A1",
        "pill": "#161B22",
    },
}


def render_card(project: dict[str, str], theme_name: str) -> str:
    theme = THEMES[theme_name]
    name = html.escape(project["name"])
    description = html.escape(project["description"])
    language = html.escape(project["language"])
    accent = html.escape(project["accent"])
    lines = textwrap.wrap(project["description"], width=48) or [""]
    description_tspans = "".join(
        f'<tspan x="28" dy="{0 if index == 0 else 20}">{html.escape(line)}</tspan>'
        for index, line in enumerate(lines)
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="140" viewBox="0 0 400 140" role="img" aria-labelledby="title desc">
  <title id="title">{name}</title>
  <desc id="desc">{description}</desc>
  <rect x="0.5" y="0.5" width="399" height="139" rx="10" fill="{theme['background']}" stroke="{theme['border']}"/>
  <rect x="0" y="0" width="5" height="140" rx="2.5" fill="{accent}"/>
  <text x="28" y="39" fill="{theme['title']}" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="21" font-weight="650">{name}</text>
  <text x="28" y="66" fill="{theme['body']}" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="14">{description_tspans}</text>
  <g transform="translate(28 108)">
    <rect width="{max(66, len(language) * 9 + 34)}" height="24" rx="12" fill="{theme['pill']}"/>
    <circle cx="13" cy="12" r="4" fill="{accent}"/>
    <text x="24" y="16" fill="{theme['muted']}" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="12" font-weight="600">{language}</text>
  </g>
  <text x="372" y="126" text-anchor="end" fill="{theme['muted']}" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="13">View project →</text>
</svg>
"""


def expected_outputs() -> dict[Path, str]:
    projects = json.loads(MANIFEST.read_text(encoding="utf-8"))
    outputs: dict[Path, str] = {}
    for project in projects:
        for theme_name in THEMES:
            path = OUTPUT_DIR / f"{project['slug']}-{theme_name}.svg"
            outputs[path] = render_card(project, theme_name)
    return outputs


def check_outputs(outputs: dict[Path, str]) -> int:
    stale = [
        path.relative_to(ROOT)
        for path, expected in outputs.items()
        if not path.exists() or path.read_text(encoding="utf-8") != expected
    ]
    if stale:
        print("Project cards are missing or stale:", file=sys.stderr)
        for path in stale:
            print(f"  {path}", file=sys.stderr)
        print("Run: python3 scripts/render_project_cards.py", file=sys.stderr)
        return 1
    print(f"Verified {len(outputs)} generated project cards.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify generated cards without writing files",
    )
    args = parser.parse_args()
    outputs = expected_outputs()
    if args.check:
        return check_outputs(outputs)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")
    print(f"Rendered {len(outputs)} project cards in {OUTPUT_DIR.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
