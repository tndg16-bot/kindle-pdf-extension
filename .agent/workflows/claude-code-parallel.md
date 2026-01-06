---
description: Claude Code並列開発ワークフロー（Web→GitHub→Chat→Local）
---

# Claude Code 並列開発ワークフロー

## コア・フロー

```
Web (初期実装) → GitHub (連携) → Chat (レビュー) → Local (最終調整)
```

## 1. Webフェーズ
- **ツール**: Claude Code Web
- **役割**: 0→1のコード生成、大規模リファクタリング
- **基準**: ビルドエラーがあってもOK、ファイル構成と主要ロジックが合っていれば合格

## 2. GitHubフェーズ
// turbo
```bash
git pull --rebase origin main
git checkout -b feature/new-function
```

**コミットルール**:
- `feat:` 新機能
- `fix:` バグ修正
- `docs:` ドキュメント

## 3. Chatフェーズ
- **ツール**: Antigravity / Codex / Claude Code
- **役割**: 生成コードのクロスチェック、細部修正

## 4. Localフェーズ（Last Resort）
- **条件**: 3分悩んだら自分で書く
- **用途**: デザイン微調整、環境変数設定、複雑なデバッグ

---

詳細: [01_Workflow_Guide.md](file:///C:/Users/chatg/Obsidian%20Vault/papa/docs/M9_Parallel_Workflow/01_Workflow_Guide.md)
