# MLB Statcast 打球分布の可視化 - 3つの方法

Statcastデータで大谷翔平の打球分布（スプレーチャート）を3つの方法で可視化するサンプルコードです。

Google Colabで実行できます。

## Notebooks

| # | 方法 | Notebook | Open in Colab |
|---|------|----------|---------------|
| 1 | pybaseball `spraychart()` | `ohtani_1_spraychart_pybaseball.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yasumorishima/mlb-statcast-visualization/blob/main/ohtani_1_spraychart_pybaseball.ipynb) |
| 2 | matplotlib 手動描画 | `ohtani_2_matplotlib_manual.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yasumorishima/mlb-statcast-visualization/blob/main/ohtani_2_matplotlib_manual.ipynb) |

## 2つの方法の比較

| 項目 | 方法1 (spraychart) | 方法2 (matplotlib) |
|------|-------------------|-------------------|
| **コード量** | 最小（1行） | 多い |
| **座標変換** | 不要 | 必要 |
| **球場形状** | 30球団内蔵 | 自分で描く |
| **ヒートマップ** | 難しい | 容易 |
| **カスタマイズ** | 制限あり | 自由 |

## セットアップ

```python
!pip install pybaseball duckdb sportypy seaborn -q
```

## 注意: game_typeフィルタ

オープン戦のデータを除外するために、必ず`game_type = "R"`でフィルタしてください。

## Statcast座標変換

```python
x = 2.5 * (hc_x - 125.42)  # ホームプレートを原点に
y = 2.5 * (198.27 - hc_y)  # Y軸を反転
```

## 参考

- [pybaseball](https://github.com/jldbc/pybaseball)
- [sportypy](https://github.com/sportsdataverse/sportypy)
- [Baseball Savant](https://baseballsavant.mlb.com/)
