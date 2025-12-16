/**
 * Social Media Automation Script
 * スプレッドシートから各SNSへ投稿を行うスクリプトです。
 */

// ==========================================
// 1. 設定 (CONFIG)
// ==========================================
const CONFIG = {
  // スプレッドシートのシート名
  SHEET_DASHBOARD: 'DASHBOARD',
  
  // X (Twitter) API Settings
  TWITTER_API_KEY: 'YOUR_API_KEY',
  TWITTER_API_SECRET: 'YOUR_API_SECRET',
  TWITTER_ACCESS_TOKEN: 'YOUR_ACCESS_TOKEN',
  TWITTER_ACCESS_SECRET: 'YOUR_ACCESS_SECRET',
  
  // Threads API Settings
  THREADS_USER_ID: '25414010094899552',
  THREADS_ACCESS_TOKEN: 'THAAWKYys4UaFBUVNjd0R2cFpTbDJTUW9PTWJFUDh4ZA3d4Q3h5X19oZAVZAXdll1TWhuZAmFRQ0RLVG93Y0dBcDVHMk1sRmk1bS1kUEZA3a2w5cGNuZAEFqVzhGR0dWQ1ZATTnJYQUdRTmc2UVhkZA3RRbFVQSG0xUU1kZAXpUTEljeUhxQ0VjZAjdqYVh0Q2tkZAUJOZAldpMjhuNzdXc1ZARekZAyY1VlZAkc5QWEZD',
  
  // Instagram Graph API Settings
  INSTAGRAM_BUSINESS_ID: 'YOUR_INSTAGRAM_BUSINESS_ID',
  INSTAGRAM_ACCESS_TOKEN: 'YOUR_INSTAGRAM_ACCESS_TOKEN'
};

// ==========================================
// 2. メイン関数 (トリガーで実行)
// ==========================================
function main() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_DASHBOARD);
  if (!sheet) {
    console.error('【エラー】シートが見つかりません: ' + CONFIG.SHEET_DASHBOARD);
    return;
  }
  const rows = sheet.getDataRange().getValues();
  const now = new Date();
  
  console.log('【実行開始】現在時刻: ' + now.toString());
  console.log('取得行数: ' + rows.length);

  // 1行目はヘッダーなのでスキップ
  for (let i = 1; i < rows.length; i++) {
    const row = rows[i];
    if (!row[0]) continue; // 日時が空ならスキップ

    const scheduledTime = new Date(row[0]); // A列: 予約日時
    const platform = row[1];              // B列: プラットフォーム
    const content = row[3] ? row[3].toString().replace(/<br>/gi, '\n') : ''; // D列: 投稿内容
    const status = row[4];                // E列: ステータス
    
    // 詳細ログを出力 (デバッグ用)
    const isReady = (status === '予約済');
    const isPast = (now >= scheduledTime);
    
    if (status === '送信済' || status === 'エラー') {
        continue; // 処理済みはログ出さない
    }

    console.log(`行${i+1} チェック: ステータス=[${status}], 予定=[${scheduledTime}], 判定: ${isReady && isPast ? 'GO' : 'SKIP'}`);

    // 投稿条件チェック
    if (isReady && isPast) {
      try {
        let result = false;
        console.log(`🚀 投稿試行: ${platform}`);
        
        if (platform === 'X' || platform === 'Twitter') {
          result = postToX(content);
        } else if (platform.toLowerCase() === 'threads') { 
          result = postToThreads(content);
        } else if (platform === 'Instagram') {
          console.log('Instagram投稿は画像が必要です。スキップします。');
        } else {
          console.log('未対応のプラットフォーム: ' + platform);
        }
        
        if (result) {
          sheet.getRange(i + 1, 5).setValue('送信済');
          console.log('✅ 投稿成功: ' + platform);
        } else {
          sheet.getRange(i + 1, 5).setValue('エラー');
        }
        
      } catch (e) {
        console.error('❌ 投稿エラー:', e);
        sheet.getRange(i + 1, 5).setValue('エラー: ' + e.message);
      }
    } else {
        if (isReady && !isPast) console.log(`  -> まだ時間ではありません (現在: ${now} < 予定: ${scheduledTime})`);
        if (!isReady) console.log(`  -> ステータスが「予約済」ではありません`);
    }
  }
}

// ==========================================
// 3. 各SNS投稿関数
// ==========================================

/**
 * X (Twitter) への投稿
 */
function postToX(text) {
  // 簡易シミュレーション
  console.log('Xへ投稿（シミュレーション）: ' + text);
  return true; 
}

/**
 * Threads への投稿
 */
function postToThreads(text) {
  // 修正: 実際のIDが入っている場合にエラーにならないよう条件を変更
  if (!CONFIG.THREADS_USER_ID || CONFIG.THREADS_USER_ID === 'YOUR_THREADS_USER_ID') {
    console.log('Threads設定が未完了です');
    return false;
  }

  try {
    // Step 1: Create a Media Container (Text thread)
    const createUrl = `https://graph.threads.net/v1.0/${CONFIG.THREADS_USER_ID}/threads`;
    const createPayload = {
      'media_type': 'TEXT',
      'text': text,
      'access_token': CONFIG.THREADS_ACCESS_TOKEN
    };
    
    const createOptions = {
      'method': 'post',
      'payload': createPayload,
      'muteHttpExceptions': true
    };
    
    const createResponse = UrlFetchApp.fetch(createUrl, createOptions);
    const createData = JSON.parse(createResponse.getContentText());
    
    if (createData.error) {
      console.error('Threads作成エラー:', createData.error);
      throw new Error(createData.error.message);
    }
    
    const creationId = createData.id;
    console.log('Step 1完了: Container ID = ' + creationId);
    
    // 待機時間 (APIの反映待ち)
    console.log('⏳ 反映待ち... (10秒)');
    Utilities.sleep(10000);
    
    // Step 2: Publish the Container
    const publishUrl = `https://graph.threads.net/v1.0/${CONFIG.THREADS_USER_ID}/threads_publish`;
    const publishPayload = {
      'creation_id': creationId,
      'access_token': CONFIG.THREADS_ACCESS_TOKEN
    };
    
    const publishOptions = {
      'method': 'post',
      'payload': publishPayload,
      'muteHttpExceptions': true
    };
    
    const publishResponse = UrlFetchApp.fetch(publishUrl, publishOptions);
    const publishData = JSON.parse(publishResponse.getContentText());

    if (publishData.error) {
      console.error('Threads公開エラー:', publishData.error);
      throw new Error(publishData.error.message);
    }
    
    console.log('Threadsへ投稿完了 ID: ' + publishData.id);
    return true;
  } catch (e) {
    console.error('Threads API Exception:', e);
    throw e;
  }
}

// ==========================================
// 4. デバッグ用関数 (うまくいかない時用)
// ==========================================
function debugSpreadsheet() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_DASHBOARD);
  if (!sheet) {
    console.error('【エラー】シートが見つかりません: ' + CONFIG.SHEET_DASHBOARD);
    return;
  }
  const rows = sheet.getDataRange().getValues();
  console.log('【デバッグ開始】全 ' + rows.length + ' 行を取得しました。2行目からチェックします。');
  
  const now = new Date();
  console.log('現在時刻 (GAS): ' + now.toString());

  for (let i = 1; i < rows.length; i++) {
    const row = rows[i];
    const dateVal = row[0];
    const status = row[4];
    
    // 日付チェック
    let dateLog = '日時: ';
    if (dateVal instanceof Date) {
        dateLog += dateVal.toString();
    } else {
        dateLog += dateVal + ' (文字または未入力)';
    }

    // 判定ロジックのシミュレーション
    const isReady = (status === '予約済');
    const isPast = (dateVal instanceof Date) && (now >= dateVal);
    
    console.log(
      '行' + (i + 1) + ': ' + 
      'ステータス=[' + status + '] (' + (isReady ? 'OK' : 'NG') + '), ' +
      dateLog + ' (' + (isPast ? '過去/現在OK' : '未来NG') + ')'
    );
  }
}
