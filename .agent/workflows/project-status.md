---
description: プロジェクトの進捗管理・運用フロー
---

# プロジェクト運用ワークフロー

## 使い方
ユーザーが「/project-status」または「/update-project」と入力したら実行。

---

## 1. 全プロジェクト一覧確認
// turbo
```powershell
gh issue list --repo tndg16-bot/papa --json number,title,state,labels --limit 30
```

---

## 2. 特定プロジェクトの詳細確認
```powershell
gh issue view [Issue番号] --repo tndg16-bot/papa
```

---

## 3. プロジェクトステータス更新

### 進行中に変更（ラベル追加）
```powershell
gh issue edit [Issue番号] --repo tndg16-bot/papa --add-label "in-progress"
```

### 完了（Issueをクローズ）
```powershell
gh issue close [Issue番号] --repo tndg16-bot/papa --comment "完了しました"
```

---

## 4. サブタスクの更新

Issue本文を編集してチェックボックスを更新：
```powershell
gh issue edit [Issue番号] --repo tndg16-bot/papa --body "## タスク`n- [x] 完了したタスク`n- [ ] 未完了タスク"
```

---

## 5. カンバンボード確認
https://github.com/users/tndg16-bot/projects/1

---

## 6. ウェブサイト反映確認
http://localhost:3001 のダッシュボードで最新状態を確認。

---

## ステータス判定ルール
| 条件 | ステータス |
|------|-----------|
| Issue closed | 完了 |
| `in-progress` ラベルあり | 進行中 |
| Issue open（ラベルなし） | 未着手 |
