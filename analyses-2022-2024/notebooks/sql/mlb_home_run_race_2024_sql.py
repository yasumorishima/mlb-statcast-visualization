!pip install pybaseball duckdb bar_chart_race -q
!apt-get update --quiet && apt-get install -y ffmpeg -qq

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pybaseball import statcast, playerid_reverse_lookup
import duckdb
import bar_chart_race as bcr
from IPython.display import Video

# Fetch 2024 season Statcast data
print("Fetching Statcast data...")
df = statcast(start_dt='2024-03-20', end_dt='2024-10-01')
print(f"Total records: {len(df):,}")

# DuckDB connection
con = duckdb.connect()

# Extract home runs from regular season using SQL
df_hr = con.execute("""
    SELECT
        game_date,
        batter,
        events
    FROM df
    WHERE game_type = 'R'
      AND events = 'home_run'
    ORDER BY game_date, batter
""").df()

print(f"Total home runs in 2024 regular season: {len(df_hr):,}")

# Aggregate HR count by date and batter using SQL
df_daily_hr = con.execute("""
    SELECT
        game_date,
        batter,
        COUNT(*) as hr_count
    FROM df
    WHERE game_type = 'R'
      AND events = 'home_run'
    GROUP BY game_date, batter
    ORDER BY game_date, batter
""").df()

print("Daily HR counts:")
print(df_daily_hr.head(10))

# Calculate cumulative HR using SQL window functions
df_cumulative = con.execute("""
    WITH daily_hr AS (
        SELECT
            game_date,
            batter,
            COUNT(*) as hr_count
        FROM df
        WHERE game_type = 'R'
          AND events = 'home_run'
        GROUP BY game_date, batter
    )
    SELECT
        game_date,
        batter,
        hr_count,
        SUM(hr_count) OVER (
            PARTITION BY batter
            ORDER BY game_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) as cumulative_hr
    FROM daily_hr
    ORDER BY game_date, batter
""").df()

print("Cumulative HR (sample):")
print(df_cumulative.head(20))

# Get final HR totals using SQL
df_final = con.execute("""
    SELECT
        batter,
        COUNT(*) as total_hr
    FROM df
    WHERE game_type = 'R'
      AND events = 'home_run'
    GROUP BY batter
    ORDER BY total_hr DESC
    LIMIT 15
""").df()

# Map batter IDs to names
name_mapping = {}
for batter_id in df_final['batter']:
    try:
        info = playerid_reverse_lookup([batter_id], key_type='mlbam')
        if not info.empty:
            name_mapping[batter_id] = f"{info['name_first'].values[0]} {info['name_last'].values[0]}"
        else:
            name_mapping[batter_id] = str(batter_id)
    except:
        name_mapping[batter_id] = str(batter_id)

df_final['player_name'] = df_final['batter'].map(name_mapping)

print("2024 HR Leaders:")
print(df_final[['player_name', 'total_hr']].to_string(index=False))

# Create pivot table using SQL and pandas
# First get all unique dates and batters
df_pivot_data = con.execute("""
    WITH daily_hr AS (
        SELECT
            CAST(game_date AS DATE) as game_date,
            batter,
            COUNT(*) as hr_count
        FROM df
        WHERE game_type = 'R'
          AND events = 'home_run'
        GROUP BY game_date, batter
    )
    SELECT * FROM daily_hr
""").df()

# Pivot and cumsum in pandas (DuckDB's PIVOT is limited)
df_pivot = df_pivot_data.pivot(index='game_date', columns='batter', values='hr_count').fillna(0)
df_pivot.index = pd.to_datetime(df_pivot.index)
df_pivot.sort_index(inplace=True)

# Reindex to fill missing dates
all_dates = pd.date_range(start='2024-03-20', end='2024-10-01')
df_pivot = df_pivot.reindex(all_dates, fill_value=0)

# Cumulative sum
df_cumsum = df_pivot.cumsum()

# Rename columns to player names
df_cumsum.rename(columns=name_mapping, inplace=True)

print("Pivot table shape:", df_cumsum.shape)
print(df_cumsum.tail())

# Generate bar chart race animation
output_filename = 'hr_race_2024_sql.mp4'

bcr.bar_chart_race(
    df=df_cumsum,
    filename=output_filename,
    n_bars=10,
    period_fmt='%Y-%m-%d',
    title='2024 MLB Home Run Race (SQL Version)',
    filter_column_colors=True,
)

print(f"Animation saved: {output_filename}")

# Display the video
display(Video(output_filename, embed=True))
