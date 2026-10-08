# ============================
# 1) 必要なパッケージのインストール
# ============================
!pip install --quiet pybaseball bar_chart_race
!apt-get update --quiet && apt-get install -y ffmpeg



# ============================
# 2) ライブラリのインポート
# ============================
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pybaseball import statcast, playerid_reverse_lookup
import bar_chart_race as bcr
import matplotlib.animation as animation
from IPython.display import Video, HTML

# ============================
# 3) Statcastデータ取得（2024年3月20日～10月1日）
# ============================
print("Fetching Statcast data, this may take a moment...")
try:
    df = statcast(start_dt='2024-03-20', end_dt='2024-10-01')
except Exception as e:
    print(f"Error fetching Statcast data: {e}")
    sys.exit(1)

if df.empty:
    print("No Statcast data found for the specified period.")
    sys.exit(1)

print("\n--- df (Statcast data) ---")
print(df.head())
print("df shape:", df.shape)






# ============================
# 4) レギュラーシーズンだけ抽出 (game_type == 'R')
# ============================
if 'game_type' in df.columns:
    print("\n--- game_typeの内訳 ---")
    print(df['game_type'].value_counts(dropna=False))

    df = df[df['game_type'] == 'R']
    if df.empty:
        print("No regular season data ('R' in 'game_type') found.")
        sys.exit(1)
else:
    print("'game_type' column not found. Skipping filter by game_type.")

# ============================
# 5) ホームランイベント抽出
# ============================
df_hr = df[df['events'] == 'home_run']
if df_hr.empty:
    print("No home run events found in the (regular season) Statcast data.")
    sys.exit(1)

print("\n--- df_hr (Home Run data) ---")
print(df_hr.head())
print("df_hr shape:", df_hr.shape)

# ============================
# 6) 日付×batter でHR数を集計
# ============================
df_grouped = df_hr.groupby(['game_date', 'batter']).size().reset_index(name='HR')
print("\n--- df_grouped ---")
print(df_grouped.head())
print("df_grouped shape:", df_grouped.shape)

# ============================
# 7) ピボットテーブル作成
#    (index=ゲーム日, columns=選手ID, 値=HR数) + fillna(0)
# ============================
df_pivot = df_grouped.pivot(index='game_date', columns='batter', values='HR').fillna(0)
print("\n--- df_pivot (before reindex) ---")
print(df_pivot.head())
print("df_pivot shape:", df_pivot.shape)

# ============================
# 8) 全日付の補完 (欠損は0埋め)
# ============================
df_pivot.index = pd.to_datetime(df_pivot.index)
df_pivot.sort_index(inplace=True)

# 2024-03-20 ~ 2024-10-01 の全日付を作り、ピボットテーブルを再インデックス
regular_season_dates = pd.date_range(start="2024-03-20", end="2024-10-01")
df_pivot = df_pivot.reindex(regular_season_dates, fill_value=0)

print("\n--- df_pivot (after reindex) ---")
print(df_pivot.head(10))  # 最初の10行をチェック
print(df_pivot.tail(5))

# ============================
# 9) 累積和 cumsum()
# ============================
df_cumsum = df_pivot.cumsum()

print("\n--- df_cumsum (after cumsum) ---")
print(df_cumsum.head(10))  # 最初の10行をチェック
print(df_cumsum.tail(5))
print("df_cumsum shape:", df_cumsum.shape)

# ============================
# 10) batter ID → 選手名変換
# ============================
name_mapping = {}
for batter_id in df_cumsum.columns:
    try:
        info = playerid_reverse_lookup([batter_id], key_type='mlbam')
        if not info.empty:
            full_name = f"{info['name_first'].values[0]} {info['name_last'].values[0]}"
        else:
            full_name = str(batter_id)
    except Exception as e:
        full_name = str(batter_id)
        print(f"Error looking up name for batter ID {batter_id}: {e}")
    name_mapping[batter_id] = full_name

df_cumsum.rename(columns=name_mapping, inplace=True)

# ============================
# 11) 折れ線グラフでざっと確認
# ============================
plt.figure(figsize=(12, 6))
for column in df_cumsum.columns:
    plt.plot(df_cumsum.index, df_cumsum[column], label=column)

plt.xlabel("Date")
plt.ylabel("Cumulative Home Runs")
plt.title("Cumulative Home Runs by Player (2024)")
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True)
plt.tight_layout()
plt.show()


# ============================
# 12) Bar Chart Race の作成 (MP4出力)
# ============================
output_filename = 'hr_race_2024_with_names_full_year.mp4'
bcr.bar_chart_race(
    df=df_cumsum,
    filename=output_filename,  # MP4ファイル出力
    n_bars=10,
    period_fmt='%Y-%m-%d',
    title='2024 Cumulative Home Run Top 10 (Regular Season Only)',
    filter_column_colors=True,
)

print(f"\n動画ファイル '{output_filename}' の生成が完了しました。")

# ============================
# 13) 生成ファイルの存在確認 ＋ ノートブック上で再生
# ============================
print("\n=== ファイルの存在確認 ===")
!ls -lh | grep {output_filename} || echo "No such file: {output_filename}"

print("\n=== ノートブック上でMP4を再生 (埋め込み) ===")
try:
    display(Video(output_filename, embed=True))
except Exception as e:
    print(f"Could not display video: {e}")



