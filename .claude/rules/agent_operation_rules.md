# 🤖 AIエージェント運用ルール

**作成日**: 2026-01-08
**更新日**: 2026-01-08

---

## 📋 タスク分解ルール

### 階層構造

| レベル | 名称 | 説明 | 例 |
|--------|------|------|-----|
| **L0** | メインタスク | プロジェクト全体の目標 | ポートフォリオにLINE診断動線を設置 |
| **L1** | 大タスク | 主要な作業単位（1 GitHub Issue） | サイトマップ把握、動線設計、実装 |
| **L2** | 中タスク | 具体的な作業 | ページ構造分析、CTA配置検討 |
| **L3** | 小タスク | 最小実行単位（1コミット相当） | ボタン追加、スタイル調整 |

### チェックリスト形式

```markdown
## [L0] メインタスク名
- [ ] **[L1] 大タスク1**
  - [ ] [L2] 中タスク1-1
    - [ ] [L3] 小タスク1-1-1
    - [ ] [L3] 小タスク1-1-2
  - [ ] [L2] 中タスク1-2
- [ ] **[L1] 大タスク2**
  ...
```

### ステータス記号

| 記号 | 意味 |
|------|------|
| `[ ]` | 未着手 |
| `[/]` | 進行中 |
| `[x]` | 完了 |
| `[!]` | ブロック中（要確認） |
| `[-]` | スキップ/中止 |

---

## 👥 エージェント割り当てルール

### エージェント一覧

| ペルソナ | 役割 | 担当レベル |
|---------|------|-----------|
| **Leo** | PM / Antigravity | L0-L1（計画・調整） |
| **Kai** | Frontend Engineer | L2-L3（実装） |
| **Mia** | UI/UX Designer | L2（デザイン） |
| **Sage** | Code Reviewer | L2-L3（レビュー） |
| **Sora** | Content Creator | L2-L3（コンテンツ） |
| **Codex** | Coding Agent | L3（バックグラウンド実装） |

### 割り当て基準

1. **フロントエンド実装** → Kai
2. **デザイン判断** → Mia
3. **コンテンツ作成** → Sora
4. **コードレビュー** → Sage（Codex経由必須）
5. **全体調整・Issue管理** → Leo

---

## 📊 ワークフロー

```
[Leo] L0/L1タスク定義
    ↓
[Leo] エージェント割り当て
    ↓
[各エージェント] L2/L3タスク実行
    ↓
[Sage] レビュー（Codex経由）
    ↓
[Leo] マージ・デプロイ・Issue Close
```

---

## ⚠️ 必須ルール

1. **Issue先行**: L1タスクごとに1つのGitHub Issueを作成
2. **Atomic Commit**: L3タスクごとに1コミット
3. **3分ルール**: 3分悩んだら人間に報告
4. **チェックリスト更新**: タスク完了時に必ずステータス更新
5. **進捗可視化**: L1完了ごとにnotify_userで報告

---

## 📁 関連ファイル

- チームルール: [TEAM_RULES.md](file:///C:/Users/chatg/Obsidian%20Vault/papa/TEAM_RULES.md)
- ワークフロー: [claude-code-parallel.md](file:///C:/Users/chatg/Obsidian%20Vault/papa/.agent/workflows/claude-code-parallel.md)
- ペルソナ: [.claude/personas/](file:///C:/Users/chatg/Obsidian%20Vault/papa/.claude/personas/)

---

*作成: Leo (Antigravity)*
