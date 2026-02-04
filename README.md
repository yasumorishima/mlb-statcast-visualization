# MLB Statcast Data Visualization

pybaseball + DuckDB + Google Colabで、MLB Statcastデータを可視化するサンプルコードです。

## Notebooks

| # | テーマ | Notebook | Open in Colab |
|---|------|----------|---------------|
| 1 | 大谷翔平 スプレーチャート（spraychart） | `ohtani_1_spraychart_pybaseball.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yasumorishima/mlb-statcast-visualization/blob/main/ohtani_1_spraychart_pybaseball.ipynb) |
| 2 | 大谷翔平 ヒートマップ（matplotlib手動描画） | `ohtani_2_matplotlib_manual.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yasumorishima/mlb-statcast-visualization/blob/main/ohtani_2_matplotlib_manual.ipynb) |
| 3 | ダルビッシュ有 投球スタイル進化（2021-2025） | `darvish_evolution_2021_2025.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yasumorishima/mlb-statcast-visualization/blob/main/darvish_evolution_2021_2025.ipynb) |

## スプレーチャート 2つの方法の比較

| 項目 | 方法1 (spraychart) | 方法2 (matplotlib) |
|------|-------------------|-------------------|
| **コード量** | 最小（1行） | 多い |
| **座標変換** | 不要 | 必要 |
| **球場形状** | 30球団内蔵 | 自分で描く |
| **ヒートマップ** | 難しい | 容易 |
| **カスタマイズ** | 制限あり | 自由 |

## セットアップ

```python
!pip install pybaseball duckdb seaborn -q
```

## 注意: game_typeフィルタ

オープン戦のデータを除外するために、必ず`game_type = "R"`でフィルタしてください。

## Statcast座標変換（スプレーチャート用）

```python
x = 2.5 * (hc_x - 125.42)  # ホームプレートを原点に
y = 2.5 * (198.27 - hc_y)  # Y軸を反転
```

## 参考

- [pybaseball](https://github.com/jldbc/pybaseball)
- [Baseball Savant](https://baseballsavant.mlb.com/)
