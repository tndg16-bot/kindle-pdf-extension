# Obsidian × Dropbox 連携設定ガイド

ObsidianとDropboxを連携させる方法を説明します。Googleドライブの代わりにDropboxを使用することで、より安定した同期が可能になります。

## 📋 目次

1. [方法1: Remotely Save プラグイン (推奨)](#方法1-remotely-save-プラグイン-推奨)
2. [方法2: Obsidian Vault を Dropbox フォルダに配置](#方法2-obsidian-vault-を-dropbox-フォルダに配置)
3. [Gmail to Obsidian の Dropbox 対応](#gmail-to-obsidian-の-dropbox-対応)

---

## 方法1: Remotely Save プラグイン (推奨)

`Remotely Save` プラグインは、Dropbox、OneDrive、S3などの複数のクラウドストレージに対応しています。

### ステップ 1: Dropbox アプリの作成

1. [Dropbox App Console](https://www.dropbox.com/developers/apps) にアクセスします
2. **「Create app」** をクリックします
3. 以下の設定を選択します:
   - **Choose an API**: `Scoped access`
   - **Choose the type of access**: `App folder` (推奨) または `Full Dropbox`
     - `App folder`: Dropboxの専用フォルダ内のみアクセス (安全)
     - `Full Dropbox`: Dropbox全体にアクセス
   - **Name your app**: 任意の名前 (例: `ObsidianSync`)
4. **「Create app」** をクリックします

### ステップ 2: アプリの設定

1. 作成したアプリの設定ページで、**「Permissions」** タブを開きます
2. 以下の権限を有効にします:
   - ✅ `files.metadata.write`
   - ✅ `files.metadata.read`
   - ✅ `files.content.write`
   - ✅ `files.content.read`
3. **「Submit」** をクリックして権限を保存します

4. **「Settings」** タブに戻り、以下の情報をメモします:
   - **App key** (後で使用します)
   - **App secret** (後で使用します)

### ステップ 3: Obsidian プラグインのインストール

1. Obsidianを開きます
2. **設定** (⚙️) → **コミュニティプラグイン** を開きます
3. 「セーフモードをオフにする」をクリック (初回のみ)
4. **「閲覧」** をクリックして、`Remotely Save` を検索します
5. **「インストール」** → **「有効化」** をクリックします

### ステップ 4: Remotely Save の設定

1. **設定** → **Remotely Save** を開きます
2. **「Choose a remote service」** で `Dropbox` を選択します
3. 先ほどメモした情報を入力します:
   - **App key**: Dropboxアプリの App key
   - **App secret**: Dropboxアプリの App secret
4. **「Auth」** ボタンをクリックします
5. ブラウザが開き、Dropboxの認証画面が表示されます
6. **「許可」** をクリックします
7. 認証コードが表示されるので、コピーしてObsidianに貼り付けます
8. **「Check」** ボタンをクリックして接続を確認します

### ステップ 5: 同期設定

1. 同期の設定を行います:
   - **Auto run every X minutes**: 自動同期の間隔 (例: `10` 分)
   - **Run once on startup**: 起動時に同期 (推奨: ON)
2. **「Save」** をクリックします

### ステップ 6: 初回同期

1. 左側のサイドバーにある **Remotely Save** アイコンをクリックします
2. **「Sync」** ボタンをクリックして初回同期を実行します
3. 同期が完了すると、Dropboxに Vault の内容がアップロードされます

---

## 方法2: Obsidian Vault を Dropbox フォルダに配置

この方法は最もシンプルですが、複数デバイスで同時編集する場合は競合が発生する可能性があります。

### ステップ 1: Dropbox のインストール

1. [Dropbox デスクトップアプリ](https://www.dropbox.com/install) をダウンロードしてインストールします
2. Dropboxにログインします

### ステップ 2: Vault の移動

#### 既存の Vault を移動する場合:

1. Obsidianを閉じます
2. 現在の Vault フォルダ (例: `c:\Users\chatg\Obsidian Vault\papa`) を Dropbox フォルダにコピーまたは移動します
   - 移動先例: `C:\Users\chatg\Dropbox\Obsidian\papa`
3. Obsidianを開きます
4. **「Open folder as vault」** をクリックして、Dropbox内の新しい場所を選択します

#### 新しい Vault を作成する場合:

1. Obsidianを開きます
2. **「Create new vault」** をクリックします
3. **「Vault name」**: 任意の名前
4. **「Location」**: Dropbox フォルダ内のパス (例: `C:\Users\chatg\Dropbox\Obsidian`)
5. **「Create」** をクリックします

### ステップ 3: 他のデバイスでの設定

1. 他のデバイスでもDropboxをインストールして同期します
2. Obsidianをインストールします
3. **「Open folder as vault」** で、Dropbox内の Vault フォルダを開きます

> **⚠️ 注意**: この方法では、複数デバイスで同時に編集すると競合ファイルが作成される可能性があります。同時編集を避けるか、方法1の `Remotely Save` を使用することを推奨します。

---

## Gmail to Obsidian の Dropbox 対応

Gmail のメールを Dropbox 経由で Obsidian に保存する方法です。

### 前提条件

- Dropbox アカウント
- Google Apps Script の基本的な知識

### ステップ 1: Dropbox アプリの作成 (方法1と同じ)

上記の「方法1: ステップ 1-2」を参照して、Dropbox アプリを作成し、App key と App secret を取得します。

### ステップ 2: Dropbox Access Token の取得

1. [Dropbox App Console](https://www.dropbox.com/developers/apps) で作成したアプリを開きます
2. **「Settings」** タブで、**「Generated access token」** セクションを探します
3. **「Generate」** ボタンをクリックしてアクセストークンを生成します
4. 生成されたトークンをコピーして安全な場所に保存します

> **🔒 重要**: このアクセストークンは秘密情報です。他人と共有しないでください。

### ステップ 3: Google Apps Script の作成

1. [script.google.com](https://script.google.com/) にアクセスします
2. **「新しいプロジェクト」** をクリックします
3. プロジェクト名を「Gmail to Dropbox」などに変更します
4. 以下のコードを貼り付けます:

```javascript
// ========== 設定項目 ==========
const DROPBOX_ACCESS_TOKEN = 'YOUR_DROPBOX_ACCESS_TOKEN'; // Dropboxのアクセストークン
const GMAIL_LABEL = 'Obsidian'; // Gmailのラベル名
const DROPBOX_FOLDER = '/Clippings'; // Dropbox内の保存先フォルダ
const PROCESSED_LABEL = 'Obsidian/Processed'; // 処理済みラベル

// ========== メイン関数 ==========
function saveGmailToDropbox() {
  const label = GmailApp.getUserLabelByName(GMAIL_LABEL);
  if (!label) {
    Logger.log(`ラベル "${GMAIL_LABEL}" が見つかりません。`);
    return;
  }
  
  const processedLabel = getOrCreateLabel(PROCESSED_LABEL);
  const threads = label.getThreads();
  Logger.log(`${threads.length} 件のスレッドを処理します。`);
  
  threads.forEach(thread => {
    if (hasLabel(thread, processedLabel)) {
      return;
    }
    
    const messages = thread.getMessages();
    messages.forEach(message => {
      try {
        const markdown = convertToMarkdown(message);
        const fileName = generateFileName(message);
        uploadToDropbox(fileName, markdown);
        Logger.log(`保存しました: ${fileName}`);
      } catch (e) {
        Logger.log(`エラー: ${e.message}`);
      }
    });
    
    thread.addLabel(processedLabel);
  });
}

// ========== Dropbox アップロード関数 ==========
function uploadToDropbox(fileName, content) {
  const url = 'https://content.dropboxapi.com/2/files/upload';
  const path = `${DROPBOX_FOLDER}/${fileName}`;
  
  const headers = {
    'Authorization': `Bearer ${DROPBOX_ACCESS_TOKEN}`,
    'Content-Type': 'application/octet-stream',
    'Dropbox-API-Arg': JSON.stringify({
      'path': path,
      'mode': 'overwrite',
      'autorename': true,
      'mute': false
    })
  };
  
  const options = {
    'method': 'post',
    'headers': headers,
    'payload': content,
    'muteHttpExceptions': true
  };
  
  const response = UrlFetchApp.fetch(url, options);
  if (response.getResponseCode() !== 200) {
    throw new Error(`Dropbox upload failed: ${response.getContentText()}`);
  }
}

// ========== Markdown 変換関数 ==========
function convertToMarkdown(message) {
  const subject = message.getSubject();
  const from = message.getFrom();
  const date = Utilities.formatDate(message.getDate(), 'Asia/Tokyo', 'yyyy-MM-dd HH:mm:ss');
  const body = message.getPlainBody();
  
  let markdown = `---\n`;
  markdown += `title: ${subject}\n`;
  markdown += `from: ${from}\n`;
  markdown += `date: ${date}\n`;
  markdown += `source: Gmail\n`;
  markdown += `tags: [clipping, email]\n`;
  markdown += `---\n\n`;
  markdown += `# ${subject}\n\n`;
  markdown += `**From:** ${from}  \n`;
  markdown += `**Date:** ${date}\n\n`;
  markdown += `---\n\n`;
  markdown += body;
  
  return markdown;
}

// ========== ファイル名生成関数 ==========
function generateFileName(message) {
  const date = Utilities.formatDate(message.getDate(), 'Asia/Tokyo', 'yyyyMMdd-HHmmss');
  const subject = message.getSubject()
    .replace(/[<>:"/\\|?*]/g, '')
    .substring(0, 50);
  return `${date}_${subject}.md`;
}

// ========== ヘルパー関数 ==========
function getOrCreateLabel(labelName) {
  let label = GmailApp.getUserLabelByName(labelName);
  if (!label) {
    label = GmailApp.createLabel(labelName);
  }
  return label;
}

function hasLabel(thread, label) {
  const labels = thread.getLabels();
  return labels.some(l => l.getName() === label.getName());
}
```

5. **重要**: `YOUR_DROPBOX_ACCESS_TOKEN` を実際のアクセストークンに置き換えます
6. 必要に応じて `DROPBOX_FOLDER` を変更します
7. **保存** (Ctrl+S) します

### ステップ 4: 動作テスト

1. Gmailで `Obsidian` ラベルを作成し、テスト用のメールにラベルを付けます
2. Google Apps Script で `saveGmailToDropbox` を実行します
3. 初回実行時は権限の確認が必要です
4. Dropboxで該当フォルダを確認し、.mdファイルが作成されていることを確認します

### ステップ 5: 定期実行の設定

1. **「トリガー」** → **「トリガーを追加」** をクリックします
2. 設定:
   - 実行する関数: `saveGmailToDropbox`
   - イベントのソース: **時間主導型**
   - 時間の間隔: **1時間おき**
3. **「保存」** をクリックします

---

## 🎯 まとめ

### 推奨構成

- **同期方法**: 方法1 (Remotely Save プラグイン)
- **Gmail連携**: Dropbox API + Google Apps Script

### メリット

✅ Googleドライブより安定した同期  
✅ 複数デバイス間での自動同期  
✅ 競合の自動解決 (Remotely Save使用時)  
✅ バージョン履歴の保持

### 注意点

⚠️ Dropboxの無料プランは容量制限があります (2GB)  
⚠️ アクセストークンは安全に管理してください  
⚠️ 複数デバイスで同時編集する場合は Remotely Save を推奨

---

## 🆘 トラブルシューティング

### Remotely Save で認証エラーが出る
- App key と App secret が正しいか確認
- Dropbox アプリの権限設定を確認

### Google Apps Script でアップロードエラーが出る
- アクセストークンが正しいか確認
- Dropbox フォルダのパスが正しいか確認

### ファイルが同期されない
- Remotely Save の同期ログを確認
- インターネット接続を確認
