"""2026 update: how four Japanese pitchers' arsenals moved, season by season.

One GIF per pitcher. Each dot is a pitch type at its average movement for the
season (arm-side break vs induced vertical break, inches); its area is the
share of pitches. Dots slide from season to season.

Data: Baseball Savant Statcast search (regular season), fetched with
fetch() below. Before drawing, every (season, pitch type) shown is checked
against Savant's own pitch-movement leaderboard (savant-extras); if the counts,
shares or movement disagree, nothing is drawn.

Run:  python build.py            (fetch if needed, check, draw)
"""
import io
import pathlib
import sys
import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / "raw"  # not committed (re-fetchable)
FIRST, LAST = 2019, 2026
MIN_SEASON_PITCHES = 300  # seasons with fewer pitches are named, not drawn
MIN_SHARE = 0.03  # pitch types below 3% of a season are not drawn
# Savant's arsenal tables fold knuckle curves and slow curves into CU.
FOLD = {"KC": "CU", "CS": "CU"}
NOT_A_PITCH = {"PO"}  # pickoff throws

PITCHERS = {
    "kikuchi": dict(id=579328, name="Yusei Kikuchi", hand="L"),
    "darvish": dict(id=506433, name="Yu Darvish", hand="R"),
    "senga": dict(id=673540, name="Kodai Senga", hand="R"),
    "imanaga": dict(id=684007, name="Shota Imanaga", hand="L"),
}
NAMES = {"FF": "Four-seam", "SI": "Sinker", "FC": "Cutter", "SL": "Slider",
         "ST": "Sweeper", "CU": "Curve", "CH": "Changeup", "FS": "Splitter",
         "FO": "Forkball", "SV": "Slurve", "EP": "Eephus"}
COLORS = {"FF": "#d1495b", "SI": "#edae49", "FC": "#8d6a9f", "SL": "#00798c",
          "ST": "#30638e", "CU": "#3a7d44", "CH": "#e07a5f", "FS": "#6c757d",
          "FO": "#6c757d", "SV": "#5e548e", "EP": "#999999"}

URL = ("https://baseballsavant.mlb.com/statcast_search/csv?all=true&type=details"
       "&player_type=pitcher&pitchers_lookup%5B%5D={pid}&hfGT=R%7C&hfSea={y}%7C"
       "&game_date_gt={y}-03-01&game_date_lt={y}-11-30")


def fetch():
    RAW.mkdir(exist_ok=True)
    for key, p in PITCHERS.items():
        for y in range(FIRST, LAST + 1):
            f = RAW / f"{key}_{y}.csv"
            if f.exists():
                continue
            r = requests.get(URL.format(pid=p["id"], y=y), timeout=120)
            r.raise_for_status()
            f.write_text(r.text, encoding="utf-8")
            time.sleep(2)


def season_table():
    rows = []
    for key, p in PITCHERS.items():
        for y in range(FIRST, LAST + 1):
            text = (RAW / f"{key}_{y}.csv").read_text(encoding="utf-8")
            d = pd.read_csv(io.StringIO(text)) if text.strip() else pd.DataFrame()
            if d.empty:
                rows.append(dict(key=key, year=y, pt=None, n=0, season_n=0))
                continue
            assert set(d.pitcher.unique()) == {p["id"]}, (key, y)
            assert set(d.game_type.unique()) == {"R"}, (key, y)
            assert (d.game_year == y).all(), (key, y)
            # The arm-side sign below depends on this; Savant's leaderboard only gives |break|.
            assert set(d.p_throws.unique()) == {p["hand"]}, (key, y)
            d = d[d.pitch_type.notna() & ~d.pitch_type.isin(NOT_A_PITCH)].copy()
            d["pt"] = d.pitch_type.replace(FOLD)
            sign = 1.0 if p["hand"] == "L" else -1.0  # arm side positive
            g = d.groupby("pt").agg(n=("pt", "size"), ivb=("pfx_z", "mean"), hb=("pfx_x", "mean"))
            for pt, r in g.iterrows():
                rows.append(dict(key=key, year=y, pt=pt, n=int(r.n), season_n=len(d),
                                 share=r.n / len(d), ivb=12 * r.ivb, hb_raw=12 * r.hb,
                                 arm=sign * 12 * r.hb))
    t = pd.DataFrame(rows)
    ff = t[(t.pt == "FF") & (t.n > 0)]
    assert (ff.arm > 0).all(), "four-seamers must run to the arm side; the sign is wrong"
    return t


# Rows the headlines are built from: each must be confirmed by Savant.
HEADLINE_ROWS = [("kikuchi", 2025, "CH"), ("kikuchi", 2026, "FS"),
                 ("darvish", 2019, "SL"), ("darvish", 2025, "SL"), ("darvish", 2019, "SI"), ("darvish", 2025, "SI"),
                 ("senga", 2025, "FF"), ("senga", 2026, "FF"), ("senga", 2025, "FC"), ("senga", 2026, "FC"),
                 ("imanaga", 2024, "FF"), ("imanaga", 2025, "FF"), ("imanaga", 2026, "FF")]


def check_against_savant(t):
    """Every drawn (season, type) must match Savant's pitch-movement leaderboard."""
    from savant_extras import pitch_movement

    drawn = t[(t.season_n >= MIN_SEASON_PITCHES) & (t.share >= MIN_SHARE)]
    bad, checked, lb_cache, seen, absent = [], 0, {}, set(), []
    gap = dict(count=0, share=0.0, ivb=0.0, hb=0.0)
    for (y, pt), grp in drawn.groupby(["year", "pt"]):
        if (y, pt) not in lb_cache:
            lb_cache[(y, pt)] = pitch_movement(int(y), pt)
            time.sleep(1)
        lb = lb_cache[(y, pt)]
        for _, r in grp.iterrows():
            m = lb[lb.pitcher_id == PITCHERS[r.key]["id"]]
            if m.empty:
                absent.append((r.key, int(y), pt, round(r.share, 3)))  # below Savant's minimum
                continue
            m = m.iloc[0]
            checked += 1
            seen.add((r.key, int(y), pt))
            gap['count'] = max(gap['count'], abs(int(m.pitches_thrown) - r.n))
            gap['share'] = max(gap['share'], abs(m.pitch_per - r.share))
            gap['ivb'] = max(gap['ivb'], abs(m.pitcher_break_z_induced - r.ivb))
            gap['hb'] = max(gap['hb'], abs(abs(m.pitcher_break_x) - abs(r.hb_raw)))
            # Counts must agree exactly. Movement: measured max gap 0.13 in over all 102 rows
            # (2026-10-08; Savant averages a slightly different set), so allow 0.15 in.
            ok = (int(m.pitches_thrown) == r.n
                  and abs(m.pitch_per - r.share) < 0.002
                  and abs(m.pitcher_break_z_induced - r.ivb) < 0.15
                  and abs(abs(m.pitcher_break_x) - abs(r.hb_raw)) < 0.15)
            if not ok:
                bad.append((r.key, y, pt, r.n, m.pitches_thrown, round(r.share, 4), m.pitch_per,
                            round(r.ivb, 2), m.pitcher_break_z_induced, round(r.hb_raw, 2), m.pitcher_break_x))
    print(f"checked against Savant: {checked} of {len(drawn)} drawn (season, type) rows; "
          f"max gaps count {gap['count']}, share {gap['share']:.5f}, ivb {gap['ivb']:.3f}, hb {gap['hb']:.3f}")
    if bad:
        for b in bad:
            print("MISMATCH", b)
        sys.exit("refusing to draw: numbers disagree with Savant")
    for a in absent:
        print("not on Savant's leaderboard (not checked):", a)
    missing = [h for h in HEADLINE_ROWS if h not in seen]
    if missing:
        sys.exit(f"refusing to draw: headline rows not confirmed by Savant: {missing}")
    for key in PITCHERS:
        n_drawn = int((drawn.key == key).sum())
        n_seen = sum(1 for s in seen if s[0] == key)
        if n_seen < 0.8 * n_drawn:
            sys.exit(f"refusing to draw: only {n_seen}/{n_drawn} of {key}'s rows could be checked")


def share(t, key, y, pt):
    r = t[(t.key == key) & (t.year == y) & (t.pt == pt)]
    return float(r.share.iloc[0]) if len(r) else 0.0


def pct(x):
    return f"{100 * x:.0f}%"


def titles(t):
    """Headline per pitcher, built from the table (no hand-typed numbers)."""
    s = lambda k, y, p: share(t, k, y, p)
    out = {}
    assert s("kikuchi", 2026, "CH") == 0 and s("kikuchi", 2025, "FS") == 0
    # Same speed and spin as the old changeup, less arm-side run: the data cannot tell a new
    # pitch from a relabelled one, so the title only says what the labels did.
    out["kikuchi"] = (f"2026: no changeup (was {pct(s('kikuchi', 2025, 'CH'))}), "
                      f"a “splitter” at {pct(s('kikuchi', 2026, 'FS'))}")
    assert s("darvish", 2025, "SL") < s("darvish", 2019, "SL") and s("darvish", 2025, "SI") > s("darvish", 2019, "SI")
    out["darvish"] = (f"Fewer sliders ({pct(s('darvish', 2019, 'SL'))} → {pct(s('darvish', 2025, 'SL'))}), "
                      f"more sinkers ({pct(s('darvish', 2019, 'SI'))} → {pct(s('darvish', 2025, 'SI'))})")
    assert s("senga", 2026, "FF") > s("senga", 2025, "FF") and s("senga", 2026, "FC") < s("senga", 2025, "FC")
    out["senga"] = (f"2026: four-seamers {pct(s('senga', 2025, 'FF'))} → {pct(s('senga', 2026, 'FF'))}, "
                    f"cutters {pct(s('senga', 2025, 'FC'))} → {pct(s('senga', 2026, 'FC'))}")
    ff = [s("imanaga", y, "FF") for y in (2024, 2025, 2026)]
    assert ff[0] > ff[1] > ff[2]
    out["imanaga"] = "Fewer four-seamers every year: " + " → ".join(pct(x) for x in ff)
    return out


def ease(u):
    return u * u * (3 - 2 * u)


def draw(t, key, title, out_path):
    p = PITCHERS[key]
    sub = t[t.key == key]
    seasons = sorted(sub.year.unique())
    shown = [y for y in seasons if sub[sub.year == y].season_n.max() >= MIN_SEASON_PITCHES]
    skipped = {y: int(sub[sub.year == y].season_n.max()) for y in seasons if y not in shown and y >= shown[0]}
    vis = sub[sub.year.isin(shown) & (sub.share >= MIN_SHARE)]
    types = sorted(vis.pt.unique(), key=lambda x: -vis[vis.pt == x].share.max())

    def state(y):
        st = {}
        for pt in types:
            r = vis[(vis.year == y) & (vis.pt == pt)]
            st[pt] = (float(r.arm.iloc[0]), float(r.ivb.iloc[0]), float(r.share.iloc[0])) if len(r) else None
        return st

    # Fixed axes for the whole GIF (computed from every drawn season).
    xlo, xhi = vis.arm.min() - 5, vis.arm.max() + 5
    ylo, yhi = vis.ivb.min() - 5, vis.ivb.max() + 5

    fig = plt.figure(figsize=(8, 8), dpi=90)
    fig.subplots_adjust(left=0.12, right=0.96, top=0.71, bottom=0.10)
    ax = fig.add_subplot(111)
    # Fixed text is drawn once (ax.clear() does not remove figure-level text).
    fig.text(0.03, 0.965, p["name"], fontsize=13, color="#555555", ha="left", va="top")
    head = fig.text(0.03, 0.925, title, fontsize=16, color="#111111", ha="left", va="top", fontweight="bold")
    fig.canvas.draw()
    box = head.get_window_extent()
    assert box.x1 <= fig.bbox.width - 8, f"title does not fit: {title!r} ends at {box.x1:.0f}px of {fig.bbox.width:.0f}" 
    fig.text(0.03, 0.865, "Average movement of each pitch type; dot area = share of pitches. Regular season.",
             fontsize=11, color="#555555", ha="left", va="top")
    # The season sits between the header and the plot, so a dot can never cover it.
    year_text = fig.text(0.03, 0.73, "", fontsize=34, color="#222222", ha="left", va="bottom", fontweight="bold")
    note_text = fig.text(0.96, 0.735, "", fontsize=12, color="#666666", ha="right", va="bottom")
    fig.text(0.03, 0.02, "Data: Baseball Savant (Statcast). Types under 3% not shown.",
             fontsize=10, color="#777777", ha="left")
    frames, durations = [], []

    def render(st_a, st_b, u, year_label, note):
        ax.clear()
        ax.set_xlim(xlo, xhi)
        ax.set_ylim(ylo, yhi)
        ax.axhline(0, color="#bbbbbb", lw=1, zorder=0)
        ax.axvline(0, color="#bbbbbb", lw=1, zorder=0)
        ax.set_xlabel("← glove side     break (in)     arm side →", fontsize=14)
        ax.set_ylabel("Induced vertical break (in)", fontsize=14)
        ax.tick_params(labelsize=12)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        e = ease(u)
        for pt in types:
            a, b = st_a.get(pt), st_b.get(pt)
            if a is None and b is None:
                continue
            # `label` is a real season share; only the dot size is interpolated while fading.
            if a is None:
                x, y, sh, alpha, label = b[0], b[1], b[2] * e, e, b[2]
            elif b is None:
                x, y, sh, alpha, label = a[0], a[1], a[2] * (1 - e), 1 - e, a[2]
            else:
                x = a[0] + (b[0] - a[0]) * e
                y = a[1] + (b[1] - a[1]) * e
                sh, alpha = a[2] + (b[2] - a[2]) * e, 1.0
                label = sh
            ax.scatter([x], [y], s=4000 * sh, color=COLORS.get(pt, "#777777"), alpha=0.85 * alpha,
                       edgecolor="white", linewidth=1.5, zorder=3)
            if alpha > 0.5:
                ax.annotate(f"{NAMES.get(pt, pt)} {100 * label:.0f}%", (x, y), xytext=(0, -np.sqrt(4000 * sh) / 2 - 12),
                            textcoords="offset points", ha="center", fontsize=12, color="#333333")
        year_text.set_text(year_label)
        note_text.set_text(note)
        fig.canvas.draw()
        frames.append(Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[..., :3]))

    for i, y in enumerate(shown):
        st = state(y)
        gap = [g for g in skipped if (i > 0 and shown[i - 1] < g < y)]
        notes = [f"{g}: {skipped[g]} pitches, not shown" for g in gap]
        if i == len(shown) - 1:  # seasons after the last drawn one go on the final frame
            notes += [f"{g}: {'no' if skipped[g] == 0 else skipped[g]} MLB pitches"
                      for g in skipped if g > y]
        render(st, st, 0.0, str(y), "; ".join(notes))
        durations.append(1400 if i < len(shown) - 1 else 3500)
        if i + 1 < len(shown):
            nxt = state(shown[i + 1])
            for k in range(1, 9):
                render(st, nxt, k / 9, f"{y}→{shown[i + 1]}", "")
                durations.append(70)
    plt.close(fig)
    pal = [f.quantize(colors=128, method=Image.Quantize.MEDIANCUT) for f in frames]
    assert len(durations) == len(frames)
    pal[0].save(out_path, save_all=True, append_images=pal[1:], duration=durations, loop=0, optimize=True)
    return len(frames), sum(durations) / 1000, out_path.stat().st_size


def main():
    fetch()
    t = season_table()
    t.drop(columns=["hb_raw"]).to_csv(HERE / "season_mix.csv", index=False, float_format="%.4f")
    check_against_savant(t)
    heads = titles(t)
    for key in PITCHERS:
        n, secs, size = draw(t, key, heads[key], HERE / f"{key}_2026.gif")
        print(f"{key}: {n} frames, {secs:.1f} s, {size / 1024:.0f} KB  | {heads[key]}")


if __name__ == "__main__":
    main()
