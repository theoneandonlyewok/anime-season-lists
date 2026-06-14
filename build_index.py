#!/usr/bin/env python3

import argparse
import html
import json
import os
import re

SEASON_ORDER = {"winter": 0, "spring": 1, "summer": 2, "fall": 3}
FILE_RE = re.compile(r"^(winter|spring|summer|fall)-(\d{4})\.json$", re.IGNORECASE)


def discover(directory):
    """Find season list files and read their series counts."""
    seasons = []
    for name in sorted(os.listdir(directory)):
        match = FILE_RE.match(name)
        if not match:
            continue  # skips manifest.json, *.unmatched.json, index.html, etc.
        season = match.group(1).lower()
        year = int(match.group(2))
        try:
            with open(os.path.join(directory, name), encoding="utf-8") as f:
                count = len(json.load(f))
        except Exception:
            count = None
        seasons.append(
            {"season": season, "year": year, "file": name, "count": count}
        )
    seasons.sort(key=lambda s: (-s["year"], SEASON_ORDER.get(s["season"], 9)))
    return seasons


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Seasonal Anime Lists for Sonarr</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font-family: system-ui, sans-serif; max-width: 820px; margin: 2rem auto;
         padding: 0 1rem; line-height: 1.5; }}
  h1 {{ margin-bottom: .25rem; }}
  p.sub {{ color: #888; margin-top: 0; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 1.5rem; }}
  th, td {{ text-align: left; padding: .55rem .5rem; border-bottom: 1px solid #8884; }}
  code {{ background: #8881; padding: .15rem .4rem; border-radius: 4px;
          font-size: .85em; word-break: break-all; }}
  button {{ cursor: pointer; border: 1px solid #8886; background: transparent;
            border-radius: 5px; padding: .2rem .55rem; font-size: .8em; }}
  button:hover {{ background: #8882; }}
  .how {{ background: #8881; border-radius: 8px; padding: .75rem 1rem; margin-top: 2rem;
          font-size: .92em; }}
  .how ol {{ margin: .4rem 0 0 1.1rem; padding: 0; }}
</style>
</head>
<body>
<h1>Seasonal Anime Lists for Sonarr</h1>
<p class="sub">Custom Import Lists, generated from AniList and mapped to TVDB. Updated weekly.</p>

<table>
<thead><tr><th>Season</th><th>Series</th><th>Import URL</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>

<div class="how">
<strong>How to use in Sonarr</strong>
<ol>
  <li>Settings &rarr; Import Lists &rarr; + &rarr; Custom List</li>
  <li>Paste a URL above into <em>List URL</em></li>
  <li>Set <em>Series Type</em> to <strong>Anime</strong>, pick a quality profile and root folder</li>
  <li>Test, Save, then run the Import List Sync task</li>
</ol>
</div>

<script>
function copy(id) {{
  const el = document.getElementById(id);
  navigator.clipboard.writeText(el.textContent).then(() => {{
    const btn = el.nextElementSibling;
    const old = btn.textContent; btn.textContent = "copied";
    setTimeout(() => btn.textContent = old, 1200);
  }});
}}
</script>
</body>
</html>
"""


def build(lists_dir, out_dir, base_url):
    seasons = discover(lists_dir)
    base = (base_url.rstrip("/") + "/") if base_url else ""
    # Path from the site root (out_dir) down to the list files, e.g. "lists/".
    rel = os.path.relpath(lists_dir, out_dir)
    subpath = "" if rel in (".", "") else rel.replace(os.sep, "/").strip("/") + "/"
    for s in seasons:
        s["path"] = subpath + s["file"]              # relative to the site root
        s["url"] = (base + s["path"]) if base else s["path"]

    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(seasons, f, indent=2)

    rows = []
    for i, s in enumerate(seasons):
        label = f"{s['season'].capitalize()} {s['year']}"
        count = f"{s['count']}" if s["count"] is not None else "?"
        cid = f"u{i}"
        url = html.escape(s["url"])
        rows.append(
            f'<tr><td>{html.escape(label)}</td><td>{count}</td>'
            f'<td><code id="{cid}">{url}</code> '
            f'<button onclick="copy(\'{cid}\')">copy</button></td></tr>'
        )
    if not rows:
        rows.append('<tr><td colspan="3">No season lists found yet.</td></tr>')

    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(PAGE.format(rows="\n".join(rows)))

    print(f"Indexed {len(seasons)} season(s) from {lists_dir}/ -> {out_dir}/")
    return seasons


def main():
    parser = argparse.ArgumentParser(
        description="Build index.html + manifest.json for a folder of season lists."
    )
    parser.add_argument(
        "lists_dir", help="folder containing the <season>-<year>.json files"
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="where to write index.html + manifest.json "
        "(default: same as lists_dir)",
    )
    parser.add_argument(
        "--base-url",
        default="",
        help="public base URL of the site root "
        "(e.g. https://you.github.io/anime-lists/)",
    )
    args = parser.parse_args()
    build(args.lists_dir, args.out_dir or args.lists_dir, args.base_url)


if __name__ == "__main__":
    main()
