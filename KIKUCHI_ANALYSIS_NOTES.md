# 菊池雄星 投球分析ノート

## ステータス
- **ノートブック**: `kikuchi_2019_2025.ipynb` 作成・push済み（2/5）
- **次のステップ**: Colabで全セル実行 → 出力付きでpush → テキスト出力で一緒に確認 → ブログ記事化

## Colab URL
https://colab.research.google.com/github/yasumorishima/mlb-statcast-visualization/blob/main/kikuchi_2019_2025.ipynb

## 基本情報
- **Player ID**: 579328
- **投打**: 左投左打
- **分析期間**: 2019-2025（7年間）

## キャリア
| 年 | チーム | 備考 |
|---|---|---|
| 2019 | SEA | MLB初年、ERA 5.46 |
| 2020 | SEA | 短縮シーズン、ERA 5.17 |
| 2021 | SEA | 前半オールスター、後半崩壊 |
| 2022 | TOR | ERA 5.19 |
| 2023 | TOR | ERA 3.86（改善） |
| 2024前半 | TOR | ERA 4.75（22試合） |
| 2024後半 | HOU | **ERA 2.70**（10試合、覚醒） |
| 2025 | LAA | ERA 3.99、**33先発**、174K、3年$63M契約 |

## アストロズ移籍後の変化（報道まとめ）
1. **スライダー使用率の劇増**: 22.2% → 37.1%（被打率 .248 → .172）
2. **専属捕手の配置**: ビクター・カラティニが全6試合先発
3. **アストロズのデータ分析チーム**が投球戦略を最適化

## ノートブック構成（33セル、15セクション）
1. Data Acquisition - 2019-2025全データ取得、8期間タグ付け
2. Career Overview - 年度別GS/投球数/球速
3. Pitch Arsenal - KEY_PERIODS(2022-2025)の球種構成
4. Pitch Mix Evolution - 7年間の球種配分推移チャート
5. **Slider Revolution** - SL使用率・空振り率・位置のTOR vs HOU vs LAA比較（メイン）
6. Velocity & Spin - FF球速+スピン率の経年変化
7. Fatigue Pattern - イニング別球速低下（2025スタミナ検証）
8. Whiff Rate - 球種別空振り率の推移
9. Two-Strike Strategy - 2ストライク時の決め球変化
10. Batted Ball - xwOBA/Hard Hit%/Exit Velo
11. Release Point - リリースポイント+エクステンション比較
12. Movement Profile - 全球種の変化量散布図（5期間並列）
13. L/R Splits - 左右打者別の攻め方
14. Time Through Order - 打順周り別の劣化パターン
15. Summary - 全体まとめ

## 期間定義
- `PERIOD_ORDER`: 2019, 2020, 2021, 2022, 2023, 2024-TOR, 2024-HOU, 2025
- `KEY_PERIODS`: 2022, 2023, 2024-TOR, 2024-HOU, 2025
- 2024年のTOR/HOU分割: `2024-07-30`を境界（7/29トレード成立）

## 分析で注目したいポイント
- スライダー（SL or ST）の使用率変化が数字で見えるか
- アストロズ移籍後にリリースポイントやエクステンションが変わったか
- 2025年のスタミナパターン（33先発を支えた要因）
- 3巡目対策がどう改善されたか（TTO分析）
- 左右打者への攻め方の変化

## ブログ記事の方向性（案）
- タイトル案: 「Statcastデータで見る菊池雄星の『スライダー革命』（2019-2025）」
- 重要方針11に従い、断定表現を避ける
- 冒頭に「データから読み取れる傾向の紹介」の断り書き
- メインストーリー: TOR→HOU移籍でスライダー増加 → LAA定着

## 参考記事
- [BASEBALL KING: 防御率4.75→2.70に大きく改善](https://baseballking.jp/ns/column/462495)
- [Yahoo!ニュース: なぜ菊池雄星はアストロズで覚醒したのか](https://news.yahoo.co.jp/expert/articles/a9d910be0fb6767923939fa5eca1faca06c7e08c)
- [Baseball Savant: Kikuchi Stats](https://baseballsavant.mlb.com/savant-player/yusei-kikuchi-579328)
