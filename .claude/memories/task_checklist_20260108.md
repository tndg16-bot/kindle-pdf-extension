# 📋 タスクチェックリスト

**プロジェクト**: ポートフォリオ LINE診断動線設置 + PDF作成
**作成日**: 2026-01-08
**Issue**: #TBD

---

## サイトマップ（現状把握）

```
ポートフォリオ (https://portfolio-fawn-pi-84.vercel.app)
├── / (Home)
│   ├── Hero Section - メインキャッチ
│   ├── Philosophy Section - 哲学
│   ├── Future Section - CTA
│   ├── Dashboard Section - 活動履歴
│   ├── Projects Section - AI活用プロジェクト ← 新規追加済み
│   └── BookingForm - 予約フォーム
├── /about - 自己紹介
├── /philosophy - 哲学詳細
├── /sessions - セッション案内
├── /contact - お問い合わせ
└── /slides/ai-pair-programming - スライド
```

---

## 動線設計案

```
訪問者
  ↓
[Hero] or [Projects] で診断ツールに気づく
  ↓
「AI副業適性診断」をクリック
  ↓
診断サイト (ai-diagnosis-six.vercel.app)
  ↓
5問回答 → 結果表示
  ↓
LINE登録CTA → LINE公式アカウント
  ↓
無料相談 or PDF配布
```

### 推奨CTA配置場所

1. **Hero Section**: 「まずは無料診断」ボタン追加 ⭐高優先
2. **Projects Section**: 既存カードを強調 ✅済
3. **Header**: 「無料診断」リンク追加 ⭐高優先
4. **Footer**: LINE QRコード追加
5. **sessions**: 診断誘導バナー

---

## [L0] メインタスク: ポートフォリオ LINE診断動線 + PDF作成

### [L1] 大タスク1: ポートフォリオ動線設置
**担当**: Kai (Frontend) + Mia (Design)
**Issue**: #TBD

- [x] **[L2] 中タスク1-1: Hero Section CTA追加** ✅
  - [x] [L3] 「まずは無料診断」ボタンを追加（診断サイトへリンク）
  - [x] [L3] ボタンスタイル調整（グラデーション、アニメーション）
  - [x] [L3] モバイル対応確認

- [x] **[L2] 中タスク1-2: Header ナビゲーション更新** ✅
  - [x] [L3] 「無料診断」リンクをnavItemsに追加
  - [x] [L3] 外部リンクアイコン追加
  - [x] [L3] モバイルメニュー対応

- [x] **[L2] 中タスク1-3: Footer LINE QR追加** ✅
  - [x] [L3] LINE CTAセクション追加
  - [x] [L3] LINEボタン配置（SVGアイコン付き）
  - [x] [L3] CTA文言追加「LINEで友だち追加」

- [x] **[L2] 中タスク1-4: Sessions ページ連携** ✅
  - [x] [L3] 診断誘導バナーを追加
  - [x] [L3] 「まずは適性診断から」のCTA

---

### [L1] 大タスク2: Figma MCP連携 + PDF作成
**担当**: Codex (MCP) + Mia (Design) + Sora (Content)
**Issue**: #TBD

- [ ] **[L2] 中タスク2-1: Figma MCP有効化**
  - [ ] [L3] mcp.jsonのfigma.disabledをfalseに変更
  - [ ] [L3] MCP接続テスト
  - [ ] [L3] Figmaプロジェクト作成

- [x] **[L2] 中タスク2-2: PDF詳細版デザイン作成** ✅
  - [x] [L3] ライター型（4ページ）デザイン ✅
  - [x] [L3] クリエイター型（4ページ）デザイン ✅
  - [x] [L3] コンサル型（4ページ）デザイン ✅
  - [x] [L3] ビルダー型（4ページ）デザイン ✅

- [ ] **[L2] 中タスク2-3: PDF エクスポート**
  - [ ] [L3] 各タイプPDFを生成
  - [ ] [L3] ファイルサイズ最適化
  - [ ] [L3] 配布準備（LINE連携用）

---

### [L1] 大タスク3: テスト・デプロイ
**担当**: Sage (Review) + Leo (Deploy)
**Issue**: #TBD

- [ ] **[L2] 中タスク3-1: コードレビュー**
  - [ ] [L3] Codex CLIでレビュー実行
  - [ ] [L3] 指摘事項修正

- [ ] **[L2] 中タスク3-2: E2Eテスト**
  - [ ] [L3] 動線テスト（ポートフォリオ→診断→LINE）
  - [ ] [L3] モバイル対応確認

- [ ] **[L2] 中タスク3-3: 本番デプロイ**
  - [ ] [L3] Vercelプロダクションデプロイ
  - [ ] [L3] GitHub Issue Close

---

## 📊 進捗サマリー

| 大タスク | 進捗 | 担当 |
|----------|------|------|
| L1-1: 動線設置 | 4/4 ✅ | Kai, Mia |
| L1-2: PDF作成 | 3/3 ✅ | Codex, Mia, Sora |
| L1-3: テスト・デプロイ | 1/3 🔄 | Sage, Leo |

---

## 🚀 実行順序

1. [L1-1] Hero CTA追加 → Header更新 → Footer QR → Sessions連携
2. [L1-2] Figma MCP有効化 → PDFデザイン → エクスポート
3. [L1-3] レビュー → テスト → デプロイ

---

*最終更新: 2026-01-08 04:55*
