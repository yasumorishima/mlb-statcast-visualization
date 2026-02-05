# MLB Statcast Data Visualization

pybaseball + DuckDB + Google Colabで、MLB Statcastデータを可視化・分析するプロジェクトです。

## Notebooks

### 投手分析

| # | 選手 | テーマ | Notebook | Colab | 記事 |
|---|------|--------|----------|-------|------|
| 4 | 今永昇太 | 2年目の変化（2024-2025） | `imanaga_2024_2025.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yasumorishima/mlb-statcast-visualization/blob/main/imanaga_2024_2025.ipynb) | [Zenn](https://zenn.dev/yasumorishima/articles/imanaga-2nd-year-analysis-2024-2025) |
| 3 | ダルビッシュ有 | 投球スタイル進化（2021-2025） | `darvish_evolution_2021_2025.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yasumorishima/mlb-statcast-visualization/blob/main/darvish_evolution_2021_2025.ipynb) | [Zenn](https://zenn.dev/yasumorishima/articles/darvish-pitching-evolution-2021-2025) |

### 打者分析

| # | 選手 | テーマ | Notebook | Colab | 記事 |
|---|------|--------|----------|-------|------|
| 2 | 大谷翔平 | ヒートマップ（matplotlib手動描画） | `ohtani_2_matplotlib_manual.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yasumorishima/mlb-statcast-visualization/blob/main/ohtani_2_matplotlib_manual.ipynb) | [Zenn](https://zenn.dev/yasumorishima/articles/matplotlib-baseball-heatmap) |
| 1 | 大谷翔平 | スプレーチャート（spraychart） | `ohtani_1_spraychart_pybaseball.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yasumorishima/mlb-statcast-visualization/blob/main/ohtani_1_spraychart_pybaseball.ipynb) | [Zenn](https://zenn.dev/yasumorishima/articles/pybaseball-spraychart-ohtani) |

## 分析手法

各ノートブックで共通して使用している手法：

- **pybaseball** でStatcastデータ取得
- **DuckDB** でSQLベースのデータ集計（pandas操作より可読性重視）
- **matplotlib / seaborn** で可視化
- テキスト要約セル付き（Claude Codeとの共同分析用）

## セットアップ

```python
!pip install pybaseball duckdb seaborn -q
```

## 注意: game_typeフィルタ

オープン戦のデータを除外するために、必ず`game_type = "R"`でフィルタしてください。

## 参考

- [pybaseball](https://github.com/jldbc/pybaseball)
- [Baseball Savant](https://baseballsavant.mlb.com/)
