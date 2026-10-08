# 大谷翔平の打球速度予測 - Random Forest回帰分析

## サマリー

| 項目 | 値 |
|------|-----|
| 対象 | 大谷翔平 2025年レギュラーシーズン |
| データ | 2,865打席 → 802打球（打球あり） |
| モデル | RandomForestRegressor（n_estimators=100, max_depth=10） |
| 訓練MAE | 8.04 mph（R²=0.65） |
| テストMAE | 14.16 mph（R²=-0.00） |

**結論**: 打球速度はコース（plate_x + plate_z = 46%）に最も依存し、球速（release_speed = 13%）の影響は小さい。投手データだけでの予測は困難（過学習）。

---

## 特徴量重要度

| 順位 | 特徴量 | 重要度 |
|------|--------|--------|
| 1 | plate_z（高さ） | 23.76% |
| 2 | plate_x（横位置） | 22.22% |
| 3 | release_spin_rate（回転数） | 14.63% |
| 4 | release_speed（球速） | 12.99% |
| 5 | pfx_x（横変化量） | 12.89% |

コース（plate_z + plate_x）が合計46%で最も支配的。球速は4位の13%に過ぎない。

## 球速と打球速度の関係

- 相関係数: **0.150**（ほぼ無相関）
- 球速が速い＝打球速度が速いとは限らない

## 使用データ

- ソース: MLB Statcast（pybaseball経由）
- 選手ID: 660271（大谷翔平）
- 期間: 2025年3月〜シーズン中
- 特徴量: release_speed, pitch_type, release_spin_rate, plate_x, plate_z, pfx_x, pfx_z

## 実装

### データ準備

```python
from pybaseball import statcast_batter
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

df = statcast_batter('2025-03-01', '2025-10-01', 660271)
df = df[df['game_type'] == 'R'].copy()
df_contact = df[df['launch_speed'].notna()].copy()
```

### 特徴量エンジニアリング

```python
features = ['release_speed', 'pitch_type', 'release_spin_rate',
            'plate_x', 'plate_z', 'pfx_x', 'pfx_z']
target = 'launch_speed'

df_ml = df_contact[features + [target]].dropna()
df_ml = pd.get_dummies(df_ml, columns=['pitch_type'], drop_first=True)
```

- pitch_type（文字列）をダミー変数化: 12球種 → 11列
- 最終特徴量数: 17

### モデル学習・評価

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(
    n_estimators=100, max_depth=10,
    min_samples_split=5, random_state=42, n_jobs=-1
)
model.fit(X_train, y_train)
```

| データ | MAE | R² |
|--------|-----|-----|
| 訓練 | 8.04 mph | 0.65 |
| テスト | 14.16 mph | -0.00 |

訓練データではR²=0.65だがテストではR²≒0 → 過学習。投手側データのみでは打球速度の汎化的予測は困難。

## 可視化

- 散布図: 球速 vs 打球速度（回帰直線付き）
- ストライクゾーンヒートマップ: 位置別打球速度
- ボックスプロット/バイオリンプロット: 球種別打球速度
- 特徴量重要度: 横棒グラフ（上位15）
- 予測精度: 実測 vs 予測（訓練/テスト）、誤差分布

## scikit-learn基本フロー

```
データ準備 → train_test_split → RandomForestRegressor() → .fit() → .predict() → 評価 → .feature_importances_
```

## 参考

- [scikit-learn](https://scikit-learn.org/)
- [pybaseball](https://github.com/jldbc/pybaseball)
- [RandomForest](https://scikit-learn.org/stable/modules/ensemble.html#forest)
