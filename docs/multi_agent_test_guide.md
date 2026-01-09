# マルチエージェント テスト運用ガイド

## 🎯 テスト目標
- サブエージェント（Claude Code, Codex, Gemini CLI）の起動確認
- GitHub Issue → 作業 → PR → CI → レビュー の流れを検証

---

## 📋 事前準備チェックリスト

### 必要なツール
| ツール | インストール確認コマンド | インストール方法 |
|--------|------------------------|----------------|
| Claude Code | `claude --version` | `npm install -g @anthropic-ai/claude-code` |
| Codex CLI | `codex --version` | `npm install -g @openai/codex` |
| Gemini CLI | `gemini --version` | `npm install -g @google/gemini-cli` |

---

## 🚀 Step 1: ターミナル分割セットアップ

### Windows Terminal の場合
1. **Windows Terminal** を開く
2. 上部の「+」ボタン横の「∨」をクリック
3. 「ペインを分割」→「右に分割」を2回実行
4. 3つのペインが並んだ状態になる

```
┌─────────────────┬─────────────────┬─────────────────┐
│   Claude Code   │    Codex CLI    │   Gemini CLI    │
│                 │                 │                 │
└─────────────────┴─────────────────┴─────────────────┘
```

### VS Code の場合
1. `Ctrl + Shift + `` でターミナルを開く
2. ターミナル右上の「+」ボタンで新しいターミナルを追加
3. 3つのターミナルタブを作成

---

## 🤖 Step 2: 各エージェントの起動

### ペイン1: Claude Code
```powershell
cd "c:\Users\chatg\Obsidian Vault\papa"
claude
```

### ペイン2: Codex CLI
```powershell
cd "c:\Users\chatg\Obsidian Vault\papa"
codex
```

### ペイン3: Gemini CLI
```powershell
cd "c:\Users\chatg\Obsidian Vault\papa"
gemini
```

---

## 📝 Step 3: GitHub Issue の確認

各エージェントに以下のIssueが割り当てられます（Antigravityが作成）:

| Issue | 担当エージェント | タスク内容 |
|-------|----------------|-----------|
| #3 | Claude Code | `docs/test_claude.md` を作成 |
| #4 | Codex CLI | `docs/test_codex.md` を作成 |
| #5 | Gemini CLI | `docs/test_gemini.md` を作成 |

---

## 💬 Step 4: サブエージェントへの指示

### Claude Code への指示（ペイン1にコピペ）
```
GitHub Issue #3 を実行してください。

タスク: ファイル docs/test_claude.md を作成
内容: Claude Code が正常に動作することを確認するためのテストファイル

完了後:
1. ブランチ `test/claude-demo` を作成
2. 変更をコミット
3. PRを作成（Issue #3 を参照）
```

### Codex CLI への指示（ペイン2にコピペ）
```
GitHub Issue #4 を実行してください。

タスク: ファイル docs/test_codex.md を作成
内容: Codex CLI が正常に動作することを確認するためのテストファイル

完了後:
1. ブランチ `test/codex-demo` を作成
2. 変更をコミット
3. PRを作成（Issue #4 を参照）
```

### Gemini CLI への指示（ペイン3にコピペ）
```
GitHub Issue #5 を実行してください。

タスク: ファイル docs/test_gemini.md を作成
内容: Gemini CLI が正常に動作することを確認するためのテストファイル

完了後:
1. ブランチ `test/gemini-demo` を作成
2. 変更をコミット
3. PRを作成（Issue #5 を参照）
```

---

## ✅ Step 5: 検証項目

### 各エージェントが完了したら確認すること
- [ ] ブランチが作成されている
- [ ] PRが作成されている
- [ ] GitHub Actions CI が実行されている（または対象外でスキップ）
- [ ] PRテンプレートが使用されている

### Antigravity（メインエージェント）の確認
- [ ] 各PRの内容をレビュー
- [ ] CIの結果を確認
- [ ] 問題なければ「LGTM」コメント（マージはしない）

---

## 🧹 テスト後のクリーンアップ

```powershell
# テストブランチの削除（PRをクローズしてから）
git branch -D test/claude-demo
git branch -D test/codex-demo
git branch -D test/gemini-demo
```

---

*作成日: 2026-01-10*
