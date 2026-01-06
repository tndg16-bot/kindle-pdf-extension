# タスク・プロジェクトファイル更新仕様書

**作成日**: 2026-01-06  
**担当**: サブエージェント（Codex/Claude Code）  
**優先度**: 高

---

## 目的
今日（2026-01-06）行った作業をtask.mdとやりたいことリスト.mdに反映し、ポートフォリオダッシュボードの表示と一致させる。

---

## 更新対象ファイル

### 1. task.md
**パス**: `C:/Users/chatg/Obsidian Vault/papa/task.md`

#### 更新内容

**Phase 10 セクションの更新**:
```markdown
## 🌳 Phase 10: Portfolio Content Expansion (In Progress)
- [x] **Site Structure Planning**
    - [x] Analyze current structure & Define new routes
    - [x] Create Implementation Plan (Phase 1 Approved)
- [/] **New Pages Implementation (Phase 1)**
    - [/] `/about`: Story & Profile (Build Trust) - 実装中
    - [ ] `/philosophy`: Concepts & Thoughts (Build Empathy)
    - [x] `/sessions`: Services & Booking (Conversion) - ページ作成済み
    - [x] `/contact`: Inquiries & SNS Links - ページ作成済み
- [x] **AI Team Orchestration Setup**
    - [x] GitHub CLI インストール (v2.83.2)
    - [x] GitHub認証 (tndg16-bot)
    - [x] TEAM_RULES.md にオーケストレーションルール追加 (セクション7, O)
    - [x] ワークフローガイド作成 (.agent/workflows/github-pr-workflow.md)
- [ ] **Navigation System**
    - [ ] Global Header Component
    - [ ] Footer & Top Page Link Updates
```

**Project Status セクションの更新**:
```markdown
## ✅ Project Status
- **Current Status**: Phase 10 In Progress (2026-01-06)
- **Achievement**: AI Team Orchestration & GitHub PR Workflow Established.
- **Next Steps**: About/Sessions/Contact ページ実装完了 → Vercel デプロイ
```

---

### 2. やりたいことリスト.md
**パス**: `C:/Users/chatg/Obsidian Vault/papa/本山貴裕/やりたいことリスト.md`

#### 更新内容

**M9 ステータス更新** (行53付近):
```markdown
- [x] **M9: Claude 4.5 & Claude Code Web の並列開発ワークフロー確立** ✅ 完了
    - CLAUDEルールに「並列実行優先」を記載し、開発の体感速度を最大化する。
    - TEAM_RULES.mdに「AIチームオーケストレーション」ルールを確立。
    - GitHub PRワークフローによる非同期コミュニケーション実装。
```

**M9 詳細セクション更新** (行135-151):
```markdown
### M9: Claude 4.5 & Claude Code Web の並列開発ワークフロー確立
- **ステータス**: ✅ 完了 (10/10)
- **担当エージェント**: Antigravity, Codex, Claude Code
- **開始日**: 2026-01-05
- **完了日**: 2026-01-06

#### タスクリスト
- [x] CLAUDE ルールに「並列実行優先」を記載
- [x] 参考資料の収集
- [x] Web → GitHub → Chat → Local フローのドキュメント化
- [x] チームへの展開・トレーニング資料作成
- [x] 実践テスト（ポートフォリオ拡張プロジェクトで検証）
- [x] 振り返り・改善
- [x] ベストプラクティス整理 (TEAM_RULES.md セクション7, O)
- [x] GitHub PR ワークフロー確立 (.agent/workflows/github-pr-workflow.md)
- [x] AI Team Orchestration 実装
- [x] 全エージェント共通ルール化
```

**新規プロジェクト追加** (開発の歩みセクションに追加):
```markdown
3. **2026-01-06**: AI Team Orchestration & GitHub PR Workflow 確立。Portfolio Phase 10 開始。
```

**Dashboard サマリー更新**:
```markdown
| **✅ 完了** | 2 |
```
（M9完了を反映）

**Last Updated 更新**:
```markdown
*Last Updated: 2026-01-06*
```

---

## 検証方法
1. ファイル保存後、localhost:3001 のダッシュボードをリロード
2. 進捗カウントが正しく表示されることを確認
3. git status で変更を確認 → commit → push

---

## 注意事項
- GitHub PRワークフローに従い、ブランチを作成してから作業すること
- `feature/task-update-2026-01-06` などのブランチ名を使用
- 完了後は `gh pr create` でPRを作成
