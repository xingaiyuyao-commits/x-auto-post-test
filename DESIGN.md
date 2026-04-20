# DESIGN.md — みゆうさんX投稿ビジュアル

X投稿用の画像（表・図解）の統一デザイン仕様。note風の柔らかな読み物トーンをベースに、SNSで保存・スクショされやすい清潔感を優先。

---

## 1. Visual Theme & Atmosphere

- **方針**: 柔らかく、清潔、読みやすい。情報は1秒で理解できる構造
- **密度**: ゆったりとした余白。数字や比較が主役
- **キーワード**: 落ち着き、温かい、ミニマル、女性的、知的
- **特徴**: 純粋な黒を使わず `#08131a` ベースで柔らかい視認性。アクセントは控えめなオレンジ

---

## 2. Color Palette

### Base
- **Background Primary** `#fdfaf5`（薄いアイボリー）
- **Background Secondary** `#ffffff`（カード面）
- **Background Tertiary** `#f5f1ea`（比較表の参考列・薄グレー役）

### Text
- **Text Primary** `#08131a`（本文・数字）
- **Text Secondary** `rgba(8,19,26,0.66)`（ラベル・補足）
- **Text Muted** `rgba(8,19,26,0.45)`（キャプション）

### Accent
- **Accent Orange** `#d97757`（強調・矢印・ハイライト）
- **Accent Orange Soft** `#f5e4d9`（背景ハイライト）

### Border
- **Border Default** `rgba(8,19,26,0.10)`
- **Border Strong** `rgba(8,19,26,0.20)`

---

## 3. Typography

### 和文
```
"ヒラギノ角ゴ ProN", "Hiragino Kaku Gothic ProN",
"Noto Sans JP", "メイリオ", Meiryo, sans-serif
```

### 欧文・数字
```
"Inter", -apple-system, BlinkMacSystemFont, sans-serif
```

### Scale
- **Display** 56-72px / weight 700 / line-height 1.3（大きな数字）
- **Heading L** 32-40px / weight 700 / line-height 1.4（タイトル）
- **Heading M** 22-26px / weight 600 / line-height 1.5（列見出し）
- **Body** 16-18px / weight 500 / line-height 1.7
- **Caption** 13-14px / weight 500 / line-height 1.6

### Rules
- line-height は本文 1.6〜1.8
- letter-spacing は見出しのみ。本文は `normal`
- 数字は Inter で視認性を上げる

---

## 4. Spacing Scale

8px 基準スケール：**4 / 8 / 16 / 24 / 32 / 40 / 56 / 72 / 96**

- カード端 padding: 40-56px
- 要素間マージン: 24-32px
- 密度の高い行間: 8-16px

---

## 5. Component Patterns

### 比較表カード
- 背景 `#ffffff`、角丸 20px、影 `0 4px 24px rgba(8,19,26,0.06)`
- 列ヘッダー背景 `#f5f1ea`、または基準列のみ `#f5f1ea`
- セル padding 24px
- 罫線 `rgba(8,19,26,0.08)`

### ハイライトセル
- 背景 `#f5e4d9`、テキスト `#d97757`
- または枠 2px solid `#d97757`

### 矢印・注釈
- 色 `#d97757`
- 太さ 2.5px
- 末尾はシンプルな▲や→

---

## 6. Canvas Sizes

| 用途 | サイズ | Aspect |
|---|---|---|
| X投稿 横長 | 1200×675 | 16:9 |
| X投稿 正方形 | 1080×1080 | 1:1 |
| X投稿 縦長 | 1080×1350 | 4:5 |

---

## 7. Do / Don't

✅ Do
- 余白を十分に取る（詰めすぎない）
- 数字を主役に、ラベルは控えめに
- 1枚1メッセージ

❌ Don't
- 純黒 `#000` を使わない
- グラデーションを使わない（ミニマル感を保つ）
- 情報を詰め込みすぎない（比較は3列まで）
- 煽り言葉をタイトルに使わない（「必見」「劇的に」など）
