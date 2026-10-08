# https://baseballsavant.mlb.com/savant-player/shohei-ohtani-660271?stats=gamelogs-r-pitching-mlb&season=2023

!pip install pybaseball

import pandas as pd
from pybaseball import statcast

dates = [
'2023-03-30', '2023-04-05', '2023-04-11', '2023-04-17',
'2023-04-21', '2023-04-27', '2023-05-03', '2023-05-09',
'2023-05-15', '2023-05-21', '2023-05-27', '2023-06-02',
'2023-06-09', '2023-06-15', '2023-06-21', '2023-06-27',
'2023-07-04', '2023-07-14', '2023-07-21', '2023-07-27',
'2023-08-03', '2023-08-09', '2023-08-23'
]


# Create an empty DataFrame to store the data
df_660271_all_dates = pd.DataFrame()

# Fetch data for each date and concatenate
for date in dates:
    df_single_day = statcast(start_dt=date, end_dt=date)
    df_660271_single_day = df_single_day[df_single_day['pitcher'] == 660271]
    df_660271_all_dates = pd.concat([df_660271_all_dates, df_660271_single_day])

# Reset the index of the final DataFrame
df_660271_all_dates.reset_index(drop=True, inplace=True)


# 投球結果を抽出
df_660271 = df_660271_all_dates

# df_660271のpitch_typeカラムに含まれるユニークな球種を確認する
unique_pitch_types = df_660271['pitch_type'].unique()

# 確認した球種を表示する
print(unique_pitch_types)


import pandas as pd

def pitch_counts(df):
    # 左打者と右打者に対する投球データを抽出
    df_L = df[df['stand'] == 'L']
    df_R = df[df['stand'] == 'R']

    # 各カテゴリーでの球種の出現回数をカウント
    total_counts = df['pitch_type'].value_counts()
    left_counts = df_L['pitch_type'].value_counts()
    right_counts = df_R['pitch_type'].value_counts()

    # 出現回数をデータフレームにまとめる
    pitch_counts_table = pd.DataFrame({'Total': total_counts, 'Left Batter': left_counts, 'Right Batter': right_counts})

    # NaNを0に置き換える
    pitch_counts_table.fillna(0, inplace=True)

    # カウントを整数に変換する
    pitch_counts_table = pitch_counts_table.astype(int)

    return pitch_counts_table

# Loop through each date
for date in dates:
    # Split the data by date
    df_date = df_660271_all_dates[df_660271_all_dates['game_date'] == date]

    # Get pitch counts for the date
    pitch_counts_date = pitch_counts(df_date)

    # Display the results
    print(f"{date}の球種カウント:")
    print(pitch_counts_date)
    print("\n")


import matplotlib.pyplot as plt

def plot_pitch_distribution(df, date):
    df_L = df[df['stand'] == 'L']
    df_R = df[df['stand'] == 'R']

    fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    plt.suptitle(f'Pitch Distribution on {date}')

    colors = {'FF': 'red', 'SL': 'blue', 'FS': 'green', 'ST': 'orange', 'CU': 'purple', 'SI': 'brown', 'FC': 'grey'}
    df['pitch_type'].value_counts().plot(kind='pie', ax=axs[0], autopct='%.1f%%', colors=[colors.get(key, 'grey') for key in df['pitch_type'].value_counts().index])  # use get method with default value
    axs[0].set_title('Total')
    axs[0].set_ylabel('')

    # vs Left batter
    if not df_L['pitch_type'].value_counts().empty:
        df_L['pitch_type'].value_counts().plot(kind='pie', ax=axs[1], autopct='%.1f%%', colors=[colors.get(key, 'grey') for key in df_L['pitch_type'].value_counts().index])  # use get method with default value
        axs[1].set_title('vs Left batter')
        axs[1].set_ylabel('')

    # vs Right batter
    if not df_R['pitch_type'].value_counts().empty:
        df_R['pitch_type'].value_counts().plot(kind='pie', ax=axs[2], autopct='%.1f%%', colors=[colors.get(key, 'grey') for key in df_R['pitch_type'].value_counts().index])  # use get method with default value
        axs[2].set_title('vs Right batter')
        axs[2].set_ylabel('')

    plt.show()

for date in dates:
    df_date = df_660271_all_dates[df_660271_all_dates['game_date'] == date]
    plot_pitch_distribution(df_date, date)


import matplotlib.pyplot as plt
import numpy as np

def plot_pitch_distribution(df, date, ax):
    colors = {'FF': 'red', 'SL': 'blue', 'FS': 'green', 'ST': 'orange', 'CU': 'purple', 'SI': 'brown', 'FC': 'grey'}

    # Function to format percentage and change its color to white
    def white_autopct(pct):
        return ('%.1f%%' % pct) if pct > 0 else ''

    # Total
    if not df['pitch_type'].value_counts().empty:
        df['pitch_type'].value_counts().plot(kind='pie', ax=ax, autopct=white_autopct, colors=[colors.get(key, 'grey') for key in df['pitch_type'].value_counts().index], textprops={'color':"white"})
        ax.set_title(f'Total on {date}', color='white')
        ax.set_ylabel('')
        ax.set_facecolor('#333333')  # set background color of the subplot

# Compute the number of rows needed for the subplots
num_rows = int(np.ceil(len(dates) / 4))

fig, axs = plt.subplots(num_rows, 4, figsize=(24, 6*num_rows), facecolor='#333333')  # adjust figsize as needed and set background color of the figure
plt.rcParams['text.color'] = 'white'  # set global text color to white

for i, date in enumerate(dates):
    row = i // 4
    col = i % 4
    df_date = df_660271_all_dates[df_660271_all_dates['game_date'] == date]
    plot_pitch_distribution(df_date, date, axs[row, col])

# Remove empty subplots
if len(dates) % 4 != 0:
    for j in range(len(dates) % 4, 4):
        fig.delaxes(axs[-1, j])

plt.suptitle('Pitch Distribution')
plt.tight_layout()
plt.show()


import matplotlib.pyplot as plt

def plot_pitch_distribution(df, title, ax):
    colors = {'FF': 'red', 'SL': 'blue', 'FS': 'green', 'ST': 'orange', 'CU': 'purple', 'SI': 'brown', 'FC': 'grey'}

    # Function to format percentage and change its color to white
    def white_autopct(pct):
        return ('%.1f%%' % pct) if pct > 0 else ''

    # Total
    if not df['pitch_type'].value_counts().empty:
        df['pitch_type'].value_counts().plot(kind='pie', ax=ax, autopct=white_autopct, colors=[colors.get(key, 'grey') for key in df['pitch_type'].value_counts().index], textprops={'color':"white"})
        ax.set_title(title, color='white')
        ax.set_ylabel('')
        ax.set_facecolor('#333333')  # set background color of the subplot

# Split the dataframe into two based on the date
df_june27 = df_660271_all_dates[df_660271_all_dates['game_date'] == '2023-07-04']
df_other_dates = df_660271_all_dates[df_660271_all_dates['game_date'] != '2023-07-04']

fig, axs = plt.subplots(1, 2, figsize=(12, 6), facecolor='#333333')  # adjust figsize as needed and set background color of the figure
plt.rcParams['text.color'] = 'white'  # set global text color to white

# Plot pitch distribution for June 27
plot_pitch_distribution(df_june27, 'Total on 2023-07-04', axs[0])

# Plot pitch distribution for other dates
plot_pitch_distribution(df_other_dates, 'Total on other dates', axs[1])

plt.suptitle('Pitch Distribution Comparison')
plt.tight_layout()
plt.show()


plt.rcParams['text.color'] = 'black'

import matplotlib.pyplot as plt

def plot_pitch_location(df, date):
    # データを pitch_type ごとにグループ分けする
    grouped = df.groupby('pitch_type')

    colors = {'FF': 'red', 'SL': 'blue', 'FS': 'green', 'ST': 'orange', 'CU': 'purple', 'SI': 'brown', 'FC': 'grey'}

    # pitch_type ごとに、'plate_x' を X 軸、'plate_z' を Y 軸とした散布図を作成する
    for pitch_type, data in grouped:
        plt.scatter(data['plate_x'], data['plate_z'], label=pitch_type, color=colors.get(pitch_type, 'grey'))  # use get method with default value

    # ストライクゾーン
    x = [-0.88, 0.88, 0.88, -0.88, -0.88]
    y = [1.51, 1.51, 3.4, 3.4, 1.51]
    plt.fill(x, y, color='r', alpha=0.1)

    # 凡例を表示する
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)

    plt.xlim(-5, 5)
    plt.ylim(-1, 6)

    plt.xlabel('Plate X')
    plt.ylabel('Plate Z')

    # 罫線
    plt.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    plt.title(f'Pitch Location on {date}')

    # グラフを表示する
    plt.show()


for date in dates:
    df_date = df_660271_all_dates[df_660271_all_dates['game_date'] == date]
    plot_pitch_location(df_date, date)


import matplotlib.pyplot as plt

def plot_release_point(df, date):
    grouped = df.groupby('pitch_type')

    colors = {'FF': 'red', 'SL': 'blue', 'FS': 'green', 'ST': 'orange', 'CU': 'purple', 'SI': 'brown', 'FC': 'grey'}

    for pitch_type, data in grouped:
        plt.scatter(data['release_pos_x'], data['release_pos_z'], label=pitch_type, color=colors.get(pitch_type, 'grey'))  # use get method with default value

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)

    plt.xlabel('Release Pos X')
    plt.ylabel('Release Pos Z')

    plt.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    plt.title(f'Release Point for {date}')

    plt.xlim(-3.5, -1)
    plt.ylim(4.5, 7.5)

    plt.show()

for date in dates:
    df_date = df_660271_all_dates[df_660271_all_dates['game_date'] == date]
    plot_release_point(df_date, date)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_spin_rate_by_date_boxplot(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = []
        labels = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_spin_rate'])

            if not grouped.empty:
                data_to_plot.append(grouped['release_spin_rate'])
                # 日付を短縮形に変換
                short_date = datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d")
                labels.append(short_date)

        if data_to_plot:
            bp = ax.boxplot(data_to_plot, labels=labels)
            for j, d in enumerate(data_to_plot):
                mean_val = d.mean()
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Date')
        ax.set_ylabel('Release Spin Rate')

        # 罫線
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Release Spin Rate by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()


# すべての日に存在する球種を取得
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_spin_rate_by_date_boxplot(dfs, all_pitch_types, dates)


from datetime import datetime

def plot_spin_rate_by_date_boxplot(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = []
        labels = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_spin_rate'])

            if not grouped.empty:
                data_to_plot.append(grouped['release_spin_rate'])
                # 日付を短縮形に変換
                short_date = datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d")
                labels.append(short_date)

        if data_to_plot:
            bp = ax.boxplot(data_to_plot, labels=labels)
            for j, d in enumerate(data_to_plot):
                max_val = d.max()  # ボックスプロットの最大値を取得
                mean_val = d.mean()  # 平均値を取得
                ax.text(j + 1, max_val, f" {mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Date')
        ax.set_ylabel('Release Spin Rate')

        # 罫線
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Release Spin Rate by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()


dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_spin_rate_by_date_boxplot(dfs, all_pitch_types, dates)


from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

def plot_spin_rate_by_date_boxplot(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()
            df.loc[:, 'month'] = pd.to_datetime(df['game_date']).dt.to_period('M')


            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_spin_rate']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend(group['release_spin_rate'].tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('Release Spin Rate')
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Release Spin Rate by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下の部分はサンプルです。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_spin_rate_by_date_boxplot(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_release_spin_rate_by_date_scatter(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        all_values = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_spin_rate', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                ax.scatter(x_values, grouped['release_spin_rate'], label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))
                all_values.extend(grouped['release_spin_rate'].tolist())

        if all_values:
            avg = np.mean(all_values)
            std_dev = np.std(all_values)
            ax.axhline(avg, color='r', linestyle='--', label='Average')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ')  # 2σを追加
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ')  # 2σを追加

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('Release Spin Rate')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Release Spin Rate by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_release_spin_rate_by_date_scatter(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_release_speed_by_date_boxplot(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = []
        labels = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_speed'])

            if not grouped.empty:
                data_to_plot.append(grouped['release_speed'])
                # 日付を短縮形に変換
                short_date = datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d")
                labels.append(short_date)

        if data_to_plot:
            bp = ax.boxplot(data_to_plot, labels=labels)
            for j, d in enumerate(data_to_plot):
                mean_val = d.mean()
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Date')
        ax.set_ylabel('Release Speed')

        # 罫線
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Release Speed by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()


# すべての日に存在する球種を取得
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_release_speed_by_date_boxplot(dfs, all_pitch_types, dates)


def plot_release_speed_by_date_boxplot(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = []
        labels = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_speed'])

            if not grouped.empty:
                # マイル/時間をキロメートル/時間に変換
                data_to_plot.append(grouped['release_speed'] * 1.60934)
                short_date = datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d")
                labels.append(short_date)

        if data_to_plot:
            bp = ax.boxplot(data_to_plot, labels=labels)
            for j, d in enumerate(data_to_plot):
                mean_val = d.mean()
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Date')
        ax.set_ylabel('Release Speed (km/h)')

        # 罫線
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Release Speed by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()


dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_release_speed_by_date_boxplot(dfs, all_pitch_types, dates)


from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

def plot_release_speed_by_date_boxplot(dfs, pitch_types):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()  # DataFrameのコピーを作成
            df['month'] = pd.to_datetime(df['game_date']).dt.to_period('M')  # 月に変換
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_speed']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend((group['release_speed'] * 1.60934).tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('Release Speed (km/h)')
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Release Speed by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下の部分はサンプルです。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_release_speed_by_date_boxplot(dfs, all_pitch_types)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_release_speed_by_date_scatter(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        all_values = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_speed', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                ax.scatter(x_values, grouped['release_speed'], label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))
                all_values.extend(grouped['release_speed'].tolist())

        if all_values:
            avg = np.mean(all_values)
            std_dev = np.std(all_values)
            ax.axhline(avg, color='r', linestyle='--', label='Average')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ')  # 2σを追加
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ')  # 2σを追加

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('Release Speed')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Release Speed by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_release_speed_by_date_scatter(dfs, all_pitch_types, dates)


from datetime import datetime

def plot_release_extension_by_date_boxplot(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = []
        labels = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_extension'])

            if not grouped.empty:
                data_to_plot.append(grouped['release_extension'])
                short_date = datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d")
                labels.append(short_date)

        if data_to_plot:
            bp = ax.boxplot(data_to_plot, labels=labels)
            for j, d in enumerate(data_to_plot):
                mean_val = d.mean()
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Date')
        ax.set_ylabel('Release Extension (ft)')

        # 罫線
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Release Extension by Date and Pitch Type (ft)', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()


dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_release_extension_by_date_boxplot(dfs, all_pitch_types, dates)


from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

def plot_release_extension_by_date_boxplot(dfs, pitch_types):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()  # DataFrameのコピーを作成
            df['month'] = pd.to_datetime(df['game_date']).dt.to_period('M')  # 月に変換
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_extension']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend(group['release_extension'].tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('Release Extension (ft)')
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Release Extension by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下の部分はサンプルです。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_release_extension_by_date_boxplot(dfs, all_pitch_types)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_release_extension_by_date_scatter(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        all_values = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_extension', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                ax.scatter(x_values, grouped['release_extension'], label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))
                all_values.extend(grouped['release_extension'].tolist())

        if all_values:
            avg = np.mean(all_values)
            std_dev = np.std(all_values)
            ax.axhline(avg, color='r', linestyle='--', label='Average')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ')  # 2σを追加
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ')  # 2σを追加

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('Release Extension')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Release Extension by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_release_extension_by_date_scatter(dfs, all_pitch_types, dates)


from datetime import datetime

def plot_spin_axis_by_date_boxplot(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = []
        labels = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['spin_axis'])

            if not grouped.empty:
                data_to_plot.append(grouped['spin_axis'])
                short_date = datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d")
                labels.append(short_date)

        if data_to_plot:
            bp = ax.boxplot(data_to_plot, labels=labels)
            for j, d in enumerate(data_to_plot):
                mean_val = d.mean()
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Date')
        ax.set_ylabel('Spin Axis')

        # 罫線
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Spin Axis by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()


dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_spin_axis_by_date_boxplot(dfs, all_pitch_types, dates)


from datetime import datetime

def plot_spin_axis_by_date_boxplot(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = []
        labels = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['spin_axis'])

            if not grouped.empty:
                data_to_plot.append(grouped['spin_axis'])
                short_date = datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d")
                labels.append(short_date)

        if data_to_plot:
            bp = ax.boxplot(data_to_plot, labels=labels)
            for j, d in enumerate(data_to_plot):
                min_val = d.min()
                mean_val = d.mean()
                ax.text(j + 1, min_val, f": {mean_val:.1f}", ha='center', va='top', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Date')
        ax.set_ylabel('Spin Axis')

        # 罫線
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Spin Axis by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_spin_axis_by_date_boxplot(dfs, all_pitch_types, dates)


from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

def plot_spin_axis_by_date_boxplot(dfs, pitch_types):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()  # DataFrameのコピーを作成
            df['month'] = pd.to_datetime(df['game_date']).dt.to_period('M')  # 月に変換
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['spin_axis']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend(group['spin_axis'].tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('Spin Axis')
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Spin Axis by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下の部分はサンプルです。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_spin_axis_by_date_boxplot(dfs, all_pitch_types)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_spin_axis_by_date_scatter(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        all_values = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['spin_axis', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                ax.scatter(x_values, grouped['spin_axis'], label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))
                all_values.extend(grouped['spin_axis'].tolist())

        if all_values:
            avg = np.mean(all_values)
            std_dev = np.std(all_values)
            ax.axhline(avg, color='r', linestyle='--', label='Average')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ')  # 2σを追加
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ')  # 2σを追加

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('Spin Axis')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Spin Axis by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_spin_axis_by_date_scatter(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_plate_z_by_date_boxplot(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = []
        labels = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['plate_z'])

            if not grouped.empty:
                data_to_plot.append(grouped['plate_z'])
                short_date = datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d")
                labels.append(short_date)

        if data_to_plot:
            bp = ax.boxplot(data_to_plot, labels=labels)
            for j, d in enumerate(data_to_plot):
                mean_val = d.mean()
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Date')
        ax.set_ylabel('Plate Z')

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Plate Z by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_plate_z_by_date_boxplot(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_plate_z_by_date_boxplot(dfs, pitch_types):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()  # DataFrameのコピーを作成
            df['month'] = pd.to_datetime(df['game_date']).dt.to_period('M')  # 月に変換
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['plate_z']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend(group['plate_z'].tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('Plate Z')
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Plate Z by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下の部分はサンプルです。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_plate_z_by_date_boxplot(dfs, all_pitch_types)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_plate_z_by_date_scatter(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['plate_z', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                ax.scatter(x_values, grouped['plate_z'], label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('Plate Z')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Plate Z by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_plate_z_by_date_scatter(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_plate_z_by_date_scatter(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        all_values = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['plate_z', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                ax.scatter(x_values, grouped['plate_z'], label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))
                all_values.extend(grouped['plate_z'].tolist())

        if all_values:
            avg = np.mean(all_values)
            std_dev = np.std(all_values)
            ax.axhline(avg, color='r', linestyle='--', label='Average')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ')
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('Plate Z')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Plate Z by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_plate_z_by_date_scatter(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_plate_x_by_date_boxplot(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = []
        labels = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['plate_x'])

            if not grouped.empty:
                data_to_plot.append(grouped['plate_x'])
                short_date = datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d")
                labels.append(short_date)

        if data_to_plot:
            bp = ax.boxplot(data_to_plot, labels=labels)
            for j, d in enumerate(data_to_plot):
                mean_val = d.mean()
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Date')
        ax.set_ylabel('Plate X')

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Plate X by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_plate_x_by_date_boxplot(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_plate_x_by_date_boxplot(dfs, pitch_types):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()  # DataFrameのコピーを作成
            df['month'] = pd.to_datetime(df['game_date']).dt.to_period('M')  # 月に変換
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['plate_x']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend(group['plate_x'].tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('Plate X')
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Plate X by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下の部分はサンプルです。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_plate_x_by_date_boxplot(dfs, all_pitch_types)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_plate_x_by_date_scatter(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['plate_x', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                ax.scatter(x_values, grouped['plate_x'], label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('Plate X')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Plate X by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_plate_x_by_date_scatter(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_plate_x_by_date_scatter(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        all_values = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['plate_x', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                ax.scatter(x_values, grouped['plate_x'], label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))
                all_values.extend(grouped['plate_x'].tolist())

        if all_values:
            avg = np.mean(all_values)
            std_dev = np.std(all_values)
            ax.axhline(avg, color='r', linestyle='--', label='Average')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ')  # 2σを追加
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ')  # 2σを追加

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('Plate X')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Plate X by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_plate_x_by_date_scatter(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_plate_x_by_date_boxplot(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = []
        labels = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_x'])

            if not grouped.empty:
                data_to_plot.append(grouped['release_pos_x'])
                short_date = datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d")
                labels.append(short_date)

        if data_to_plot:
            bp = ax.boxplot(data_to_plot, labels=labels)
            for j, d in enumerate(data_to_plot):
                mean_val = d.mean()
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Date')
        ax.set_ylabel('release_pos_x')

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('release_pos_x by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_plate_x_by_date_boxplot(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_release_pos_x_by_date_boxplot(dfs, pitch_types):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()  # DataFrameのコピーを作成
            df['month'] = pd.to_datetime(df['game_date']).dt.to_period('M')  # 月に変換
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_x']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend(group['release_pos_x'].tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('Release Pos X')
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Release Pos X by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下の部分はサンプルです。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_release_pos_x_by_date_boxplot(dfs, all_pitch_types)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_release_pos_x_by_date_scatter(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        all_values = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_x', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                ax.scatter(x_values, grouped['release_pos_x'], label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))
                all_values.extend(grouped['release_pos_x'].tolist())

        if all_values:
            avg = np.mean(all_values)
            std_dev = np.std(all_values)
            ax.axhline(avg, color='r', linestyle='--', label='Average')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ')  # 2σを追加
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ')  # 2σを追加

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('Release Pos X')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Release Pos X by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_release_pos_x_by_date_scatter(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_plate_x_by_date_boxplot(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = []
        labels = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_z'])

            if not grouped.empty:
                data_to_plot.append(grouped['release_pos_z'])
                short_date = datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d")
                labels.append(short_date)

        if data_to_plot:
            bp = ax.boxplot(data_to_plot, labels=labels)
            for j, d in enumerate(data_to_plot):
                mean_val = d.mean()
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Date')
        ax.set_ylabel('release_pos_z')

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('release_pos_x by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_plate_x_by_date_boxplot(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_release_pos_z_by_date_boxplot(dfs, pitch_types):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()  # DataFrameのコピーを作成
            df['month'] = pd.to_datetime(df['game_date']).dt.to_period('M')  # 月に変換
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_z']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend(group['release_pos_z'].tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('Release Pos Z')
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Release Pos Z by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下の部分はサンプルです。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_release_pos_z_by_date_boxplot(dfs, all_pitch_types)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_release_pos_z_by_date_scatter(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        all_values = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_z', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                ax.scatter(x_values, grouped['release_pos_z'], label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))
                all_values.extend(grouped['release_pos_z'].tolist())

        if all_values:
            avg = np.mean(all_values)
            std_dev = np.std(all_values)
            ax.axhline(avg, color='r', linestyle='--', label='Average')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ')  # 2σを追加
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ')  # 2σを追加

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('Release Pos Z')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Release Pos Z by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_release_pos_z_by_date_scatter(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_release_pos_y_by_date_boxplot(dfs, pitch_types):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()  # DataFrameのコピーを作成
            df['month'] = pd.to_datetime(df['game_date']).dt.to_period('M')  # 月に変換
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_y']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend(group['release_pos_y'].tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('Release Pos Y')
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Release Pos Y by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下の部分はサンプルです。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_release_pos_y_by_date_boxplot(dfs, all_pitch_types)


def plot_release_pos_y_by_pitch_count(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        values_until_627 = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_y', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                y_values = grouped['release_pos_y']
                ax.scatter(x_values, y_values, label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))

                if datetime.strptime(dates[j], "%Y-%m-%d") <= datetime.strptime("2023-06-27", "%Y-%m-%d"):
                    values_until_627.extend(y_values.tolist())

        if values_until_627:
            avg = np.mean(values_until_627)
            std_dev = np.std(values_until_627)
            ax.axhline(avg, color='r', linestyle='--', label='Average (until 6/27)')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ (until 6/27)')
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ (until 6/27)')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('release_pos_y')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('release_pos_y by Pitch Count and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下は例で、datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_release_pos_y_by_pitch_count(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_effective_speed_by_date_boxplot(dfs, pitch_types):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()
            df['month'] = pd.to_datetime(df['game_date']).dt.to_period('M')
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['effective_speed']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend(group['effective_speed'].tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('Effective Speed')
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Effective Speed by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# サンプルデータ部分。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_effective_speed_by_date_boxplot(dfs, all_pitch_types)


def plot_effective_speed_by_pitch_count(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        values_until_627 = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['effective_speed', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                y_values = grouped['effective_speed']
                ax.scatter(x_values, y_values, label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))

                if datetime.strptime(dates[j], "%Y-%m-%d") <= datetime.strptime("2023-06-27", "%Y-%m-%d"):
                    values_until_627.extend(y_values.tolist())

        if values_until_627:
            avg = np.mean(values_until_627)
            std_dev = np.std(values_until_627)
            ax.axhline(avg, color='r', linestyle='--', label='Average (until 6/27)')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ (until 6/27)')
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ (until 6/27)')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('Effective Speed')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Effective Speed by Pitch Count and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下は例で、datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_effective_speed_by_pitch_count(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_pfx_x_by_date_boxplot(dfs, pitch_types):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()
            df['month'] = pd.to_datetime(df['game_date']).dt.to_period('M')
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['pfx_x']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend(group['pfx_x'].tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('Pfx X')
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Pfx X by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# サンプルデータ部分。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_pfx_x_by_date_boxplot(dfs, all_pitch_types)


def plot_pfx_x_by_pitch_count(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        values_until_627 = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['pfx_x', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                y_values = grouped['pfx_x']
                ax.scatter(x_values, y_values, label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))

                if datetime.strptime(dates[j], "%Y-%m-%d") <= datetime.strptime("2023-06-27", "%Y-%m-%d"):
                    values_until_627.extend(y_values.tolist())

        if values_until_627:
            avg = np.mean(values_until_627)
            std_dev = np.std(values_until_627)
            ax.axhline(avg, color='r', linestyle='--', label='Average (until 6/27)')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ (until 6/27)')
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ (until 6/27)')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('pfx_x')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('pfx_x by Pitch Count and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下は例で、datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_pfx_x_by_pitch_count(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_pfx_z_by_date_boxplot(dfs, pitch_types):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()
            df['month'] = pd.to_datetime(df['game_date']).dt.to_period('M')
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['pfx_z']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend(group['pfx_z'].tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('Pfx Z')
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Pfx Z by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# サンプルデータ部分。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_pfx_z_by_date_boxplot(dfs, all_pitch_types)


def plot_pfx_z_by_pitch_count(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        values_until_627 = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['pfx_z', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                y_values = grouped['pfx_z']
                ax.scatter(x_values, y_values, label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))

                if datetime.strptime(dates[j], "%Y-%m-%d") <= datetime.strptime("2023-06-27", "%Y-%m-%d"):
                    values_until_627.extend(y_values.tolist())

        if values_until_627:
            avg = np.mean(values_until_627)
            std_dev = np.std(values_until_627)
            ax.axhline(avg, color='r', linestyle='--', label='Average (until 6/27)')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ (until 6/27)')
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ (until 6/27)')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('pfx_z')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('pfx_z by Pitch Count and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下は例で、datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_pfx_z_by_pitch_count(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_vx0_by_date_boxplot(dfs, pitch_types):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()
            df['month'] = pd.to_datetime(df['game_date']).dt.to_period('M')
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['vx0']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend(group['vx0'].tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('Vx0')
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Vx0 by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# サンプルデータ部分。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_vx0_by_date_boxplot(dfs, all_pitch_types)


def plot_vx0_by_pitch_count(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        values_until_627 = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['vx0', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                y_values = grouped['vx0']
                ax.scatter(x_values, y_values, label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))

                if datetime.strptime(dates[j], "%Y-%m-%d") <= datetime.strptime("2023-06-27", "%Y-%m-%d"):
                    values_until_627.extend(y_values.tolist())

        if values_until_627:
            avg = np.mean(values_until_627)
            std_dev = np.std(values_until_627)
            ax.axhline(avg, color='r', linestyle='--', label='Average (until 6/27)')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ (until 6/27)')
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ (until 6/27)')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('vx0')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('vx0 by Pitch Count and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下は例で、datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_vx0_by_pitch_count(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_vy0_by_date_boxplot(dfs, pitch_types):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()
            df['month'] = pd.to_datetime(df['game_date']).dt.to_period('M')
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['vy0']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend(group['vy0'].tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('Vy0')
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Vy0 by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# サンプルデータ部分。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_vy0_by_date_boxplot(dfs, all_pitch_types)


def plot_vy0_by_pitch_count(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        values_until_627 = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['vy0', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                y_values = grouped['vy0']
                ax.scatter(x_values, y_values, label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))

                if datetime.strptime(dates[j], "%Y-%m-%d") <= datetime.strptime("2023-06-27", "%Y-%m-%d"):
                    values_until_627.extend(y_values.tolist())

        if values_until_627:
            avg = np.mean(values_until_627)
            std_dev = np.std(values_until_627)
            ax.axhline(avg, color='r', linestyle='--', label='Average (until 6/27)')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ (until 6/27)')
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ (until 6/27)')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('vy0')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('vy0 by Pitch Count and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下は例で、datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_vy0_by_pitch_count(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_vz0_by_date_boxplot(dfs, pitch_types):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()
            df['month'] = pd.to_datetime(df['game_date']).dt.to_period('M')
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['vz0']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend(group['vz0'].tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('Vz0')
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Vz0 by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# サンプルデータ部分。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_vz0_by_date_boxplot(dfs, all_pitch_types)


def plot_vz0_by_pitch_count(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        values_until_627 = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['vz0', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                y_values = grouped['vz0']
                ax.scatter(x_values, y_values, label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))

                if datetime.strptime(dates[j], "%Y-%m-%d") <= datetime.strptime("2023-06-27", "%Y-%m-%d"):
                    values_until_627.extend(y_values.tolist())

        if values_until_627:
            avg = np.mean(values_until_627)
            std_dev = np.std(values_until_627)
            ax.axhline(avg, color='r', linestyle='--', label='Average (until 6/27)')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ (until 6/27)')
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ (until 6/27)')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('vz0')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('vz0 by Pitch Count and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下は例で、datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_vz0_by_pitch_count(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_ax_by_date_boxplot(dfs, pitch_types):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()
            df['month'] = pd.to_datetime(df['game_date']).dt.to_period('M')
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['ax']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend(group['ax'].tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('Ax')
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Ax by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# サンプルデータ部分。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_ax_by_date_boxplot(dfs, all_pitch_types)


def plot_ax_by_pitch_count(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        values_until_627 = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['ax', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                y_values = grouped['ax']
                ax.scatter(x_values, y_values, label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))

                if datetime.strptime(dates[j], "%Y-%m-%d") <= datetime.strptime("2023-06-27", "%Y-%m-%d"):
                    values_until_627.extend(y_values.tolist())

        if values_until_627:
            avg = np.mean(values_until_627)
            std_dev = np.std(values_until_627)
            ax.axhline(avg, color='r', linestyle='--', label='Average (until 6/27)')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ (until 6/27)')
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ (until 6/27)')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('ax')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('ax by Pitch Count and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下は例で、datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_ax_by_pitch_count(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_ay_by_date_boxplot(dfs, pitch_types):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()
            df['month'] = pd.to_datetime(df['game_date']).dt.to_period('M')
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['ay']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend(group['ay'].tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('Ay')
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Ay by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# サンプルデータ部分。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_ay_by_date_boxplot(dfs, all_pitch_types)


def plot_ay_by_pitch_count(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        values_until_627 = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['ay', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                y_values = grouped['ay']
                ax.scatter(x_values, y_values, label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))

                if datetime.strptime(dates[j], "%Y-%m-%d") <= datetime.strptime("2023-06-27", "%Y-%m-%d"):
                    values_until_627.extend(y_values.tolist())

        if values_until_627:
            avg = np.mean(values_until_627)
            std_dev = np.std(values_until_627)
            ax.axhline(avg, color='r', linestyle='--', label='Average (until 6/27)')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ (until 6/27)')
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ (until 6/27)')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('ay')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('ay by Pitch Count and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下は例で、datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_ay_by_pitch_count(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_az_by_date_boxplot(dfs, pitch_types):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()
            df['month'] = pd.to_datetime(df['game_date']).dt.to_period('M')
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['az']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend(group['az'].tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('Az')
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Az by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# サンプルデータ部分。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_az_by_date_boxplot(dfs, all_pitch_types)


def plot_az_by_pitch_count(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        values_until_627 = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['az', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                y_values = grouped['az']
                ax.scatter(x_values, y_values, label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))

                if datetime.strptime(dates[j], "%Y-%m-%d") <= datetime.strptime("2023-06-27", "%Y-%m-%d"):
                    values_until_627.extend(y_values.tolist())

        if values_until_627:
            avg = np.mean(values_until_627)
            std_dev = np.std(values_until_627)
            ax.axhline(avg, color='r', linestyle='--', label='Average (until 6/27)')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ (until 6/27)')
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ (until 6/27)')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('az')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('az by Pitch Count and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下は例で、datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_az_by_pitch_count(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_speed_difference_by_date_boxplot(dfs, pitch_types):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()
            df['month'] = pd.to_datetime(df['game_date']).dt.to_period('M')
            df['speed_diff'] = df['release_speed'] - df['effective_speed']
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['speed_diff']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend(group['speed_diff'].tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('Speed Difference (Release - Effective)')
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Speed Difference by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# サンプルデータ部分。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_speed_difference_by_date_boxplot(dfs, all_pitch_types)


def plot_speed_difference_by_pitch_count(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        values_until_627 = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_speed', 'effective_speed', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                speed_diff = grouped['release_speed'] - grouped['effective_speed']
                ax.scatter(x_values, speed_diff, label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))

                if datetime.strptime(dates[j], "%Y-%m-%d") <= datetime.strptime("2023-06-27", "%Y-%m-%d"):
                    values_until_627.extend(speed_diff.tolist())

        if values_until_627:
            avg = np.mean(values_until_627)
            std_dev = np.std(values_until_627)
            ax.axhline(avg, color='r', linestyle='--', label='Average (until 6/27)')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ (until 6/27)')
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ (until 6/27)')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('Release Speed - Effective Speed')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Release Speed - Effective Speed by Pitch Count and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下は例で、datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_speed_difference_by_pitch_count(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_release_pos_z_times_plate_x_by_pitch_count(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        all_values = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_x', 'plate_x', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                ax.scatter(x_values, grouped['release_pos_x'] * grouped['plate_x'], label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))
                all_values.extend((grouped['release_pos_x'] * grouped['plate_x']).tolist())

        if all_values:
            avg = np.mean(all_values)
            std_dev = np.std(all_values)
            ax.axhline(avg, color='r', linestyle='--', label='Average')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ')  # 2σを追加
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ')  # 2σを追加

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('Release Pos x × Plate X')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Release Pos x × Plate X by Pitch Count and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_release_pos_z_times_plate_x_by_pitch_count(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_release_pos_z_times_plate_z_by_pitch_count(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        all_values = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_z', 'plate_z', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                ax.scatter(x_values, grouped['release_pos_z'] * grouped['plate_z'], label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))
                all_values.extend((grouped['release_pos_z'] * grouped['plate_z']).tolist())

        if all_values:
            avg = np.mean(all_values)
            std_dev = np.std(all_values)
            ax.axhline(avg, color='r', linestyle='--', label='Average')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ')  # 2σを追加
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ')  # 2σを追加

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('Release Pos Z × Plate Z')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Release Pos Z × Plate Z by Pitch Count and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_release_pos_z_times_plate_z_by_pitch_count(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_release_pos_x_times_z_by_pitch_count(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        all_values = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_x', 'release_pos_z', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                ax.scatter(x_values, grouped['release_pos_x'] * grouped['release_pos_z'], label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))
                all_values.extend((grouped['release_pos_x'] * grouped['release_pos_z']).tolist())

        if all_values:
            avg = np.mean(all_values)
            std_dev = np.std(all_values)
            ax.axhline(avg, color='r', linestyle='--', label='Average')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ')  # 2σを追加
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ')  # 2σを追加

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('Release Pos X × Release Pos Z')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Release Pos X × Release Pos Z by Pitch Count and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_release_pos_x_times_z_by_pitch_count(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np
import math

def plot_sqrt_release_pos_x2_plus_z2_by_pitch_count(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        all_values = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_x', 'release_pos_z', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                sqrt_values = np.sqrt(grouped['release_pos_x']**2 + grouped['release_pos_z']**2)
                ax.scatter(x_values, sqrt_values, label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))
                all_values.extend(sqrt_values.tolist())

        if all_values:
            avg = np.mean(all_values)
            std_dev = np.std(all_values)
            ax.axhline(avg, color='r', linestyle='--', label='Average')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ')  # 2σを追加
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ')  # 2σを追加

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('√(release_pos_x^2 + release_pos_z^2)')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('√(release_pos_x^2 + release_pos_z^2) by Pitch Count and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_sqrt_release_pos_x2_plus_z2_by_pitch_count(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_sqrt_release_pos_x2_plus_z2_by_pitch_count(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        all_values = []
        values_until_627 = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_x', 'release_pos_z', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                sqrt_values = np.sqrt(grouped['release_pos_x']**2 + grouped['release_pos_z']**2)
                ax.scatter(x_values, sqrt_values, label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))
                all_values.extend(sqrt_values.tolist())

                if datetime.strptime(dates[j], "%Y-%m-%d") <= datetime.strptime("2023-06-27", "%Y-%m-%d"):
                    values_until_627.extend(sqrt_values.tolist())

        if values_until_627:
            avg = np.mean(values_until_627)
            std_dev = np.std(values_until_627)
            ax.axhline(avg, color='r', linestyle='--', label='Average (until 6/27)')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ (until 6/27)')  # 2σを追加
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ (until 6/27)')  # 2σを追加

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('√(release_pos_x^2 + release_pos_z^2)')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('√(release_pos_x^2 + release_pos_z^2) by Pitch Count and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_sqrt_release_pos_x2_plus_z2_by_pitch_count(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_product_sqrt_spin_rate_by_pitch_count(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        all_values = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_x', 'release_pos_z', 'release_spin_rate', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                product_values = np.sqrt(grouped['release_pos_x']**2 + grouped['release_pos_z']**2) * grouped['release_spin_rate']
                ax.scatter(x_values, product_values, label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))
                all_values.extend(product_values.tolist())

        if all_values:
            avg = np.mean(all_values)
            std_dev = np.std(all_values)
            ax.axhline(avg, color='r', linestyle='--', label='Average')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ')  # 2σを追加
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ')  # 2σを追加

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('√(release_pos_x^2 + release_pos_z^2) × release_spin_rate')
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Product of √(release_pos_x^2 + release_pos_z^2) and Release Spin Rate by Pitch Count and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_product_sqrt_spin_rate_by_pitch_count(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_product_sqrt_spin_rate_by_pitch_count(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        all_values = []
        values_until_627 = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_x', 'release_pos_z', 'release_spin_rate', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                product_values = np.sqrt(grouped['release_pos_x']**2 + grouped['release_pos_z']**2) * grouped['release_spin_rate']
                ax.scatter(x_values, product_values, label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))
                all_values.extend(product_values.tolist())

                if datetime.strptime(dates[j], "%Y-%m-%d") <= datetime.strptime("2023-06-27", "%Y-%m-%d"):
                    values_until_627.extend(product_values.tolist())

        if values_until_627:
            avg = np.mean(values_until_627)
            std_dev = np.std(values_until_627)
            ax.axhline(avg, color='r', linestyle='--', label='Average (until 6/27)')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ (until 6/27)')  # 2σを追加
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ (until 6/27)')  # 2σを追加

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('√(release_pos_x^2 + release_pos_z^2)\n× release_spin_rate')

        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Product of √(release_pos_x^2 + release_pos_z^2) and Release Spin Rate by Pitch Count and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_product_sqrt_spin_rate_by_pitch_count(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_product_sqrt_spin_rate_by_pitch_count(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0
        all_values = []
        values_until_627 = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_x', 'release_pos_z', 'release_spin_rate', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                product_values = np.sqrt(grouped['release_pos_x']**2 + grouped['release_pos_z']**2) * grouped['release_spin_rate']
                ax.scatter(x_values, product_values, label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))
                all_values.extend(product_values.tolist())

                if datetime.strptime(dates[j], "%Y-%m-%d") <= datetime.strptime("2023-06-27", "%Y-%m-%d"):
                    values_until_627.extend(product_values.tolist())

        if pitch_type == 'ST':
            ax.set_ylim(bottom=12000)

        if values_until_627:
            avg = np.mean(values_until_627)
            std_dev = np.std(values_until_627)
            ax.axhline(avg, color='r', linestyle='--', label='Average (until 6/27)')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ (until 6/27)')
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ (until 6/27)')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('√(release_pos_x^2 + release_pos_z^2)\n× release_spin_rate')

        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Product of √(release_pos_x^2 + release_pos_z^2) and Release Spin Rate by Pitch Count and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_product_sqrt_spin_rate_by_pitch_count(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

def plot_sqrt_pos_xz_by_date_boxplot(dfs, pitch_types):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()  # DataFrameのコピーを作成
            df['month'] = pd.to_datetime(df['game_date']).dt.to_period('M')  # 月に変換
            df['sqrt_pos_xz'] = np.sqrt(df['release_pos_x']**2 + df['release_pos_z']**2)  # √(release_pos_x^2 + release_pos_z^2)
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['sqrt_pos_xz']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend(group['sqrt_pos_xz'].tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('√(release_pos_x^2 + release_pos_z^2)')
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('√(release_pos_x^2 + release_pos_z^2) by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下の部分はサンプルです。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_sqrt_pos_xz_by_date_boxplot(dfs, all_pitch_types)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_distance_by_date_boxplot(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = []
        labels = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_x', 'release_pos_z'])
            grouped['distance'] = np.sqrt(grouped['release_pos_x']**2 + grouped['release_pos_z']**2)

            if not grouped.empty:
                data_to_plot.append(grouped['distance'])
                short_date = datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d")
                labels.append(short_date)

        if data_to_plot:
            bp = ax.boxplot(data_to_plot, labels=labels)
            for j, d in enumerate(data_to_plot):
                mean_val = d.mean()
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Date')
        ax.set_ylabel('Distance (ft)')

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Distance by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_distance_by_date_boxplot(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

def plot_sqrt_pos_xz_spin_rate_by_date_boxplot(dfs, pitch_types):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()  # DataFrameのコピーを作成
            df['month'] = pd.to_datetime(df['game_date']).dt.to_period('M')  # 月に変換
            df['sqrt_pos_xz_spin_rate'] = np.sqrt(df['release_pos_x']**2 + df['release_pos_z']**2) * df['release_spin_rate']
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['sqrt_pos_xz_spin_rate']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend(group['sqrt_pos_xz_spin_rate'].tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('√(release_pos_x^2 + release_pos_z^2) × release_spin_rate')
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('√(release_pos_x^2 + release_pos_z^2) × release_spin_rate by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下の部分はサンプルです。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_sqrt_pos_xz_spin_rate_by_date_boxplot(dfs, all_pitch_types)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_distance_spin_rate_by_date_boxplot(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = []
        labels = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_x', 'release_pos_z', 'release_spin_rate'])
            grouped['distance'] = np.sqrt(grouped['release_pos_x']**2 + grouped['release_pos_z']**2)
            grouped['distance_spin_rate'] = grouped['distance'] * grouped['release_spin_rate']

            if not grouped.empty:
                data_to_plot.append(grouped['distance_spin_rate'])
                short_date = datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d")
                labels.append(short_date)

        if data_to_plot:
            bp = ax.boxplot(data_to_plot, labels=labels)
            for j, d in enumerate(data_to_plot):
                mean_val = d.mean()
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Date')
        ax.set_ylabel('Distance * Spin Rate')

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Distance * Spin Rate by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_distance_spin_rate_by_date_boxplot(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_distance_spin_rate_by_date_boxplot(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = []
        labels = []
        avg_until_627 = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_x', 'release_pos_z', 'release_spin_rate'])
            grouped['distance'] = np.sqrt(grouped['release_pos_x']**2 + grouped['release_pos_z']**2)
            grouped['distance_spin_rate'] = grouped['distance'] * grouped['release_spin_rate']

            if not grouped.empty:
                data_to_plot.append(grouped['distance_spin_rate'])
                short_date = datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d")
                labels.append(short_date)

                if short_date <= '06/27':
                    avg_until_627.append(grouped['distance_spin_rate'].mean())

        if data_to_plot:
            bp = ax.boxplot(data_to_plot, labels=labels)
            for j, d in enumerate(data_to_plot):
                mean_val = d.mean()
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

            if avg_until_627:
                avg_line_value = np.mean(avg_until_627)
                ax.axhline(y=avg_line_value, color='r', linestyle='--', label=f"Avg until 06/27: {avg_line_value:.1f}")
                ax.legend()

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Date')
        ax.set_ylabel('Distance * Spin Rate')

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Distance * Spin Rate by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_distance_spin_rate_by_date_boxplot(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_distance_spin_rate_by_date_boxplot(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = []
        labels = []
        avg_until_627 = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_x', 'release_pos_z', 'release_spin_rate'])
            grouped['distance'] = np.sqrt(grouped['release_pos_x']**2 + grouped['release_pos_z']**2)
            grouped['distance_spin_rate'] = grouped['distance'] * grouped['release_spin_rate']

            if not grouped.empty:
                data_to_plot.append(grouped['distance_spin_rate'])
                short_date = datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d")
                labels.append(short_date)

                if short_date <= '06/27':
                    avg_until_627.append(grouped['distance_spin_rate'].mean())

        if data_to_plot:
            bp = ax.boxplot(data_to_plot, labels=labels)
            for j, d in enumerate(data_to_plot):
                mean_val = d.mean()
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

            if avg_until_627:
                avg_line_value = np.mean(avg_until_627)
                ax.axhline(y=avg_line_value, color='r', linestyle='--', label=f"Avg until 06/27: {avg_line_value:.1f}")
                ax.legend()

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Date')
        ax.set_ylabel('Distance * Spin Rate')

        if pitch_type == 'ST':
            ax.set_ylim(bottom=11000)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Distance * Spin Rate by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_distance_spin_rate_by_date_boxplot(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_product_sqrt_release_and_plate_by_pitch_count(dfs, pitch_types, dates):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]  # nan を除外
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        total_pitch_count = 0  # 積算されるトータルの球数
        all_values = []
        values_until_627 = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_x', 'release_pos_z', 'plate_x', 'plate_z', 'pitch_number'])

            if not grouped.empty:
                x_values = [total_pitch_count + k for k in range(1, len(grouped) + 1)]
                total_pitch_count += len(grouped)
                product_values = np.sqrt(grouped['release_pos_x']**2 + grouped['release_pos_z']**2) * np.sqrt(grouped['plate_x']**2 + grouped['plate_z']**2)
                ax.scatter(x_values, product_values, label=datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d"))
                all_values.extend(product_values.tolist())

                if datetime.strptime(dates[j], "%Y-%m-%d") <= datetime.strptime("2023-06-27", "%Y-%m-%d"):
                    values_until_627.extend(product_values.tolist())

        if values_until_627:
            avg = np.mean(values_until_627)
            std_dev = np.std(values_until_627)
            ax.axhline(avg, color='r', linestyle='--', label='Average (until 6/27)')
            ax.axhline(avg + 2 * std_dev, color='g', linestyle='--', label='Average + 2σ (until 6/27)')  # 2σを追加
            ax.axhline(avg - 2 * std_dev, color='g', linestyle='--', label='Average - 2σ (until 6/27)')  # 2σを追加

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Total Pitch Count')
        ax.set_ylabel('√(release_pos_x^2 + release_pos_z^2)\n× √(plate_x^2 + plate_z^2)')  # 2行に分ける
        ax.legend(title='Date', loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(dates) // 2)

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Product of √(release_pos_x^2 + release_pos_z^2) and √(plate_x^2 + plate_z^2) by Pitch Count and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 例: datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_product_sqrt_release_and_plate_by_pitch_count(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

def plot_sqrt_pos_plate_by_date_boxplot(dfs, pitch_types):
    pitch_types = [pt for pt in pitch_types if pt is not None and pd.notna(pt)]
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(10, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]

        data_to_plot = {}
        labels = []

        for j, df in enumerate(dfs):
            df = df.copy()  # DataFrameのコピーを作成
            df['month'] = pd.to_datetime(df['game_date']).dt.to_period('M')  # 月に変換
            df['sqrt_pos_plate'] = np.sqrt(df['release_pos_x']**2 + df['release_pos_z']**2) * np.sqrt(df['plate_x']**2 + df['plate_z']**2)
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['sqrt_pos_plate']).groupby('month')

            for month, group in grouped:
                if month.strftime('%Y-%m') not in data_to_plot:
                    data_to_plot[month.strftime('%Y-%m')] = []
                data_to_plot[month.strftime('%Y-%m')].extend(group['sqrt_pos_plate'].tolist())

        sorted_months = sorted(data_to_plot.keys())
        sorted_data = [data_to_plot[month] for month in sorted_months]

        if sorted_data:
            bp = ax.boxplot(sorted_data, labels=sorted_months)
            for j, d in enumerate(sorted_data):
                mean_val = sum(d) / len(d)
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Month')
        ax.set_ylabel('√(release_pos_x^2 + release_pos_z^2)\n× √(plate_x^2 + plate_z^2)')  # 2行に分ける
        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('√(release_pos_x^2 + release_pos_z^2) × √(plate_x^2 + plate_z^2) by Month and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# 以下の部分はサンプルです。実際のデータに合わせてください。
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_sqrt_pos_plate_by_date_boxplot(dfs, all_pitch_types)


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_distance_spin_rate_by_date_boxplot(dfs, pitch_types, dates):
    fig, axs = plt.subplots(len(pitch_types), 1, figsize=(20, len(pitch_types) * 4))

    for i, pitch_type in enumerate(pitch_types):
        ax = axs[i]
        data_to_plot = []
        labels = []
        avg_until_627 = []

        for j, df in enumerate(dfs):
            grouped = df[df['pitch_type'] == pitch_type].dropna(subset=['release_pos_x', 'release_pos_z', 'plate_x', 'plate_z', 'release_spin_rate'])

            grouped['distance'] = np.sqrt(grouped['release_pos_x']**2 + grouped['release_pos_z']**2)
            grouped['distance_plate'] = np.sqrt(grouped['plate_x']**2 + grouped['plate_z']**2)
            grouped['distance_spin_rate_plate'] = grouped['distance'] * grouped['distance_plate']

            if not grouped.empty:
                data_to_plot.append(grouped['distance_spin_rate_plate'])
                short_date = datetime.strptime(dates[j], "%Y-%m-%d").strftime("%m/%d")
                labels.append(short_date)

                if short_date <= '06/27':
                    avg_until_627.append(grouped['distance_spin_rate_plate'].mean())

        if data_to_plot:
            bp = ax.boxplot(data_to_plot, labels=labels)
            for j, d in enumerate(data_to_plot):
                mean_val = d.mean()
                ax.text(j + 1, mean_val, f"{mean_val:.1f}", ha='center', va='bottom', fontsize=10, color='blue')

            if avg_until_627:
                avg_line_value = np.mean(avg_until_627)
                ax.axhline(y=avg_line_value, color='r', linestyle='--', label=f"Avg until 06/27: {avg_line_value:.1f}")
                ax.legend()

        ax.set_title(f"Pitch Type: {pitch_type}")
        ax.set_xlabel('Date')
        ax.set_ylabel('√(release_pos_x^2 + release_pos_z^2)\n× √(plate_x^2 + plate_z^2)')  # 2行に分ける

        ax.grid(which='both', linestyle='--', color='gray', alpha=0.5)

    fig.suptitle('Distance * Distance (Plate) by Date and Pitch Type', fontsize=16, y=1.02)
    plt.tight_layout(pad=3)
    plt.show()

# datesとdf_660271_all_datesはすでに定義されていると仮定
dfs = [df_660271_all_dates[df_660271_all_dates['game_date'] == date] for date in dates]
all_pitch_types = set()
for df in dfs:
    all_pitch_types |= set(df['pitch_type'].unique())

plot_distance_spin_rate_by_date_boxplot(dfs, all_pitch_types, dates)


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Create a list of unique dates
unique_dates = sorted(df_660271_all_dates['game_date'].unique())

# Create a color map, viridis color map except the latest one.
colors = plt.cm.viridis(np.linspace(0, 1, len(unique_dates) - 1))

plt.figure(figsize=(12, 6))

for i, date in enumerate(unique_dates):
    df_date = df_660271_all_dates[df_660271_all_dates['game_date'] == date]
    df_ff = df_date[df_date['pitch_type'] == 'FF'].dropna(subset=['release_speed', 'release_spin_rate'])
    # Make the latest date's color red.
    color = 'red' if i == len(unique_dates) - 1 else colors[i]
    plt.scatter(df_ff['release_speed'], df_ff['release_spin_rate'], color=color, label=pd.to_datetime(date).strftime('%Y-%m-%d'), alpha=0.5)

plt.xlabel('release_speed')
plt.ylabel('release_spin_rate')
plt.title('FF Pitch release_speed vs release_spin_rate')
plt.legend(title='Game Date', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(which='both', linestyle='--', color='gray', alpha=0.5)

# Set the y-axis range
# plt.ylim(200, None)

plt.show()


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_boxplot_by_pitch_type(dfs, pitch_types):
    concatenated_df = pd.concat(dfs, ignore_index=True)
    concatenated_df['spin_rate_bin'] = (concatenated_df['release_spin_rate'] // 50) * 50

    for pitch_type in pitch_types:
        # プロットの設定（2つのサブプロット）
        fig, axes = plt.subplots(1, 2, figsize=(24, 8))

        # リリースポジションXのボックスプロット
        subset_df_x = concatenated_df[(concatenated_df['pitch_type'] == pitch_type) & (concatenated_df['spin_rate_bin'].notna())]
        sns.boxplot(x='spin_rate_bin', y='release_pos_x', data=subset_df_x, ax=axes[0])
        axes[0].set_title(f"Boxplot of Release Position X by Spin Rate for {pitch_type}")
        axes[0].set_xlabel("Spin Rate Bin")
        axes[0].set_ylabel("Release Position X")
        axes[0].grid(True, linestyle='--')  # 点線のグリッド追加

        # リリースポジションZのボックスプロット
        subset_df_z = concatenated_df[(concatenated_df['pitch_type'] == pitch_type) & (concatenated_df['spin_rate_bin'].notna())]
        sns.boxplot(x='spin_rate_bin', y='release_pos_z', data=subset_df_z, ax=axes[1])
        axes[1].set_title(f"Boxplot of Release Position Z by Spin Rate for {pitch_type}")
        axes[1].set_xlabel("Spin Rate Bin")
        axes[1].set_ylabel("Release Position Z")
        axes[1].grid(True, linestyle='--')  # 点線のグリッド追加

        plt.tight_layout()
        plt.show()

# 例: dfsとall_pitch_typesはすでに定義されていると仮定
plot_boxplot_by_pitch_type(dfs, all_pitch_types)


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_boxplot_by_pitch_type(dfs, pitch_types):
    concatenated_df = pd.concat(dfs, ignore_index=True)
    concatenated_df['spin_rate_bin'] = (concatenated_df['release_spin_rate'] // 50) * 50  # 50単位でビン化
    concatenated_df['root_pos_xz'] = (concatenated_df['release_pos_x']**2 + concatenated_df['release_pos_z']**2)**0.5  # 指定の数式に基づいて新しい列を作成

    for pitch_type in pitch_types:
        plt.figure(figsize=(12, 8))
        subset_df = concatenated_df[(concatenated_df['pitch_type'] == pitch_type) & (concatenated_df['spin_rate_bin'].notna())]

        sns.boxplot(x='spin_rate_bin', y='root_pos_xz', data=subset_df)
        plt.title(f"Boxplot of √(release_pos_x² + release_pos_z²) by Spin Rate for {pitch_type}")
        plt.xlabel("Spin Rate Bin")
        plt.ylabel("√(release_pos_x² + release_pos_z²)")
        plt.grid(True, linestyle='--')  # 点線のグリッド追加
        plt.show()

# 例: dfsとall_pitch_typesはすでに定義されていると仮定
plot_boxplot_by_pitch_type(dfs, all_pitch_types)


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_boxplot_by_pitch_type_pfx(dfs, pitch_types, bin_size=10):
    concatenated_df = pd.concat(dfs, ignore_index=True)
    # pfx_xとpfx_zのビン化（小数点2桁で丸める）
    concatenated_df['pfx_x_bin'] = ((concatenated_df['pfx_x'] / bin_size).round(0) * bin_size).round(2)
    concatenated_df['pfx_z_bin'] = ((concatenated_df['pfx_z'] / bin_size).round(0) * bin_size).round(2)

    for pitch_type in pitch_types:
        # プロットの設定（2x2のサブプロット）
        fig, axes = plt.subplots(2, 2, figsize=(24, 16))

        # release_pos_x と pfx_x のボックスプロット
        sns.boxplot(x='pfx_x_bin', y='release_pos_x', data=concatenated_df[concatenated_df['pitch_type'] == pitch_type], ax=axes[0, 0])
        axes[0, 0].set_title(f"Release Position X vs PFX_X for {pitch_type}")
        axes[0, 0].set_xlabel("PFX_X Bin")
        axes[0, 0].set_ylabel("Release Position X")
        axes[0, 0].grid(True, linestyle='--')  # 点線のグリッド追加

        # release_pos_x と pfx_z のボックスプロット
        sns.boxplot(x='pfx_z_bin', y='release_pos_x', data=concatenated_df[concatenated_df['pitch_type'] == pitch_type], ax=axes[0, 1])
        axes[0, 1].set_title(f"Release Position X vs PFX_Z for {pitch_type}")
        axes[0, 1].set_xlabel("PFX_Z Bin")
        axes[0, 1].set_ylabel("Release Position X")
        axes[0, 1].grid(True, linestyle='--')  # 点線のグリッド追加

        # release_pos_z と pfx_x のボックスプロット
        sns.boxplot(x='pfx_x_bin', y='release_pos_z', data=concatenated_df[concatenated_df['pitch_type'] == pitch_type], ax=axes[1, 0])
        axes[1, 0].set_title(f"Release Position Z vs PFX_X for {pitch_type}")
        axes[1, 0].set_xlabel("PFX_X Bin")
        axes[1, 0].set_ylabel("Release Position Z")
        axes[1, 0].grid(True, linestyle='--')  # 点線のグリッド追加

        # release_pos_z と pfx_z のボックスプロット
        sns.boxplot(x='pfx_z_bin', y='release_pos_z', data=concatenated_df[concatenated_df['pitch_type'] == pitch_type], ax=axes[1, 1])
        axes[1, 1].set_title(f"Release Position Z vs PFX_Z for {pitch_type}")
        axes[1, 1].set_xlabel("PFX_Z Bin")
        axes[1, 1].set_ylabel("Release Position Z")
        axes[1, 1].grid(True, linestyle='--')  # 点線のグリッド追加

        plt.tight_layout()
        plt.show()

# 例: dfsとall_pitch_typesはすでに定義されていると仮定
plot_boxplot_by_pitch_type_pfx(dfs, all_pitch_types, bin_size=0.1)


# CSVファイルに保存
csv_file_path = 'statcast_data_660271.csv'
df_660271_all_dates.to_csv(csv_file_path, index=False)


