---
description: 新規プロジェクトをGitHub Issueとして登録する
---

# 新規プロジェクト登録ワークフロー

## 使い方
ユーザーが「/new-project」と入力したら、このワークフローを実行します。

## 手順

### 1. ヒアリング
ユーザーに以下を確認：
- プロジェクト名
- 目的・背景
- 具体的なサブタスク（3-10個程度）

### 2. 壁打ち（必要に応じて）
プロジェクトの目的を整理し、タスクを洗い出す。

### 3. M番号の決定
// turbo
既存のIssueを確認して次のM番号を決定：
```powershell
gh issue list --repo tndg16-bot/papa --json number,title | ConvertFrom-Json | Where-Object { $_.title -match '^\[M\d+\]' } | ForEach-Object { $_.title }
```

### 4. Issue作成
// turbo
サブタスクをチェックリスト形式で本文に含めて作成：
```powershell
gh issue create --repo tndg16-bot/papa --title "[M番号] プロジェクト名" --body "## 概要`n説明`n`n## タスク`n- [ ] サブタスク1`n- [ ] サブタスク2`n- [ ] サブタスク3" --label "ラベル名"
```

### 5. 確認
// turbo
作成されたIssueを確認：
```powershell
gh issue view [Issue番号] --repo tndg16-bot/papa
```

### 6. ウェブサイト反映確認
http://localhost:3001 のダッシュボードにプロジェクトが表示されることを確認。

---

## ラベル一覧
- `coaching` - コーチングセッション関連
- `ai-business` - AI副業関連
- `infra` - インフラ・ワークフロー関連
- `portfolio` - ポートフォリオサイト関連
