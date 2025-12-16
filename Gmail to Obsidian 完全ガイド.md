# Gmail to Obsidian 完全ガイド (Dropbox経由)

GmailのメールをMarkdown形式でObsidianに自動保存する方法を説明します。

## 📋 全体の流れ

```
📧 Gmail (Obsidianラベル)
    ↓ Google Apps Script (1時間ごと)
☁️ Dropbox (/Apps/アプリ名/Gmail/)
    ↓ Remotely Save (10分ごと)
📝 Obsidian (Gmailフォルダ)
```

---

## 🎯 準備するもの

- Gmailアカウント
- Dropboxアカウント
- Obsidian

---

## ステップ1: Dropbox App の作成

### 1-1. アプリを作成

1. [Dropbox App Console](https://www.dropbox.com/developers/apps) にアクセス
2. **「Create app」** をクリック
3. 以下を選択:
   - **Choose an API**: `Scoped access`
   - **Choose the type of access**: `App folder` （推奨）
   - **Name your app**: 任意の名前（例: `ObsidianGmail`）
4. **「Create app」** をクリック

### 1-2. 権限を設定

1. **「Permissions」** タブを開く
2. 以下の権限にチェック:
   - ✅ `files.metadata.write`
   - ✅ `files.metadata.read`
   - ✅ `files.content.write`
   - ✅ `files.content.read`
3. **ページ上部の「Submit」ボタンをクリック**（重要！）

### 1-3. アクセストークンを取得

1. **「Settings」** タブに移動
2. 以下の情報をメモ:
   - **App key**: `xxxxxxxxxxxxxxx`
   - **App secret**: `xxxxxxxxxxxxxxx`
3. 下にスクロールして **「OAuth 2」** セクションを探す
4. **「Generated access token」** の **「Generate」** ボタンをクリック
5. 表示されたトークンを**全てコピー**して安全な場所に保存

> **重要**: トークンは `sl.` で始まる長い文字列です。全体をコピーしてください。

---

## ステップ2: Google Apps Script の設定

### 2-1. プロジェクトを作成

1. [Google Apps Script](https://script.google.com/) にアクセス
2. **「新しいプロジェクト」** をクリック
3. プロジェクト名を「Gmail to Dropbox」に変更

### 2-2. コードを貼り付け

エディタの内容を全て削除して、以下のコードを貼り付けます:

```javascript
// ========== 設定項目 ==========
const DROPBOX_ACCESS_TOKEN = 'YOUR_DROPBOX_ACCESS_TOKEN'; // ← ここに実際のトークンを入れる
const GMAIL_LABEL = 'Obsidian'; // Gmailのラベル名
const DROPBOX_FOLDER = '/Gmail'; // Dropbox内の保存先フォルダ
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
  let subject = message.getSubject();
  
  if (!subject || subject.trim() === '') {
    subject = 'NoSubject';
  }
  
  subject = subject
    .replace(/[<>:"/\\|?*]/g, '')
    .replace(/\s+/g, '_')
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

### 2-3. トークンを設定

コードの2行目を編集:
```javascript
const DROPBOX_ACCESS_TOKEN = 'sl.xxxxxxxxxxxxxxxxx'; // ← 実際のトークンを貼り付け
```

**保存** (Ctrl+S) します。

### 2-4. 動作テスト

1. Gmailで **`Obsidian`** ラベルを作成
2. テスト用のメールに `Obsidian` ラベルを付ける
3. Google Apps Script で **「実行」** → `saveGmailToDropbox` を選択
4. 初回は権限の確認が必要:
   - **「権限を確認」** → アカウント選択
   - **「詳細」** → **「(プロジェクト名)に移動」** → **「許可」**
5. 実行ログで「保存しました: ファイル名.md」と表示されればOK

### 2-5. 定期実行トリガーを設定

1. 左側のメニューから **「トリガー」** (⏰) をクリック
2. **「トリガーを追加」** をクリック
3. 設定:
   - 実行する関数: `saveGmailToDropbox`
   - イベントのソース: **時間主導型**
   - 時間ベースのトリガーのタイプ: **時間ベースのタイマー**
   - 時間の間隔: **1時間おき**
4. **「保存」**

---

## ステップ3: Obsidian の設定 (Remotely Save)

### 3-1. プラグインをインストール

1. Obsidianを開く
2. **設定** (⚙️) → **コミュニティプラグイン**
3. 「セーフモードをオフにする」（初回のみ）
4. **「閲覧」** → `Remotely Save` を検索
5. **「インストール」** → **「有効化」**

### 3-2. Dropbox と連携

1. **設定** → **Remotely Save**
2. **「Choose a remote service」**: `Dropbox` を選択
3. 以下を入力（ステップ1-3でメモした情報）:
   - **App key**: Dropboxアプリの App key
   - **App secret**: Dropboxアプリの App secret
4. **「Auth」** ボタンをクリック
5. ブラウザが開くので、Dropboxで **「許可」**
6. 表示された認証コードをコピー
7. Obsidianに戻り、認証コードを貼り付け
8. **「Check」** をクリック

### 3-3. 同期設定

1. **Auto run every X minutes**: `10` （10分ごとに自動同期）
2. **Run once on startup**: ✅ ON
3. **「Save」** をクリック

### 3-4. 初回同期

1. 左側のサイドバーの **Remotely Save** アイコンをクリック
2. **「Sync」** をクリック
3. 同期完了後、`Gmail` フォルダが表示される

---

## ✅ 完成！

### 使い方

1. **Gmailで保存したいメールに `Obsidian` ラベルを付ける**
2. **1時間以内に自動的にDropboxに保存される**
3. **10分以内にObsidianに同期される**

### Gmail フィルタで自動化（オプション）

特定の送信者からのメールを自動保存:

1. Gmail **設定** → **フィルタとブロック中のアドレス**
2. **新しいフィルタを作成**
3. 条件を設定（例: `from:newsletter@example.com`）
4. **ラベルを付ける**: `Obsidian`
5. **フィルタを作成**

---

## 🆘 トラブルシューティング

### GASでエラーが出る

**エラー**: `The given OAuth 2 access token is malformed`
- **解決**: Dropbox App の権限設定後、新しいトークンを生成

**エラー**: `files.content.write` の権限がない
- **解決**: Dropbox App の Permissions タブで権限を追加し、**Submit** を押す

### Obsidianに同期されない

- Remotely Save で手動同期を試す
- Dropbox Web で `/Apps/アプリ名/Gmail/` にファイルがあるか確認
- Remotely Save の同期ログを確認

### ファイルが重複する

- `Obsidian/Processed` ラベルが正しく付いているか確認
- GASの実行ログを確認

---

## 📚 保存されるファイルの形式

```markdown
---
title: メールの件名
from: 送信者のメールアドレス
date: 2025-12-14 19:00:00
source: Gmail
tags: [clipping, email]
---

# メールの件名

**From:** 送信者のメールアドレス  
**Date:** 2025-12-14 19:00:00

---

メール本文がここに入ります...
```

ファイル名: `20251214-190000_メールの件名.md`
