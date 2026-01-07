import { useState, useEffect } from 'react';
import { useSpeechRecognition } from '../hooks/useSpeechRecognition';
import { createTaskBoth } from '../services/googleApi';
import './TaskForm.css';

export const TaskForm = () => {
  const [title, setTitle] = useState('');
  const [deadline, setDeadline] = useState('');
  const [duration, setDuration] = useState('1');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const {
    isListening,
    transcript,
    error: speechError,
    isSupported,
    startListening,
    stopListening,
    resetTranscript,
  } = useSpeechRecognition();

  // 音声認識の結果をタイトルに反映
  useEffect(() => {
    if (transcript) {
      setTitle(transcript);
    }
  }, [transcript]);

  // フォーム送信ハンドラー
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSuccessMessage('');
    setErrorMessage('');

    // バリデーション
    if (!title.trim()) {
      setErrorMessage('タスク名を入力してください');
      return;
    }
    if (!deadline) {
      setErrorMessage('期限を選択してください');
      return;
    }

    setIsSubmitting(true);

    try {
      // Google Calendar & Tasks に登録
      await createTaskBoth(title, deadline, parseFloat(duration));

      setSuccessMessage('✅ タスクを登録しました！');

      // フォームをリセット
      setTitle('');
      setDeadline('');
      setDuration('1');
      resetTranscript();

      // 成功メッセージを3秒後に消す
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (error) {
      console.error('Error creating task:', error);
      setErrorMessage('❌ タスクの登録に失敗しました。もう一度お試しください。');
    } finally {
      setIsSubmitting(false);
    }
  };

  // 音声入力ボタンのハンドラー
  const handleVoiceInput = () => {
    if (isListening) {
      stopListening();
    } else {
      resetTranscript();
      startListening();
    }
  };

  return (
    <div className="task-form-container">
      <h2>📝 タスク登録</h2>

      <form onSubmit={handleSubmit} className="task-form">
        {/* タスク名 */}
        <div className="form-group">
          <label htmlFor="title">タスク名</label>
          <div className="input-with-voice">
            <input
              type="text"
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="例: プロジェクト資料作成"
              disabled={isSubmitting}
            />
            {isSupported && (
              <button
                type="button"
                className={`voice-button ${isListening ? 'listening' : ''}`}
                onClick={handleVoiceInput}
                disabled={isSubmitting}
                title="音声入力"
              >
                {isListening ? '🎤 録音中...' : '🎤'}
              </button>
            )}
          </div>
          {speechError && <p className="error-text small">{speechError}</p>}
        </div>

        {/* 期限 */}
        <div className="form-group">
          <label htmlFor="deadline">期限（日時）</label>
          <input
            type="datetime-local"
            id="deadline"
            value={deadline}
            onChange={(e) => setDeadline(e.target.value)}
            disabled={isSubmitting}
          />
        </div>

        {/* 所要時間 */}
        <div className="form-group">
          <label htmlFor="duration">所要時間（時間）</label>
          <select
            id="duration"
            value={duration}
            onChange={(e) => setDuration(e.target.value)}
            disabled={isSubmitting}
          >
            <option value="0.5">0.5時間（30分）</option>
            <option value="1">1時間</option>
            <option value="1.5">1.5時間（1時間30分）</option>
            <option value="2">2時間</option>
            <option value="3">3時間</option>
            <option value="4">4時間</option>
            <option value="5">5時間</option>
            <option value="6">6時間</option>
            <option value="8">8時間</option>
          </select>
        </div>

        {/* メッセージ表示 */}
        {successMessage && <p className="success-message">{successMessage}</p>}
        {errorMessage && <p className="error-message">{errorMessage}</p>}

        {/* 送信ボタン */}
        <button type="submit" className="submit-button" disabled={isSubmitting}>
          {isSubmitting ? '登録中...' : '📅 カレンダーに登録'}
        </button>
      </form>

      {/* 説明文 */}
      <div className="form-info">
        <p>💡 このツールは Google Calendar と Google Tasks の両方にタスクを登録します</p>
        <p>🎤 音声入力は Chrome / Edge で利用できます</p>
      </div>
    </div>
  );
};
