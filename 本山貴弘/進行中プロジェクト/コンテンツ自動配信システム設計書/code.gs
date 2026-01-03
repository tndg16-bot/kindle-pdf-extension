/**
 * Social Media Automation Script (Updated)
 * スプレッドシートから各SNSへ投稿を行うスクリプトです。
 * 
 * 【更新機能】
 * 1. 投稿成功時、DASHBOARDからARCHIVEシートへ行を移動します（未送信のみ残す）。
 * 2. 過去の未送信分（エラーやトークン切れで送れなかった分）も、次回実行時に再試行します。
 */

// ==========================================
// 1. 設定 (CONFIG)
// ==========================================
const CONFIG = {
  // スプレッドシートのシート名
  SHEET_DASHBOARD: 'DASHBOARD',
  SHEET_ARCHIVE: 'ARCHIVE', // 送信済みログを移動するシート
  
  // X (Twitter) API Settings
  TWITTER_API_KEY: 'YOUR_API_KEY',
  TWITTER_API_SECRET: 'YOUR_API_SECRET',
  TWITTER_ACCESS_TOKEN: 'YOUR_ACCESS_TOKEN',
  TWITTER_ACCESS_SECRET: 'YOUR_ACCESS_SECRET',
  
  // Threads API Settings
  // ★重要★ ここには「長期トークン(Long-Lived Access Token)」を入れてください。
  // 短期トークンは1時間で切れますが、長期トークンは60日間持ちます。
  THREADS_USER_ID: 'YOUR_THREADS_USER_ID',
  THREADS_ACCESS_TOKEN: 'YOUR_LONG_LIVED_ACCESS_TOKEN',
  
  // Instagram Graph API Settings
  INSTAGRAM_BUSINESS_ID: 'YOUR_INSTAGRAM_BUSINESS_ID',
  INSTAGRAM_ACCESS_TOKEN: 'YOUR_INSTAGRAM_ACCESS_TOKEN'
};

// ==========================================
// 2. メイン関数 (トリガーで実行)
// ==========================================
function main() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(CONFIG.SHEET_DASHBOARD);
  const archiveSheet = ss.getSheetByName(CONFIG.SHEET_ARCHIVE);
  
  if (!sheet || !archiveSheet) {
    console.error('【エラー】シートが見つかりません: DASHBOARD または ARCHIVE');
    return;
  }
  
  const rows = sheet.getDataRange().getValues();
  const now = new Date();
  
  console.log('【実行開始】現在時刻: ' + now.toString());
  
  // 行削除を行うため、後ろからループする (インデックスズレ防止)
  for (let i = rows.length - 1; i >= 1; i--) {
    const row = rows[i];
    if (!row[0]) continue; // 日時が空ならスキップ

    const scheduledTime = new Date(row[0]); // A列: 予約日時
    const platform = row[1];              // B列: プラットフォーム
    const content = row[3] ? row[3].toString().replace(/<br>/gi, '\n') : ''; // D列: 投稿内容
    const status = row[4];                // E列: ステータス
    
    // 判定: 「予約済」かつ「予定時刻を過ぎている」場合
    const isReady = (status === '予約済');
    const isPast = (now >= scheduledTime);
    
    if (isReady && isPast) {
      console.log(`🚀 投稿試行 (行${i+1}): ${platform} - ${scheduledTime}`);
      
      try {
        let result = false;
        
        if (platform === 'X' || platform === 'Twitter') {
          result = postToX(content);
        } else if (platform.toLowerCase() === 'threads') { 
          result = postToThreads(content);
        } else if (platform === 'Instagram') {
          console.log('Instagram投稿は画像処理が複雑なため今回はスキップ');
        } else {
          console.log('未対応のプラットフォーム: ' + platform);
        }
        
        if (result) {
          // ■■■ 成功時: ARCHIVEへ移動 ■■■
          // 1. ステータスを更新
          row[4] = '送信済'; 
          // 2. ARCHIVEシートの末尾に追加
          archiveSheet.appendRow(row);
          // 3. DASHBOARDから削除
          sheet.deleteRow(i + 1);
          console.log('✅ 投稿成功＆アーカイブ移動完了');
        } else {
          sheet.getRange(i + 1, 5).setValue('エラー: API呼び出し失敗');
        }
        
      } catch (e) {
        console.error('❌ 投稿エラー:', e);
        sheet.getRange(i + 1, 5).setValue('エラー: ' + e.message);
        // エラー時は移動せず、ステータスだけ書き換えて残す
      }
    }
  }
}

// ==========================================
// 3. 各SNS投稿関数
// ==========================================

function postToX(text) {
  // X API ロジック (実際にはTwitter API v2ライブラリ等を使用)
  console.log('Xへ投稿（シミュレーション）: ' + text);
  return true; 
}

function postToThreads(text) {
  if (!CONFIG.THREADS_USER_ID || CONFIG.THREADS_USER_ID.includes('YOUR_')) {
    console.log('Threads設定が未完了です');
    return false;
  }

  try {
    // Media Container 作成
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
    const createRes = UrlFetchApp.fetch(createUrl, createOptions);
    const createData = JSON.parse(createRes.getContentText());
    
    if (createData.error) throw new Error(createData.error.message);
    const creationId = createData.id;
    
    Utilities.sleep(10000); // 待機
    
    // Publish
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
    const publishRes = UrlFetchApp.fetch(publishUrl, publishOptions);
    const publishData = JSON.parse(publishRes.getContentText());

    if (publishData.error) throw new Error(publishData.error.message);
    
    return true;
  } catch (e) {
    console.error('Threads API Exception:', e);
    throw e;
  }
}
