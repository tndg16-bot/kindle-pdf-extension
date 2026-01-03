# 🛠️ 作成済みツール・プロジェクト一式マニュアル
作成日: 2026-01-01

本セッションで構築した「自動化・効率化ツール」の一覧です。
定期的なメンテナンスや、使い方の確認にご活用ください。

---

## 1. 📅 毎朝の自動処理 (Daily Automation)
**概要**: 何もしなくても、毎朝 05:00 に自動的に実行されます。
**確認方法**: その日の日報 (`daily/YYYY-MM-DD.md`) や各プロジェクト計画書を確認します。

### (1) Googleカレンダー連携
*   **関連ファイル**: `[sync_google_calendar.py](scripts/calendar_sync/sync_google_calendar.py)`
*   **機能**: 今日の予定を取得し、日報にリスト化します。
*   **確認場所**: 日報の `## Google Calendar` セクション。

### (2) プロジェクト進捗自動ログ
*   **関連ファイル**: `[auto_update_progress.py](scripts/project_management/auto_update_progress.py)`
*   **機能**: 全プロジェクトフォルダを巡回し、過去24時間に更新があった場合、計画書に「進行中」ログを追記します。
*   **確認場所**: 各 `Project_Plan.md` の「自動更新ログ」テーブル。

### (3) 名言Bot (BusinessQuoteBot)
*   **関連ファイル**: `[quote_bot.py](BusinessQuoteBot/quote_bot.py)` / `[quotes.json](BusinessQuoteBot/quotes.json)`
*   **機能**: ビジネスの賢人の名言（日本語訳付）をランダムに選び、日報に書き込みます。
*   **確認場所**: 日報の `## Morning Motivation` セクション。

---

## 2. ⚡ 手動で使うツール (On-Demand Tools)
**概要**: デスクトップやエクスプローラーから、必要なタイミングで実行します。

### (4) 新規プロジェクト作成
*   **起動スイッチ**: `Start_New_Project.bat`
*   **いつ使う？**: 「新しいタスクや開発を始めたい！」と思った瞬間。
*   **手順**:
    1.  ファイルをダブルクリック。
    2.  プロジェクト名を入力してEnter。
    3.  自動的にフォルダと `[Project_Plan.md](Templates/Project_Plan.md)` が作成され、Obsidianで開きます。

### (5) アイデア具体化ウィザード
*   **起動スイッチ**: `Start_Idea_Gen.bat`
*   **いつ使う？**: 「ふんわりしたアイデアがあるが、仕様が決まっていない」時。
*   **手順**:
    1.  ファイルをダブルクリック。
    2.  「どんなアプリ？」「誰向け？」などの質問に答える。
    3.  `Idea_Lab` フォルダに「最強のプロンプト」が生成される。
    4.  それをコピーしてAI（ClaudeやChatGPT）に渡すと、仕様書とLP案が出力されます。

### (6) Vault構造診断 (健康診断)
*   **起動コード**: `python scripts/vault_maintenance/check_structure.py`
    *   (※必要であれば `Check_Vault.bat` を作成します)
*   **いつ使う？**: 「ファイルが散らかってきた」「整理したい」と思った時。
*   **手順**:
    1.  スクリプトを実行。
    2.  `[Vault_Maintenance_Report.md](Vault_Maintenance_Report.md)` が生成され、孤立ファイル一覧が表示されます。
