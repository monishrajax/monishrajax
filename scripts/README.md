# scripts

Everything that draws the farm. Pure Python 3 standard library, no installs needed.

| File | What it does |
|:--|:--|
| `build_assets.py` | Builds the **static** SVGs in `../assets` (hero, section banners, tags, project cards, tech carousel, footer, contact badges). Edit the `CONFIG` block at the top (handle, tagline, projects, tech lists), then run `python3 scripts/build_assets.py` and commit the result. |
| `update_yield.py` | Builds the **live** `assets/yield.svg` (stat plates + a grass-in-boxes contribution graph) from your GitHub contribution calendar and refreshes the repo table in `README.md` (between the `REPOS:START/END` markers). Run by `.github/workflows/farm-yield.yml` every 6 hours; you can also run it by hand: `python3 scripts/update_yield.py`. |
| `farmlib.py` | Shared drawing helpers: palette, text-to-path, wheat, grass, tractor, barn and other icons. |
| `farm_glyphs.json` | Vector outlines of the two fonts below, so text renders identically everywhere (GitHub loads SVGs through `<img>`, which cannot use web fonts). |
| `farm_icons.json` | Tech logo outlines from Simple Icons. |

## Notes

- Stats: *Contributions* = last 12 months; *Longest streak* = best run across your whole account history; *Public repos* = repos you own.
- Cell intensity is relative to your own active days (quartiles), so one huge day cannot flatten the whole graph.
- Animations use CSS and pause automatically for visitors who prefer reduced motion.
- Private contributions (optional): turn on **Include private contributions on my profile** in your GitHub profile settings, then add a repository secret named `PROFILE_TOKEN` holding a classic personal access token with the `read:user` scope. Without it the graph shows public activity only.

## Credits

- Type: **Alfa Slab One** (c) 2016 The Alfa Slab One Project Authors and **Space Mono** (c) 2016 The Space Mono Project Authors, both under the [SIL Open Font License 1.1](https://openfontlicense.org).
- Logos: [Simple Icons](https://simpleicons.org), CC0 1.0. Trademarks belong to their owners.
