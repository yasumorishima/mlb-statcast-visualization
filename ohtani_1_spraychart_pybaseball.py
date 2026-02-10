!pip install pybaseball duckdb -q

from pybaseball import statcast, spraychart
import duckdb

# ====== 設定 ======
BATTER_ID = 660271      # 大谷翔平 MLBAM ID
SEASON_YEAR = 2025
GAME_TYPE = "R"         # "R"=レギュラーシーズン, "P"=ポストシーズン, None=全試合
# ==================

# Statcastデータ取得
df_raw = statcast(start_dt=f'{SEASON_YEAR}-03-01', end_dt=f'{SEASON_YEAR}-12-31')
print(f"Total records (raw): {len(df_raw):,}")

# game_typeでフィルタ
con = duckdb.connect()
if GAME_TYPE:
    df = con.execute(f"""
        SELECT * FROM df_raw WHERE game_type = '{GAME_TYPE}'
    """).df()
    print(f"Filtered records (game_type='{GAME_TYPE}'): {len(df):,}")
else:
    df = df_raw.copy()
    print(f"Using all game types: {len(df):,}")

# DuckDB で大谷のデータを抽出
df_hits = con.execute("""
    SELECT * FROM df
    WHERE batter = 660271
      AND events IN ('home_run', 'double', 'triple', 'single')
      AND hc_x IS NOT NULL AND hc_y IS NOT NULL
""").df()

df_all = con.execute("""
    SELECT * FROM df
    WHERE batter = 660271
      AND hc_x IS NOT NULL AND hc_y IS NOT NULL
""").df()

df_hr = con.execute("""
    SELECT * FROM df
    WHERE batter = 660271
      AND events = 'home_run'
      AND hc_x IS NOT NULL AND hc_y IS NOT NULL
""").df()

print(f"Hits: {len(df_hits)}, All: {len(df_all)}, HR: {len(df_hr)}")

# 汎用スタジアム + イベント別色分け（全データ）
spraychart(df_hits, 'generic', title='Ohtani 2025 Hits (All Stadiums)', colorby='events')

# 全打球
spraychart(df_all, 'generic', title='Ohtani 2025 All Batted Balls', colorby='events')

# 球場 → チームコードのマッピング
STADIUM_TEAMS = {
    'angels': 'LAA', 'dodgers': 'LAD', 'yankees': 'NYY', 'red_sox': 'BOS',
    'astros': 'HOU', 'mariners': 'SEA', 'athletics': 'OAK', 'rangers': 'TEX',
    'padres': 'SD', 'giants': 'SF', 'cubs': 'CHC', 'white_sox': 'CWS',
    'twins': 'MIN', 'tigers': 'DET', 'royals': 'KC', 'guardians': 'CLE',
    'rays': 'TB', 'orioles': 'BAL', 'blue_jays': 'TOR', 'mets': 'NYM',
    'phillies': 'PHI', 'nationals': 'WSH', 'marlins': 'MIA', 'braves': 'ATL',
    'reds': 'CIN', 'brewers': 'MIL', 'cardinals': 'STL', 'pirates': 'PIT',
    'rockies': 'COL', 'diamondbacks': 'AZ'
}

def spraychart_by_stadium(df_data, stadium_name, con):
    """指定した球場でプレイしたデータのみをフィルターして表示"""
    team_code = STADIUM_TEAMS.get(stadium_name)
    if not team_code:
        print(f"Unknown stadium: {stadium_name}")
        return

    df_stadium = con.execute(f"""
        SELECT * FROM df_data WHERE home_team = '{team_code}'
    """).df()

    if len(df_stadium) == 0:
        print(f"No data at {stadium_name} ({team_code})")
        return

    print(f"{stadium_name.upper()} ({team_code}): {len(df_stadium)} batted balls")
    spraychart(df_stadium, stadium_name,
               title=f'Ohtani 2025 @ {stadium_name.title()} ({len(df_stadium)} balls)',
               colorby='events')

# 各球場でのデータ件数を確認
stadium_counts = con.execute("""
    SELECT home_team, COUNT(*) as balls, SUM(CASE WHEN events = 'home_run' THEN 1 ELSE 0 END) as HR
    FROM df_all
    GROUP BY home_team
    ORDER BY balls DESC
""").df()

print("=== Batted Balls by Stadium ===")
print(stadium_counts.to_string(index=False))

# ドジャースタジアム（ホーム）
spraychart_by_stadium(df_all, 'dodgers', con)

# パドレス（アウェイ・同地区）
spraychart_by_stadium(df_all, 'padres', con)

# ジャイアンツ（アウェイ・同地区）
spraychart_by_stadium(df_all, 'giants', con)

# HR球場別
hr_by_stadium = con.execute("""
    SELECT home_team, COUNT(*) as HR FROM df_hr GROUP BY home_team ORDER BY HR DESC
""").df()
print("=== Home Runs by Stadium ===")
print(hr_by_stadium.to_string(index=False))

# ドジャースタジアムでのホームラン
df_hr_dodgers = con.execute("SELECT * FROM df_hr WHERE home_team = 'LAD'").df()
if len(df_hr_dodgers) > 0:
    print(f"HR at Dodger Stadium: {len(df_hr_dodgers)}")
    spraychart(df_hr_dodgers, 'dodgers', title=f'Ohtani 2025 HRs @ Dodger Stadium ({len(df_hr_dodgers)})')
