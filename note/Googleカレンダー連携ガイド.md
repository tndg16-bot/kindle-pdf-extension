# Googleカレンダー連携ガイド

ObsidianでGoogleカレンダーの予定を利用するには、主に以下の2つの方法があります。

## 方法1: プラグインを使用する (推奨)

「Full Calendar」などのプラグインを使用すると、Obsidian内でカレンダーを表示・管理できます。

### 手順1: GoogleカレンダーからiCal URLを取得

1. ブラウザで **Googleカレンダー** を開きます。
2. 左側の「マイカレンダー」から連携したいカレンダーの「︙」をクリックし、**「設定と共有」** を選択します。
3. ページ下部の「カレンダーの統合」セクションまでスクロールします。
4. **「iCal形式の非公開URL」** のURLをコピーします（※「公開URL」ではないので注意）。

### 手順2: Obsidianプラグイン「Full Calendar」の設定

1. Obsidianの **設定 > コミュニティプラグイン** から **Full Calendar** の設定画面を開きます。
2. **「Calendars」** セクションの **「Add Calendar」** ボタンをクリックします。
3. **Calendar Type** で **「iCal」** (または Remote / Network) を選択します。
4. **Calendar Name** に任意の名前（例: `My Google Calendar`）を入力します。
5. **Calendar Url** に、手順1でコピーしたURLを貼り付けます。
6. **Save** をクリックして完了です。

これで、Obsidian上でGoogleカレンダーの予定を閲覧できるようになります（読み取り専用）。

## 方法2: 手動でコピーする (シンプル)

特別な設定をせず、シンプルに運用する方法です。

1.  Googleカレンダーを開きます。
2.  「スケジュール」ビューに切り替えると、リスト形式で予定が表示されコピーしやすくなります。
3.  その日の予定をドラッグして選択し、コピーします。
4.  Obsidianの日記ファイルの「今日のスケジュール」欄に貼り付けます。

## 日記の作成フロー (推奨)

設定が完了しているため、以下の手順で最も簡単に日記を作成できます。

1.  Obsidianの画面左側（リボン）にある **「今日のデイリーノートを開く」** アイコン（カレンダーにチェックマークのアイコン 📅）をクリックします。
2.  自動的に今日のノートが作成され、テンプレート（カレンダー入り）が適用されます。
3.  そのまま振り返りを記入してください。

## 方法3: Pythonスクリプトでノートを自動生成する (上級者向け)

より柔軟に、各予定ごとに個別のObsidianノートを自動作成する方法です。

### 事前準備

1.  **Google Cloud Console** でプロジェクトを作成し、Google Calendar APIを有効化します。
2.  「OAuthクライアントID」を作成し、`credentials.json` をダウンロードします。
3.  このファイルを `Obsidian Vault/papa/scripts/calendar_sync/credentials.json` に配置します。

### セットアップと実行

1.  必要なライブラリをインストールします:
    ```bash
    pip install -r scripts/calendar_sync/requirements.txt
    ```
2.  スクリプトを実行します:
    ```bash
    python scripts/calendar_sync/sync_google_calendar.py
    ```
3.  初回実行時はブラウザが開き、Googleアカウントの認証が求められます。
4.  認証が完了すると、`Calendar/` フォルダ内に予定ごとのノートが作成されます。
