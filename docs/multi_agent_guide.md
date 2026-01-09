# マルチエージェント運用ガイド

## 🎖 エージェント階層構造

```
👤 管理者（あなた）
    │
    ├── 🎖 Antigravity (PM)
    │       ├── タスク分解・Issue作成
    │       ├── 進捗管理
    │       └── PRレビュー・マージ
    │
    └── 🛠 サブエージェント群
            ├── Claude Code（デバッグ・リファクタ）
            ├── Codex CLI（ChatGPT連携）
            └── Gemini CLI（Google連携・調査）
```

---

## 📋 ワークフロー

### Step 1: 管理者 → Antigravity
大きな目標を Antigravity に伝える。

```
例: 「ポートフォリオサイトのパフォーマンスを改善したい」
```

### Step 2: Antigravity → GitHub Issue
タスクを分解し、GitHub Issue を作成。

**Issue作成時のルール:**
- テンプレート `🤖 AIエージェント向けタスク` を使用
- 担当エージェントをラベルで明示
- 期待する成果をチェックリストで記載

### Step 3: サブエージェント → 作業実行
各エージェントは割り当てられた Issue を確認し、作業開始。

### Step 4: サブエージェント → PR作成
作業完了後、PR を作成（テンプレート使用）。

### Step 5: GitHub Actions → 自動チェック
Lint/Build が自動実行される。

### Step 6: Antigravity → レビュー・マージ
CI が通れば Antigravity がレビューし、マージ。

### Step 7: Antigravity → 完了報告
管理者に作業完了を報告。

---

## 🚀 サブエージェントの起動方法

### Claude Code
```powershell
cd "c:\Users\chatg\Obsidian Vault\papa"
claude
```
起動後、GitHub Issue の URL を貼り付けて指示。

### Codex CLI
```powershell
cd "c:\Users\chatg\Obsidian Vault\papa"
codex
```

### Gemini CLI
```powershell
cd "c:\Users\chatg\Obsidian Vault\papa"
gemini
```

---

## 📝 サブエージェントへの指示テンプレート

```markdown
## 🎯 タスク: [Issue #番号] [タイトル]

### GitHub Issue
https://github.com/tndg16-bot/kindle-pdf-extension/issues/XX

### 目的
[何を達成したいか]

### 期待する成果
- [ ] [具体的な成果物1]
- [ ] [具体的な成果物2]

### 制約
- [やってはいけないこと]

### 完了条件
- [ ] Lint が通る
- [ ] ビルドが成功する
- [ ] PR を作成し、Issue と紐付ける
```

---

## 📊 作業結果の集約

### GitHub Projects ボード

| To Do | In Progress | Review | Done |
|-------|-------------|--------|------|
| 新規Issue | AI作業中 | PR待ち | 完了 |

### 自動化設定（GitHub側で設定）
1. Issue 作成 → 自動で「To Do」へ
2. PR 作成 → 自動で「Review」へ
3. PR マージ → 自動で「Done」へ、Issue クローズ

---

*更新日: 2026-01-09*
