import datetime
import os.path
import sys
import argparse

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pytz

# スコープ
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# 設定
VAULT_ROOT = r"c:/Users/chatg/Obsidian Vault/papa"
DAILY_DIR = os.path.join(VAULT_ROOT, "daily")

def get_calendar_service():
    creds = None
    token_path = 'scripts/calendar_sync/token.json'
    creds_path = 'scripts/calendar_sync/credentials.json'

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                print(f"エラー: {creds_path} が見つかりません。")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

def main():
    parser = argparse.ArgumentParser(description='Sync Google Calendar to Obsidian Daily Note')
    parser.add_argument('--date', type=str, help='Date to sync (YYYY-MM-DD)', default=None)
    args = parser.parse_args()

    service = get_calendar_service()
    if not service:
        return

    # 対象日の決定
    if args.date:
        target_date = datetime.datetime.strptime(args.date, '%Y-%m-%d').date()
    else:
        target_date = datetime.datetime.now().date()

    # タイムゾーン等の設定 (JSTを想定)
    jst = pytz.timezone('Asia/Tokyo')
    
    # 検索範囲の開始と終了
    time_min = datetime.datetime.combine(target_date, datetime.time.min).replace(tzinfo=jst).isoformat()
    time_max = datetime.datetime.combine(target_date, datetime.time.max).replace(tzinfo=jst).isoformat()

    print(f'{target_date} の予定を取得中...')
    events_result = service.events().list(calendarId='primary', timeMin=time_min, timeMax=time_max,
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    # 日報ファイルのパス
    daily_file = os.path.join(DAILY_DIR, f"{target_date.strftime('%Y-%m-%d')}.md")

    # 書き込み内容の作成
    new_section_lines = ["\n## Google Calendar\n"]
    if not events:
        new_section_lines.append("- 予定はありません\n")
    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            # 時刻のみ抽出 (YYYY-MM-DDTHH:MM:SS+09:00 -> HH:MM)
            if 'T' in start:
                time_str = start.split('T')[1][:5]
            else:
                time_str = "全日"
            
            summary = event.get('summary', 'タイトルなし')
            new_section_lines.append(f"- {time_str}: {summary}\n")

    # ファイル処理
    if os.path.exists(daily_file):
        print(f"既存の日報ファイルを更新します: {daily_file}")
        with open(daily_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 既存のセクションを探して置換する
        start_index = -1
        end_index = -1
        
        for i, line in enumerate(lines):
            if line.strip() == "## Google Calendar":
                start_index = i
                break
        
        if start_index != -1:
            # セクションの終わりを探す（次の見出しまたはファイルの終わり）
            for i in range(start_index + 1, len(lines)):
                if lines[i].startswith("## "):
                    end_index = i
                    break
            if end_index == -1:
                end_index = len(lines)
            
            # 置換: 開始位置より前 + 新しいセクション + 終了位置以降
            final_lines = lines[:start_index] + new_section_lines + lines[end_index:]
            # 元のファイルに改行調整が必要かもしれないので確認
            if lines[start_index].startswith('\n'): # 元のセクション前に空行があった場合など
                 pass 
        else:
            # セクションがない場合は末尾に追加
            final_lines = lines + new_section_lines

        with open(daily_file, 'w', encoding='utf-8') as f:
            f.writelines(final_lines)
        print("更新完了しました。")

    else:
        print(f"日報ファイルを新規作成します: {daily_file}")
        with open(daily_file, 'w', encoding='utf-8') as f:
            f.write(f"# {target_date.strftime('%Y-%m-%d')}\n")
            f.writelines(new_section_lines)
        print("新規作成しました。")

if __name__ == '__main__':
    main()
