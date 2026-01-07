import { useState, useEffect, useCallback } from 'react';
import { GoogleOAuthProvider, useGoogleLogin, googleLogout } from '@react-oauth/google';
import './App.css';

// Google APIの型定義
declare const gapi: any;

// 環境変数からClient IDを取得
const CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;

// ユーザー情報の型
interface UserInfo {
  name: string;
  email: string;
  picture?: string;
}

// タスク履歴の型
interface TaskHistory {
  id: string;
  title: string;
  deadline: string;
  duration: number;
  createdAt: Date;
}

// クイックプリセットの型
interface QuickPreset {
  label: string;
  icon: string;
  hours: number;
  minutes: number;
}

// クイックプリセット定義
const QUICK_PRESETS: QuickPreset[] = [
  { label: '朝', icon: '🌅', hours: 9, minutes: 0 },
  { label: '昼', icon: '☀️', hours: 12, minutes: 0 },
  { label: '夕方', icon: '🌇', hours: 17, minutes: 0 },
  { label: '夜', icon: '🌙', hours: 21, minutes: 0 },
];

// 認証ボタンコンポーネント（改良版）
function AuthSection({
  onLoginSuccess,
  onLogout,
  user
}: {
  onLoginSuccess: (user: UserInfo, accessToken: string) => void;
  onLogout: () => void;
  user: UserInfo | null;
}) {
  const [isLoading, setIsLoading] = useState(false);

  const login = useGoogleLogin({
    onSuccess: async (tokenResponse) => {
      setIsLoading(true);
      try {
        const userInfoResponse = await fetch('https://www.googleapis.com/oauth2/v3/userinfo', {
          headers: { Authorization: `Bearer ${tokenResponse.access_token}` },
        });
        const userInfo = await userInfoResponse.json();
        onLoginSuccess({ name: userInfo.name, email: userInfo.email, picture: userInfo.picture }, tokenResponse.access_token);
      } catch (error) {
        console.error('Failed to get user info:', error);
      } finally {
        setIsLoading(false);
      }
    },
    onError: () => setIsLoading(false),
    scope: 'https://www.googleapis.com/auth/calendar.events https://www.googleapis.com/auth/tasks',
  });

  if (user) {
    return (
      <div className="user-card glass-card">
        <div className="user-info">
          {user.picture && <img src={user.picture} alt={user.name} className="user-avatar" />}
          <div className="user-details">
            <span className="user-name">👋 {user.name}</span>
            <span className="user-email">{user.email}</span>
          </div>
        </div>
        <button onClick={() => { googleLogout(); onLogout(); }} className="logout-btn">
          ログアウト
        </button>
      </div>
    );
  }

  return (
    <div className="login-section glass-card">
      <div className="login-content">
        <h2>🚀 はじめよう</h2>
        <p>Googleアカウントでログインして、タスク管理を始めましょう</p>
        <button onClick={() => login()} disabled={isLoading} className="google-login-btn">
          <svg width="20" height="20" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
          </svg>
          {isLoading ? '接続中...' : 'Googleでログイン'}
        </button>
      </div>
      <div className="features-preview">
        <div className="feature-item">📅 カレンダー登録</div>
        <div className="feature-item">🎤 音声入力</div>
        <div className="feature-item">✅ タスク管理</div>
      </div>
    </div>
  );
}

// タスク入力フォーム（大幅改良版）
function TaskForm({ accessToken }: { accessToken: string }) {
  const [title, setTitle] = useState('');
  const [deadline, setDeadline] = useState('');
  const [duration, setDuration] = useState('1');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>('medium');
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState<'success' | 'error' | 'info'>('info');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [gapiReady, setGapiReady] = useState(false);
  const [taskHistory, setTaskHistory] = useState<TaskHistory[]>([]);
  const [showHistory, setShowHistory] = useState(false);

  // 音声入力の状態
  const [isListening, setIsListening] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(false);
  const [recognition, setRecognition] = useState<any>(null);

  // 音声認識の初期化
  useEffect(() => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SpeechRecognition) {
      setSpeechSupported(true);
      const recognitionInstance = new SpeechRecognition();
      recognitionInstance.continuous = false;
      recognitionInstance.interimResults = true;
      recognitionInstance.lang = 'ja-JP';

      recognitionInstance.onresult = (event: any) => {
        const transcript = event.results[event.results.length - 1][0].transcript;
        setTitle(transcript);
      };
      recognitionInstance.onerror = () => setIsListening(false);
      recognitionInstance.onend = () => setIsListening(false);
      setRecognition(recognitionInstance);
    }
  }, []);

  // gapi初期化
  useEffect(() => {
    const initGapi = async () => {
      try {
        let attempts = 0;
        while (typeof gapi === 'undefined' && attempts < 50) {
          await new Promise(resolve => setTimeout(resolve, 100));
          attempts++;
        }
        if (typeof gapi === 'undefined') return;

        await new Promise<void>((resolve, reject) => {
          gapi.load('client', { callback: resolve, onerror: reject });
        });
        await gapi.client.init({
          discoveryDocs: [
            'https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest',
            'https://www.googleapis.com/discovery/v1/apis/tasks/v1/rest',
          ],
        });
        gapi.client.setToken({ access_token: accessToken });
        setGapiReady(true);
      } catch (error) {
        console.error('gapi init error:', error);
      }
    };
    if (accessToken) initGapi();
  }, [accessToken]);

  // 履歴をローカルストレージから読み込み
  useEffect(() => {
    const saved = localStorage.getItem('taskHistory');
    if (saved) setTaskHistory(JSON.parse(saved));
  }, []);

  const toggleListening = () => {
    if (!recognition) return;
    if (isListening) {
      recognition.stop();
    } else {
      recognition.start();
      setIsListening(true);
    }
  };

  // クイックプリセットを適用
  const applyPreset = (preset: QuickPreset) => {
    const date = new Date();
    date.setHours(preset.hours, preset.minutes, 0, 0);
    if (date < new Date()) date.setDate(date.getDate() + 1);
    setDeadline(date.toISOString().slice(0, 16));
  };

  // デフォルト日時を設定
  const getDefaultDeadline = useCallback(() => {
    const now = new Date();
    now.setMinutes(now.getMinutes() + 30);
    now.setSeconds(0);
    return now.toISOString().slice(0, 16);
  }, []);

  useEffect(() => {
    if (!deadline) setDeadline(getDefaultDeadline());
  }, [deadline, getDefaultDeadline]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !deadline) {
      setMessage('タスク名と日時を入力してください');
      setMessageType('error');
      return;
    }
    if (!gapiReady) {
      setMessage('API初期化中...');
      setMessageType('info');
      return;
    }

    setIsSubmitting(true);
    setMessage('');

    try {
      const startTime = new Date(deadline);
      const endTime = new Date(startTime.getTime() + parseFloat(duration) * 60 * 60 * 1000);
      const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;

      await gapi.client.calendar.events.insert({
        calendarId: 'primary',
        resource: {
          summary: `${priority === 'high' ? '🔴 ' : priority === 'medium' ? '🟡 ' : '🟢 '}${title}`,
          start: { dateTime: startTime.toISOString(), timeZone },
          end: { dateTime: endTime.toISOString(), timeZone },
        },
      });

      try {
        const taskListsResponse = await gapi.client.tasks.tasklists.list();
        const defaultTaskList = taskListsResponse.result.items?.[0]?.id;
        if (defaultTaskList) {
          await gapi.client.tasks.tasks.insert({
            tasklist: defaultTaskList,
            resource: { title, due: startTime.toISOString() },
          });
        }
      } catch {
        // Tasks API optional
      }

      // 履歴に追加
      const newTask: TaskHistory = {
        id: Date.now().toString(),
        title,
        deadline,
        duration: parseFloat(duration),
        createdAt: new Date(),
      };
      const updatedHistory = [newTask, ...taskHistory.slice(0, 9)];
      setTaskHistory(updatedHistory);
      localStorage.setItem('taskHistory', JSON.stringify(updatedHistory));

      setMessage('✅ 登録完了！');
      setMessageType('success');
      setTitle('');
      setDeadline('');
      setDuration('1');
    } catch (error: any) {
      setMessage(error?.result?.error?.message || '登録に失敗しました');
      setMessageType('error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="task-form-container">
      <form onSubmit={handleSubmit} className="task-form glass-card">
        {/* タスク名入力 */}
        <div className="form-group">
          <label className="form-label">📝 タスク名</label>
          <div className="input-with-mic">
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder={isListening ? '🎤 話してください...' : 'タスク名を入力'}
              className={`form-input ${isListening ? 'listening' : ''}`}
            />
            {speechSupported && (
              <button type="button" onClick={toggleListening} className={`mic-btn ${isListening ? 'active' : ''}`}>
                {isListening ? '⏹️' : '🎤'}
              </button>
            )}
          </div>
        </div>

        {/* クイックプリセット */}
        <div className="form-group">
          <label className="form-label">⚡ クイック設定</label>
          <div className="quick-presets">
            {QUICK_PRESETS.map((preset) => (
              <button key={preset.label} type="button" onClick={() => applyPreset(preset)} className="preset-btn">
                <span className="preset-icon">{preset.icon}</span>
                <span className="preset-label">{preset.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* 日時入力 */}
        <div className="form-group">
          <label className="form-label">🕐 開始日時</label>
          <input
            type="datetime-local"
            value={deadline}
            onChange={(e) => setDeadline(e.target.value)}
            className="form-input"
          />
        </div>

        {/* 所要時間と優先度 */}
        <div className="form-row">
          <div className="form-group half">
            <label className="form-label">⏱️ 所要時間</label>
            <select value={duration} onChange={(e) => setDuration(e.target.value)} className="form-select">
              {[0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6].map((h) => (
                <option key={h} value={h}>{h}時間</option>
              ))}
            </select>
          </div>
          <div className="form-group half">
            <label className="form-label">🎯 優先度</label>
            <div className="priority-selector">
              {(['low', 'medium', 'high'] as const).map((p) => (
                <button
                  key={p}
                  type="button"
                  onClick={() => setPriority(p)}
                  className={`priority-btn ${priority === p ? 'active' : ''} ${p}`}
                >
                  {p === 'high' ? '🔴' : p === 'medium' ? '🟡' : '🟢'}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* 登録ボタン */}
        <button type="submit" disabled={isSubmitting || !gapiReady} className="submit-btn">
          {isSubmitting ? (
            <span className="loading-spinner"></span>
          ) : (
            <>📅 カレンダーに登録</>
          )}
        </button>

        {/* メッセージ */}
        {message && (
          <div className={`message ${messageType}`}>
            {message}
          </div>
        )}
      </form>

      {/* 履歴セクション */}
      {taskHistory.length > 0 && (
        <div className="history-section glass-card">
          <button onClick={() => setShowHistory(!showHistory)} className="history-toggle">
            📋 最近のタスク ({taskHistory.length})
            <span className={`arrow ${showHistory ? 'open' : ''}`}>▼</span>
          </button>
          {showHistory && (
            <div className="history-list">
              {taskHistory.map((task) => (
                <div key={task.id} className="history-item" onClick={() => { setTitle(task.title); setDuration(task.duration.toString()); }}>
                  <span className="history-title">{task.title}</span>
                  <span className="history-time">{new Date(task.deadline).toLocaleString('ja-JP', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// メインアプリ
function AppContent() {
  const [user, setUser] = useState<UserInfo | null>(null);
  const [accessToken, setAccessToken] = useState<string>('');

  return (
    <div className="app">
      <div className="background-effects">
        <div className="blob blob-1"></div>
        <div className="blob blob-2"></div>
        <div className="blob blob-3"></div>
      </div>

      <header className="app-header">
        <h1 className="app-title">
          <span className="title-icon">📅</span>
          <span className="title-text">Task Manager</span>
        </h1>
        <p className="app-subtitle">Google Calendar × Tasks × 音声入力</p>
      </header>

      <main className="app-main">
        <AuthSection
          user={user}
          onLoginSuccess={(userInfo, token) => { setUser(userInfo); setAccessToken(token); }}
          onLogout={() => { setUser(null); setAccessToken(''); }}
        />
        {user && accessToken && <TaskForm accessToken={accessToken} />}
      </main>

      <footer className="app-footer">
        <p>Made with ❤️ using React + TypeScript</p>
      </footer>
    </div>
  );
}

function App() {
  if (!CLIENT_ID) {
    return (
      <div className="error-screen">
        <h1>⚠️ 設定エラー</h1>
        <p>Client IDが設定されていません</p>
      </div>
    );
  }

  return (
    <GoogleOAuthProvider clientId={CLIENT_ID}>
      <AppContent />
    </GoogleOAuthProvider>
  );
}

export default App;
