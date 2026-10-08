!pip install pybaseball duckdb -q

from pybaseball import statcast
import duckdb
import matplotlib.pyplot as plt
import seaborn as sns

# Fetch 2022 season Statcast data
df = statcast(start_dt='2022-03-30', end_dt='2022-12-31')
print(f"Total records: {len(df):,}")

# DuckDB connection
con = duckdb.connect()

# Extract Ohtani's hit data using SQL
# Ohtani's batter ID: 660271
df_ohtani_hits = con.execute("""
    SELECT *
    FROM df
    WHERE batter = 660271
      AND events IN ('home_run', 'double', 'triple', 'single')
      AND hc_x IS NOT NULL
      AND hc_y IS NOT NULL
""").df()

# Extract Ohtani's out data using SQL
df_ohtani_outs = con.execute("""
    SELECT *
    FROM df
    WHERE batter = 660271
      AND events NOT IN ('home_run', 'double', 'triple', 'single')
      AND hc_x IS NOT NULL
      AND hc_y IS NOT NULL
""").df()

print(f"Hits: {len(df_ohtani_hits)}")
print(f"Outs: {len(df_ohtani_outs)}")

# Count hits by event type using SQL
hit_counts = con.execute("""
    SELECT
        events,
        COUNT(*) as count
    FROM df
    WHERE batter = 660271
      AND events IN ('home_run', 'double', 'triple', 'single')
    GROUP BY events
    ORDER BY count DESC
""").df()

print("Ohtani 2022 Hit Distribution:")
print(hit_counts)

# Extract plate location data for hits and outs
df_hits_zone = con.execute("""
    SELECT plate_x, plate_z, events
    FROM df
    WHERE batter = 660271
      AND events IN ('home_run', 'double', 'triple', 'single')
      AND plate_x IS NOT NULL
      AND plate_z IS NOT NULL
""").df()

df_outs_zone = con.execute("""
    SELECT plate_x, plate_z, events
    FROM df
    WHERE batter = 660271
      AND (events NOT IN ('home_run', 'double', 'triple', 'single') OR events IS NULL)
      AND plate_x IS NOT NULL
      AND plate_z IS NOT NULL
""").df()

# Plot strike zone heatmap
fig, axs = plt.subplots(1, 2, figsize=(14, 6), sharex=True, sharey=True)

# Strike zone coordinates
x = [-0.88, 0.88, 0.88, -0.88, -0.88]
y = [1.51, 1.51, 3.4, 3.4, 1.51]

sns.histplot(data=df_outs_zone, x='plate_x', y='plate_z', cmap="coolwarm", cbar=True, ax=axs[0], binwidth=0.5)
axs[0].plot(x, y, linestyle='--', color='black')
axs[0].set_title('Outs - Plate Location')

sns.histplot(data=df_hits_zone, x='plate_x', y='plate_z', cmap="coolwarm_r", cbar=True, ax=axs[1], binwidth=0.5)
axs[1].plot(x, y, linestyle='--', color='black')
axs[1].set_title('Hits - Plate Location')

plt.tight_layout()
plt.show()

def plot_hit_vs_out(outs, hits):
    # Invert Y values for proper field orientation
    outs = outs.copy()
    hits = hits.copy()
    outs['hc_y'] = -outs['hc_y']
    hits['hc_y'] = -hits['hc_y']

    fig, axs = plt.subplots(1, 2, figsize=(16, 8), sharex=True, sharey=True)
    plt.subplots_adjust(wspace=0.1)

    # Draw foul lines
    def draw_foul_lines(ax):
        ax.plot([125, 250], [-210, -85], 'k-', lw=3)
        ax.plot([125, 0], [-210, -85], 'k-', lw=3)

    # Outs heatmap
    sns.histplot(data=outs, x='hc_x', y='hc_y', cmap="coolwarm", cbar=True, ax=axs[0], binwidth=10)
    axs[0].set_title('Outs - Batted Ball Direction')
    axs[0].set_xlabel('X coordinate')
    axs[0].set_ylabel('Y coordinate')
    draw_foul_lines(axs[0])

    # Hits heatmap
    sns.histplot(data=hits, x='hc_x', y='hc_y', cmap="coolwarm", cbar=True, ax=axs[1], binwidth=10)
    axs[1].set_title('Hits - Batted Ball Direction')
    axs[1].set_xlabel('X coordinate')
    axs[1].set_ylabel('Y coordinate')
    draw_foul_lines(axs[1])

    plt.suptitle('Shohei Ohtani 2022 - Batted Ball Distribution', fontsize=14, y=1.02)
    plt.show()

# Execute visualization
plot_hit_vs_out(df_ohtani_outs, df_ohtani_hits)

# Calculate batting statistics using SQL
batting_stats = con.execute("""
    WITH ohtani_abs AS (
        SELECT *
        FROM df
        WHERE batter = 660271
          AND events IS NOT NULL
          AND events NOT IN ('walk', 'hit_by_pitch', 'sac_fly', 'sac_bunt', 'catcher_interf')
    )
    SELECT
        COUNT(*) as at_bats,
        SUM(CASE WHEN events IN ('single', 'double', 'triple', 'home_run') THEN 1 ELSE 0 END) as hits,
        SUM(CASE WHEN events = 'home_run' THEN 1 ELSE 0 END) as home_runs,
        SUM(CASE WHEN events = 'double' THEN 1 ELSE 0 END) as doubles,
        SUM(CASE WHEN events = 'triple' THEN 1 ELSE 0 END) as triples,
        ROUND(SUM(CASE WHEN events IN ('single', 'double', 'triple', 'home_run') THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 3) as batting_avg
    FROM ohtani_abs
""").df()

print("Ohtani 2022 Batting Statistics (from Statcast):")
print(batting_stats.to_string(index=False))
