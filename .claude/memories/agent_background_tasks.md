# 🤖 AIエージェント バックグラウンドタスク

**発行日**: 2026-01-08
**発行者**: Leo (Project Manager / Antigravity)

---

## 📋 タスク一覧

### タスク1: LINE連携設定
**担当**: Leo (Antigravity)
**ステータス**: ✅ 完了（https://lin.ee/VAYurUv 設定済み）

**作業内容**:
1. ユーザーからLINE公式アカウントのURLを取得
2. `ai-diagnosis/src/App.tsx`の`LINE_URL`を更新
3. Vercelに再デプロイ
4. 動作確認

**必要情報**:
- LINE公式アカウントのURL（形式: `https://line.me/R/ti/p/@xxxxx`）

---

### タスク2: Canva/Figma MCP連携（PDFデザイン）
**担当**: Codex / Claude Code（バックグラウンド）
**優先度**: 🟠 中

**作業内容**:
1. Figma MCPを有効化（現在disabled）
2. 詳細版PDF（16ページ）のデザインをFigma/Canvaで作成
3. PDFとしてエクスポート

**MCP設定ファイル**: `.claude/mcp.json`
```json
"figma": {
  "disabled": true,  // → false に変更
  "type": "http",
  "url": "https://mcp.figma.com/mcp"
}
```

**コマンド**:
```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp -s project
```

---

### タスク3: ポートフォリオサイトに診断ツール組み込み
**担当**: Kai (Frontend Engineer) + Mia (Design)
**ステータス**: ✅ 完了（https://portfolio-fawn-pi-84.vercel.app）

**作業内容**:
1. ポートフォリオサイトにProjectsセクションを追加
2. AI副業適性診断ツールをiframeまたはリンクで埋め込み
3. デザインの統一性を確認（Miaがレビュー）

**技術スタック**:
- Next.js 15
- Tailwind CSS v4
- Framer Motion

---

## 👥 エージェントチーム

| ペルソナ | 役割 | 担当タスク |
|---------|------|-----------|
| **Leo** | Project Manager | 全体調整、LINE連携 |
| **Kai** | Frontend Engineer | ポートフォリオ組み込み |
| **Mia** | UI/UX Designer | PDFデザイン、デザインレビュー |
| **Sage** | Code Reviewer | コードレビュー、品質チェック |
| **Sora** | Content Creator | PDFコンテンツ最終調整 |
| **Codex** | Coding Agent | MCP連携、バックグラウンド作業 |

---

## 📊 ワークフロー

```
[Leo] タスク定義
    ↓
[Kai + Mia] 並列作業（ポートフォリオ）
    ↓
[Codex] MCP連携作業（Figma）
    ↓
[Sage] レビュー
    ↓
[Leo] 最終確認・デプロイ
```

---

## ⚠️ 注意事項

1. **Issue先行ルール**: 作業前にGitHub Issueを作成
2. **3分ルール**: 3分悩んだら人間に聞く
3. **Atomic Commit**: 1機能1コミット
4. **Codex必須**: コードレビューはCodex CLIを経由

---

## 📝 TODO

- [x] LINEのURLを受け取る（ユーザーから）✅ 完了
- [ ] Figma MCPを有効化 ⏳ 次回
- [x] ポートフォリオサイトにProjectsセクションを追加 ✅ 完了
- [ ] PDFデザインを作成 ⏳ 次回

---

*作成: Leo (Antigravity)*
