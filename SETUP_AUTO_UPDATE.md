# 📊 投資ダッシュボード — 自動データ更新セットアップガイド

## 概要

GitHub Actions を使って**毎日朝7時（日本時間）**に自動で最新の株価データを取得し、ダッシュボードに反映する仕組みです。

**仕組み:**
1. GitHub Actions が毎朝 `scripts/fetch_data.py` を実行
2. yfinance で149銘柄の最新データ（株価・変動率・PER・配当利回り）を取得
3. `data.json` としてリポジトリに自動コミット
4. ダッシュボード（index.html）がページ読み込み時に `data.json` を読み込んで表示を更新

---

## セットアップ手順

### ステップ1: ファイルをGitHubにpush

ターミナルで以下を実行します:

```bash
cd ~/my-project

# 新しいファイルをコピー
cp -r investment_dashboards/.github .github
cp -r investment_dashboards/scripts scripts
cp investment_dashboards/data.json data.json
cp investment_dashboards/index.html index.html

# コミット＆プッシュ
git add .github scripts data.json index.html
git commit -m "自動データ更新の仕組みを追加"
git push
```

### ステップ2: GitHub Actions を有効化

1. GitHubでリポジトリページを開く
2. 上部の **「Actions」** タブをクリック
3. 「I understand my workflows, go ahead and enable them」をクリック（初回のみ）

### ステップ3: 手動で初回実行テスト

1. **Actions** タブ → 左側の **「📊 Update Stock Data」** をクリック
2. 右側の **「Run workflow」** ボタンをクリック
3. **「Run workflow」** を確認クリック
4. 1〜2分待って、緑のチェックマーク ✅ が出れば成功！

### ステップ4: 動作確認

GitHub Pages のURLを開いて、ヘッダーに「📊 データ更新: 2026-03-10 07:00 JST」のような表示が出ていれば完了です。

---

## ファイル構成

```
投資ダッシュボード/
├── index.html          ← メインのダッシュボード
├── data.json           ← 自動更新される株価データ
├── scripts/
│   └── fetch_data.py   ← データ取得スクリプト
└── .github/
    └── workflows/
        └── update-data.yml  ← 自動実行の設定
```

---

## カスタマイズ

### 更新頻度を変えたい場合

`.github/workflows/update-data.yml` の cron 部分を変更:

```yaml
# 毎日朝7時（日本時間）← 現在の設定
- cron: '0 22 * * *'

# 平日のみ朝7時と夕方18時
- cron: '0 22 * * 1-5'
  # と
- cron: '0 9 * * 1-5'

# 毎週月曜朝7時のみ
- cron: '0 22 * * 1'
```

※ cron は UTC 時間なので、日本時間から -9時間 して指定します。

### 手動で即座に更新したい場合

GitHub の Actions タブ → 「📊 Update Stock Data」 → 「Run workflow」をクリック

---

## トラブルシューティング

**Q: Actions が動かない**
→ リポジトリの Settings → Actions → General で「Allow all actions」が選択されているか確認

**Q: data.json が更新されない**
→ Actions タブで実行ログを確認。赤い ✗ マークの場合、ログにエラー詳細が表示される

**Q: 一部の銘柄データが取れない**
→ yfinance が対応していない銘柄がある場合があります。その場合、その銘柄は HTML に記載の初期値がそのまま使われます

---

## 費用

**すべて無料** で運用できます:
- GitHub Actions: パブリックリポジトリは無料、プライベートでも月2,000分の無料枠
- yfinance: 無料（Yahoo Finance の非公式API）
- GitHub Pages: 無料
