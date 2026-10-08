!pip install pybaseball duckdb -q

from pybaseball import statcast
import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Fetch 2023 season Statcast data
df = statcast(start_dt='2023-03-30', end_dt='2023-08-31')
print(f"Total records: {len(df):,}")

# DuckDB connection
con = duckdb.connect()

# Get Ohtani's pitching appearances
df_ohtani = con.execute("""
    SELECT *
    FROM df
    WHERE pitcher = 660271
      AND pitch_type IS NOT NULL
    ORDER BY game_date, at_bat_number, pitch_number
""").df()

print(f"Ohtani's 2023 pitches: {len(df_ohtani):,}")

# Get unique game dates (start dates)
game_dates = con.execute("""
    SELECT DISTINCT game_date
    FROM df
    WHERE pitcher = 660271
    ORDER BY game_date
""").df()

print(f"Number of starts: {len(game_dates)}")
print(game_dates)

# Calculate baseline statistics (before June 27)
baseline_stats = con.execute("""
    SELECT
        pitch_type,
        ROUND(AVG(release_speed), 2) as avg_speed,
        ROUND(STDDEV(release_speed), 2) as std_speed,
        ROUND(AVG(release_spin_rate), 0) as avg_spin,
        ROUND(STDDEV(release_spin_rate), 0) as std_spin,
        ROUND(AVG(release_pos_x), 3) as avg_release_x,
        ROUND(STDDEV(release_pos_x), 3) as std_release_x,
        ROUND(AVG(release_pos_z), 3) as avg_release_z,
        ROUND(STDDEV(release_pos_z), 3) as std_release_z,
        COUNT(*) as pitch_count
    FROM df
    WHERE pitcher = 660271
      AND game_date < '2023-06-27'
      AND pitch_type IS NOT NULL
    GROUP BY pitch_type
    ORDER BY pitch_count DESC
""").df()

print("Baseline Statistics (before June 27):")
print(baseline_stats.to_string(index=False))

# Calculate daily averages for key metrics
daily_metrics = con.execute("""
    SELECT
        game_date,
        ROUND(AVG(release_speed), 2) as avg_speed,
        ROUND(AVG(release_spin_rate), 0) as avg_spin,
        ROUND(AVG(release_pos_x), 3) as avg_release_x,
        ROUND(AVG(release_pos_z), 3) as avg_release_z,
        ROUND(AVG(release_extension), 3) as avg_extension,
        COUNT(*) as pitch_count
    FROM df
    WHERE pitcher = 660271
      AND pitch_type IS NOT NULL
    GROUP BY game_date
    ORDER BY game_date
""").df()

print("Daily Metrics:")
print(daily_metrics)

# Detect anomalies using ±2σ method with SQL
anomaly_detection = con.execute("""
    WITH baseline AS (
        SELECT
            AVG(release_speed) as baseline_speed,
            STDDEV(release_speed) as std_speed,
            AVG(release_spin_rate) as baseline_spin,
            STDDEV(release_spin_rate) as std_spin,
            AVG(release_pos_x) as baseline_x,
            STDDEV(release_pos_x) as std_x,
            AVG(release_pos_z) as baseline_z,
            STDDEV(release_pos_z) as std_z
        FROM df
        WHERE pitcher = 660271
          AND game_date < '2023-06-27'
          AND pitch_type IS NOT NULL
    ),
    daily_avg AS (
        SELECT
            game_date,
            AVG(release_speed) as daily_speed,
            AVG(release_spin_rate) as daily_spin,
            AVG(release_pos_x) as daily_x,
            AVG(release_pos_z) as daily_z
        FROM df
        WHERE pitcher = 660271
          AND pitch_type IS NOT NULL
        GROUP BY game_date
    )
    SELECT
        d.game_date,
        ROUND(d.daily_speed, 2) as speed,
        CASE
            WHEN d.daily_speed < b.baseline_speed - 2 * b.std_speed THEN 'LOW'
            WHEN d.daily_speed > b.baseline_speed + 2 * b.std_speed THEN 'HIGH'
            ELSE 'NORMAL'
        END as speed_status,
        ROUND(d.daily_spin, 0) as spin,
        CASE
            WHEN d.daily_spin < b.baseline_spin - 2 * b.std_spin THEN 'LOW'
            WHEN d.daily_spin > b.baseline_spin + 2 * b.std_spin THEN 'HIGH'
            ELSE 'NORMAL'
        END as spin_status,
        ROUND(d.daily_x, 3) as release_x,
        CASE
            WHEN d.daily_x < b.baseline_x - 2 * b.std_x THEN 'LOW'
            WHEN d.daily_x > b.baseline_x + 2 * b.std_x THEN 'HIGH'
            ELSE 'NORMAL'
        END as x_status,
        ROUND(d.daily_z, 3) as release_z,
        CASE
            WHEN d.daily_z < b.baseline_z - 2 * b.std_z THEN 'LOW'
            WHEN d.daily_z > b.baseline_z + 2 * b.std_z THEN 'HIGH'
            ELSE 'NORMAL'
        END as z_status
    FROM daily_avg d
    CROSS JOIN baseline b
    ORDER BY d.game_date
""").df()

print("Anomaly Detection Results:")
print(anomaly_detection.to_string(index=False))

# Count anomalies per game
anomaly_counts = con.execute("""
    WITH baseline AS (
        SELECT
            AVG(release_speed) as baseline_speed,
            STDDEV(release_speed) as std_speed,
            AVG(release_spin_rate) as baseline_spin,
            STDDEV(release_spin_rate) as std_spin,
            AVG(release_pos_x) as baseline_x,
            STDDEV(release_pos_x) as std_x,
            AVG(release_pos_z) as baseline_z,
            STDDEV(release_pos_z) as std_z
        FROM df
        WHERE pitcher = 660271
          AND game_date < '2023-06-27'
          AND pitch_type IS NOT NULL
    ),
    pitch_anomalies AS (
        SELECT
            d.game_date,
            CASE WHEN ABS(d.release_speed - b.baseline_speed) > 2 * b.std_speed THEN 1 ELSE 0 END as speed_anomaly,
            CASE WHEN ABS(d.release_spin_rate - b.baseline_spin) > 2 * b.std_spin THEN 1 ELSE 0 END as spin_anomaly,
            CASE WHEN ABS(d.release_pos_x - b.baseline_x) > 2 * b.std_x THEN 1 ELSE 0 END as x_anomaly,
            CASE WHEN ABS(d.release_pos_z - b.baseline_z) > 2 * b.std_z THEN 1 ELSE 0 END as z_anomaly
        FROM df d
        CROSS JOIN baseline b
        WHERE d.pitcher = 660271
          AND d.pitch_type IS NOT NULL
    )
    SELECT
        game_date,
        COUNT(*) as total_pitches,
        SUM(speed_anomaly) as speed_anomalies,
        SUM(spin_anomaly) as spin_anomalies,
        SUM(x_anomaly) as x_anomalies,
        SUM(z_anomaly) as z_anomalies,
        SUM(speed_anomaly + spin_anomaly + x_anomaly + z_anomaly) as total_anomalies,
        ROUND(SUM(speed_anomaly + spin_anomaly + x_anomaly + z_anomaly) * 100.0 / COUNT(*), 1) as anomaly_rate
    FROM pitch_anomalies
    GROUP BY game_date
    ORDER BY game_date
""").df()

print("Anomaly Counts per Game:")
print(anomaly_counts.to_string(index=False))

# Get pitch-level data with calculated metric using SQL
df_plot = con.execute("""
    SELECT
        game_date,
        pitch_type,
        pitch_number,
        release_pos_x,
        release_pos_z,
        release_spin_rate,
        SQRT(POWER(release_pos_x, 2) + POWER(release_pos_z, 2)) * release_spin_rate as metric
    FROM df
    WHERE pitcher = 660271
      AND pitch_type IS NOT NULL
      AND release_pos_x IS NOT NULL
      AND release_pos_z IS NOT NULL
      AND release_spin_rate IS NOT NULL
    ORDER BY game_date, pitch_number
""").df()

# Get unique dates and pitch types
dates = df_plot['game_date'].unique()
pitch_types = [pt for pt in df_plot['pitch_type'].unique() if pt is not None and pd.notna(pt)]

# Plot
fig, axs = plt.subplots(len(pitch_types), 1, figsize=(16, len(pitch_types) * 5))
if len(pitch_types) == 1:
    axs = [axs]

for i, pitch_type in enumerate(pitch_types):
    ax = axs[i]
    total_pitch_count = 0
    all_values = []

    for date in dates:
        date_data = df_plot[(df_plot['game_date'] == date) & (df_plot['pitch_type'] == pitch_type)]
        if not date_data.empty:
            x_values = [total_pitch_count + k for k in range(1, len(date_data) + 1)]
            total_pitch_count += len(date_data)
            metric_values = date_data['metric'].values
            date_str = pd.to_datetime(date).strftime("%m/%d")
            ax.scatter(x_values, metric_values, label=date_str, alpha=0.7, s=15)
            all_values.extend(metric_values.tolist())

    if all_values:
        avg = np.mean(all_values)
        std_dev = np.std(all_values)
        ax.axhline(avg, color='r', linestyle='--', linewidth=2, label='Average')
        ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', linewidth=2, label='Average + 2σ')
        ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', linewidth=2, label='Average - 2σ')

    ax.set_title(f"Pitch Type: {pitch_type}", fontsize=12)
    ax.set_xlabel('Total Pitch Count')
    ax.set_ylabel('√(pos_x² + pos_z²) × spin_rate')
    # Move legend below the plot
    ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=len(dates)//2 + 1, fontsize=7)
    ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

fig.suptitle('Ohtani 2023 - Release Position × Spin Rate by Pitch Count\n(Note: Outliers increase toward end of season)', fontsize=14, y=1.02)
plt.tight_layout(pad=3)
plt.subplots_adjust(hspace=0.5)
plt.show()

# Calculate anomaly rate by period using SQL
anomaly_stats = con.execute("""
    WITH metrics AS (
        SELECT
            game_date,
            SQRT(POWER(release_pos_x, 2) + POWER(release_pos_z, 2)) * release_spin_rate as metric
        FROM df
        WHERE pitcher = 660271
          AND pitch_type IS NOT NULL
          AND release_pos_x IS NOT NULL
          AND release_pos_z IS NOT NULL
          AND release_spin_rate IS NOT NULL
    ),
    stats AS (
        SELECT AVG(metric) as avg_metric, STDDEV(metric) as std_metric FROM metrics
    )
    SELECT
        CASE WHEN m.game_date < '2023-06-27' THEN 'Before June 27' ELSE 'After June 27' END as period,
        COUNT(*) as total,
        SUM(CASE WHEN ABS(m.metric - s.avg_metric) > 2 * s.std_metric THEN 1 ELSE 0 END) as anomalies,
        ROUND(SUM(CASE WHEN ABS(m.metric - s.avg_metric) > 2 * s.std_metric THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as anomaly_rate
    FROM metrics m
    CROSS JOIN stats s
    GROUP BY period
    ORDER BY period DESC
""").df()

print("\n=== Anomaly Rate Comparison (±2σ) ===")
print(anomaly_stats.to_string(index=False))
