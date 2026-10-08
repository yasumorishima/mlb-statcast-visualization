# MLB Data Analysis

pybaseball + pandas + matplotlib で MLB Statcast データを分析するプロジェクトです。
主要な分析には SQL版（DuckDB）も用意しています。

> 新しい分析は [mlb-statcast-visualization](https://github.com/yasumorishima/mlb-statcast-visualization) で公開しています。

## Notebooks

### 投手分析

#### 1. WBC 2023 サンドバル スカウティング
左打者にスライダー49.2%、被HR 0本 | pybaseball, seaborn
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yasumorishima/mlb-data-analysis/blob/main/notebooks/wbc_2023_sandoval_scouting.ipynb)

![Sandoval Pitch Usage by Batter Side](./docs/image/sandoval_pitch_usage.png)
![Sandoval Hit Distribution](./docs/image/sandoval_hit_distribution.png)

#### 2. バウアー セットポジション画像分析
K-meansでグラブ位置の球種別の癖を検出 | PIL, scikit-learn
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yasumorishima/mlb-data-analysis/blob/main/notebooks/bauer_set_position_analysis_2023.ipynb)


#### 5. 大谷翔平 怪我予兆分析（2023）
複数パラメーター±2σで投球異常を検出 | pybaseball, numpy
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yasumorishima/mlb-data-analysis/blob/main/notebooks/ohtani_injury_analysis_2023.ipynb)

![Ohtani Injury Analysis](./docs/image/ohtani_injury_analysis.png)

### 打者分析

#### 3. 大谷翔平 打撃分析（2022）
セカンド付近ヒット集中 →「大谷シフト」の根拠 | pybaseball, matplotlib
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yasumorishima/mlb-data-analysis/blob/main/notebooks/ohtani_batting_analysis_2022.ipynb)

![Ohtani Batting Heatmap](./docs/image/ohtani_batting_heatmap.png)

#### 6. 大谷翔平 打球速度予測（Random Forest）
コース位置が予測の46%、球速は13%のみ | scikit-learn
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yasumorishima/mlb-data-analysis/blob/main/notebooks/ohtani_exit_velocity_random_forest.ipynb)

### その他

#### 4. MLB HR Race 2024
バーチャートレースアニメーション | bar_chart_race
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yasumorishima/mlb-data-analysis/blob/main/notebooks/mlb_home_run_race_2024.ipynb)

https://github.com/user-attachments/assets/c2f5565c-ba87-419a-aaa3-fdc993034a95

## SQL版（DuckDB）

| 分析 | SQL Notebook |
|------|-------------|
| 大谷 打撃 2022 | [SQL版](./notebooks/sql/ohtani_batting_analysis_2022_sql.ipynb) |
| サンドバル スカウティング | [SQL版](./notebooks/sql/wbc_2023_sandoval_scouting_sql.ipynb) |
| HR Race 2024 | [SQL版](./notebooks/sql/mlb_home_run_race_2024_sql.ipynb) |
| 大谷 怪我予兆 2023 | [SQL版](./notebooks/sql/ohtani_injury_analysis_2023_sql.ipynb) |

## セットアップ

```bash
pip install pybaseball pandas matplotlib seaborn bar_chart_race numpy pillow scikit-learn duckdb
```
