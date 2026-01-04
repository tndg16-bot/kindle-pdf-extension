# 📋 要件定義書: [プロジェクト/機能名]
**Status**: Draft | **Owner**: Antigravity | **Dev**: Claude Code

---

## 1. 🎯 ゴール (Goal)
*何を作るのか、一言で記述してください。*
> 例：現在時刻を表示し、ポモドーロタイマーとしても機能するシンプルなWebアプリ。

## 2. 👤 ユーザーストーリー (User Story)
*誰が、何のために、どう使うのか？*
*   **As a (誰が)**: 日々のタスクに集中したいユーザーが
*   **I want to (何をしたい)**: ブラウザ上で手軽にポモドーロタイマーを設定・開始したい
*   **So that (その結果)**: 別途アプリを開く手間なく、集中時間を管理できる

## 3. ✅ 完了条件 (Acceptance Criteria / TDD)
*AIが「完了した」と判断するための具体的なテスト項目。これを元にテストコードを書きます。*

### 必須機能 (Must Have)
- [ ] [UI] 画面中央に「25:00」からカウントダウンするタイマーが表示される
- [ ] [UI] 「Start」「Stop」「Reset」ボタンが存在する
- [ ] [Logic] Startボタン押下でカウントダウンが始まる (1秒ごとに減る)
- [ ] [Logic] 0になったら「Time's up!」とアラートが出る（または音が鳴る）

### 推奨機能 (Nice to Have)
- [ ] タイマー時間のカスタマイズ機能 (25分 / 5分)
- [ ] ブラウザタブのタイトルに残り時間を表示

## 4. 🛠️ 技術スタック & 制約 (Technical Constraints)
*   **Frontend**: HTML, CSS (Vanilla), JavaScript (Vanilla)
*   **Framework**: なし（シンプルな構成）
*   **Design**: モダンでミニマルなデザイン (Dark Mode対応)
*   **Testing**: Playwright (E2Eテスト)

---

## 📝 Antigravity Memo (PM Note)
*ここにはAntigravityが補足情報を記載します。*
