# 📄 Codexタスク: PDF作成

**発行日**: 2026-01-08
**担当**: Codex / Claude Code
**ステータス**: 🔄 進行中

---

## 🎯 目標

詳細版PDF（16ページ）のデザインテンプレートを作成する。

---

## 📋 タスク内容

### 方法1: Figma MCP経由（推奨）
```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp -s project
```
- Figmaでテンプレートを作成
- 4タイプ×4ページ = 16ページ
- PDF出力

### 方法2: HTML/CSS テンプレート
- HTMLで印刷用テンプレートを作成
- ブラウザからPDF出力
- `/ai-diagnosis/pdf-templates/` に配置

---

## 📄 コンテンツ参照

- [PDFロードマップ_詳細版16ページ.md](file:///C:/Users/chatg/Obsidian%20Vault/papa/本山貴裕/11_開発ツール連携図_事業構想/PDFロードマップ_詳細版16ページ.md)

---

## 🎨 デザイン仕様

| 項目 | 設定 |
|------|------|
| サイズ | A4縦（210mm × 297mm） |
| フォント | Noto Sans JP |
| カラー | ダークテーマ（診断ツールと統一） |
| 背景 | グラデーション（#0f172a → #1e1b4b） |

---

## 📦 成果物

- [ ] ライター型 PDF（4ページ）
- [ ] クリエイター型 PDF（4ページ）
- [ ] コンサル型 PDF（4ページ）
- [ ] ビルダー型 PDF（4ページ）

---

*割り当て: Leo (Antigravity PM)*
