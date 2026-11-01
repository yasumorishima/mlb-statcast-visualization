# CLAUDE.md — mlb-statcast-visualization

Statcast visualisation notebooks (pybaseball + DuckDB + matplotlib) on Japanese MLB players, a 2026 arsenal-GIF update, and older analyses merged in from a now-archived repo. **Dormant**: no work is scheduled.

## Session protocol (cloud)
1. Read this file first. There is nothing scheduled: act only on what the owner asks in this session.
2. Before ending, add a dated line to "Progress log" (and update "Next tasks" if anything changed), then open a PR to `main` from the session branch and merge it yourself; report the merged commit.
3. No `gh` CLI in cloud (use the GitHub MCP tools); `workflow_dispatch` returns 403 from cloud.
4. Reply to the owner in Japanese (です/ます). Do not claim anything you did not run in this session; say where each number was measured.

## Progress log
- 2026-02: root notebooks (Ohtani spray chart / heat map, Darvish, Imanaga, Senga, Kikuchi) with `.py` copies; Zenn articles linked in README.
- 2026-10-08: the old `mlb-data-analysis` repo merged with its history into `analyses-2022-2024/` (PR #3, merge `94191cc`; that repo is archived and points here); root `LICENSE` MIT; Zenn/Colab links fixed. `update-2026/` added (PR #4, `b97b366`): per-season arsenal GIFs for four pitchers, checked against Savant's pitch-movement leaderboard before drawing (102/102 pitch counts equal, movement within 0.13 in, measured 2026-10-08).
- 2026-11-01: this file written for cloud. Nothing run. The six Zenn links in README answered HTTP 200 (checked from the owner's PC).

## What this is
- Root: `*_20xx_20xx.ipynb` + same-name `.py` (Colab; `!pip` lines commented out in the `.py`).
- `analyses-2022-2024/`: 2022–2024 notebooks, with DuckDB versions in `notebooks/sql/`.
- `update-2026/build.py`: fetches regular-season pitches from Baseball Savant into `update-2026/raw/` (git-ignored), checks them against `savant_extras.pitch_movement`, writes `season_mix.csv` and four GIFs. It refuses to draw (`sys.exit`) if any check fails; headline numbers come from `season_mix.csv` with asserted directions.

## Non-negotiable discipline
1. Filter to regular season (`game_type == "R"`) in every analysis (README rule).
2. Keep a `.py` copy next to every `.ipynb` (`analyses-2022-2024/Makefile` has the nbconvert recipe).
3. The owner's profile README counts this repo's `.ipynb` files recursively (excluding `sql/`, currently 11) automatically; adding or removing notebooks changes that number.
4. Do not re-add the notebook/image of the pitcher removed on 2026-02-26 (`5d04c12`, likeness rights) or anything depending on a personal Google Drive.
5. In `update-2026/`, never type a number into a title by hand and never relax a check to make the script draw.

## Next tasks
None scheduled; only act when the owner asks. Candidates noticed on 2026-11-01:
- The repository description still says "3 methods ... sportypy", but the sportypy notebook was removed (`1b3610f`, `bd832be`).
- `KIKUCHI_ANALYSIS_NOTES.md` is an old work note ("next step: run in Colab, then write the article"); the article is published.
- README dataset titles say 2015-2025 / 2020-2025 / 2024-2025; whether the Kaggle datasets were since extended to 2026 is not checked here (Kaggle returns 200 for any path, so a status code proves nothing).
- No CI workflow (only GitHub's dependency graph).

## How to run (cloud, not yet tried there)
```bash
cd update-2026 && pip install pandas requests matplotlib pillow savant-extras && python build.py
pip install pybaseball duckdb seaborn && python kikuchi_2019_2025.py   # any root .py
```
Needs `baseballsavant.mlb.com` (pybaseball and `build.py`). Do not commit `update-2026/raw/`.

## Credits (keep in README)
Baseball Savant (Statcast, MLB Advanced Media); pybaseball. Code MIT (`LICENSE`, `analyses-2022-2024/LICENSE`).
