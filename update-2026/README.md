# 2026 update: four Japanese pitchers' arsenals, season by season

`build.py` fetches regular-season Statcast pitches from Baseball Savant (2019-2026) for Yusei Kikuchi, Yu Darvish, Kodai Senga and Shota Imanaga, and draws one GIF per pitcher. Each dot is a pitch type at its average movement for the season, and its area is that type's share of the pitches. The dots slide from one season to the next.

```bash
pip install pandas requests matplotlib pillow savant-extras
python build.py   # fetch into raw/ (not committed), check, draw
```

## Before drawing, the numbers are checked against Savant

Every (season, pitch type) that is drawn is compared with Savant's own pitch-movement leaderboard (`savant_extras.pitch_movement`). If anything disagrees, nothing is drawn.

| Check | Allowed | Measured 2026-10-08 |
|---|---|---|
| Pitch count | exact | 102 of 102 rows equal |
| Share of pitches | < 0.002 | max 0.00017 (after folding KC into CU) |
| Movement (in) | < 0.15 | vertical max 0.08, horizontal max 0.13 |

Of the 111 drawn rows, 9 are absent from Savant's leaderboard because it has a minimum pitch count. They are not checked.

## Conventions

- Pickoff throws (`PO`) are not pitches. Knuckle curves and slow curves are counted as `CU`, the same way Savant's arsenal tables count them.
- Seasons with fewer than 300 pitches are named on the frame but not drawn: Senga 2024 has 73 pitches, and Darvish 2026 has none. Pitch types under 3% of a season are not drawn.
- Horizontal break is shown with the arm side positive, so left- and right-handers read the same way.
- The headlines are built from `season_mix.csv`, and the script asserts the direction each one claims, so no number in a title is typed by hand.
- The script also checks that each title fits inside the frame.

Data: [Baseball Savant](https://baseballsavant.mlb.com/) (Statcast).
