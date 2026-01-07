// タスクの入力データ型
export interface TaskInput {
  title: string; // タスク名
  deadline: string; // 期限（ISO 8601形式: 2025-12-15T14:00:00）
  duration: number; // 所要時間（時間単位）
}

// Google Calendar イベント型
export interface CalendarEvent {
  summary: string; // イベント名
  start: {
    dateTime: string; // 開始日時
    timeZone: string; // タイムゾーン
  };
  end: {
    dateTime: string; // 終了日時
    timeZone: string; // タイムゾーン
  };
}

// Google Tasks タスク型
export interface GoogleTask {
  title: string; // タスク名
  due: string; // 期限（RFC 3339形式）
}

// 認証状態
export interface AuthState {
  isSignedIn: boolean; // ログイン状態
  user: {
    name: string;
    email: string;
    imageUrl?: string;
  } | null;
}
