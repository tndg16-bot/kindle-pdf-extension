import type { CalendarEvent, GoogleTask } from '../types';

// Google API設定
const CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;
const API_KEY = import.meta.env.VITE_GOOGLE_API_KEY;
const DISCOVERY_DOCS = [
  'https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest',
  'https://www.googleapis.com/discovery/v1/apis/tasks/v1/rest',
];
const SCOPES = 'https://www.googleapis.com/auth/calendar.events https://www.googleapis.com/auth/tasks';

/**
 * gapiが読み込まれるまで待機
 */
const waitForGapi = (): Promise<void> => {
  return new Promise((resolve, reject) => {
    let attempts = 0;
    const maxAttempts = 50; // 5秒間待機

    const checkGapi = () => {
      if (typeof gapi !== 'undefined') {
        resolve();
      } else if (attempts >= maxAttempts) {
        reject(new Error('Google APIの読み込みに失敗しました。ページをリロードしてください。'));
      } else {
        attempts++;
        setTimeout(checkGapi, 100);
      }
    };

    checkGapi();
  });
};

/**
 * Google APIクライアントを初期化
 */
export const initGoogleApi = (): Promise<void> => {
  return new Promise(async (resolve, reject) => {
    try {
      // gapiが読み込まれるまで待機
      await waitForGapi();

      gapi.load('client:auth2', async () => {
        try {
          await gapi.client.init({
            apiKey: API_KEY,
            clientId: CLIENT_ID,
            discoveryDocs: DISCOVERY_DOCS,
            scope: SCOPES,
          });
          console.log('Google API initialized successfully');
          resolve();
        } catch (error) {
          console.error('gapi.client.init failed:', error);
          reject(error);
        }
      });
    } catch (error) {
      reject(error);
    }
  });
};


/**
 * ログイン状態を取得
 */
export const isSignedIn = (): boolean => {
  return gapi.auth2.getAuthInstance().isSignedIn.get();
};

/**
 * サインイン
 */
export const signIn = async (): Promise<void> => {
  await gapi.auth2.getAuthInstance().signIn();
};

/**
 * サインアウト
 */
export const signOut = async (): Promise<void> => {
  await gapi.auth2.getAuthInstance().signOut();
};

/**
 * 現在のユーザー情報を取得
 */
export const getCurrentUser = () => {
  if (!isSignedIn()) return null;

  const user = gapi.auth2.getAuthInstance().currentUser.get();
  const profile = user.getBasicProfile();

  return {
    name: profile.getName(),
    email: profile.getEmail(),
    imageUrl: profile.getImageUrl(),
  };
};

/**
 * Google Calendarにイベントを作成
 */
export const createCalendarEvent = async (event: CalendarEvent): Promise<any> => {
  try {
    const response = await gapi.client.calendar.events.insert({
      calendarId: 'primary',
      resource: event,
    });
    return response.result;
  } catch (error) {
    console.error('Error creating calendar event:', error);
    throw error;
  }
};

/**
 * Google Tasksにタスクを作成
 */
export const createTask = async (task: GoogleTask): Promise<any> => {
  try {
    // まず、デフォルトのタスクリストを取得
    const taskListsResponse = await gapi.client.tasks.tasklists.list();
    const defaultTaskList = taskListsResponse.result.items?.[0]?.id;

    if (!defaultTaskList) {
      throw new Error('No task list found');
    }

    // タスクを作成
    const response = await gapi.client.tasks.tasks.insert({
      tasklist: defaultTaskList,
      resource: task,
    });
    return response.result;
  } catch (error) {
    console.error('Error creating task:', error);
    throw error;
  }
};

/**
 * タスクをCalendarとTasksの両方に登録
 * @param title タスク名
 * @param deadline 期限（ISO 8601形式）
 * @param duration 所要時間（時間単位）
 */
export const createTaskBoth = async (
  title: string,
  deadline: string,
  duration: number
): Promise<{ calendar: any; task: any }> => {
  // 開始時刻と終了時刻を計算
  const startTime = new Date(deadline);
  const endTime = new Date(startTime.getTime() + duration * 60 * 60 * 1000);

  // Calendarイベント作成
  const calendarEvent: CalendarEvent = {
    summary: title,
    start: {
      dateTime: startTime.toISOString(),
      timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    },
    end: {
      dateTime: endTime.toISOString(),
      timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    },
  };

  // Tasksタスク作成（RFC 3339形式に変換）
  const googleTask: GoogleTask = {
    title: title,
    due: startTime.toISOString(),
  };

  // 両方を並列で作成
  const [calendarResult, taskResult] = await Promise.all([
    createCalendarEvent(calendarEvent),
    createTask(googleTask),
  ]);

  return {
    calendar: calendarResult,
    task: taskResult,
  };
};
