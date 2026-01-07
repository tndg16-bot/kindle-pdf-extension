import { useState, useEffect } from 'react';
import { initGoogleApi, isSignedIn, signIn, signOut, getCurrentUser } from '../services/googleApi';
import './AuthButton.css';

interface AuthButtonProps {
  onAuthChange?: (isSignedIn: boolean) => void;
}

export const AuthButton = ({ onAuthChange }: AuthButtonProps) => {
  const [isInitialized, setIsInitialized] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<{ name: string; email: string; imageUrl?: string } | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const initialize = async () => {
      try {
        await initGoogleApi();
        setIsInitialized(true);

        // 初期ログイン状態を確認
        const signedIn = isSignedIn();
        setIsAuthenticated(signedIn);
        if (signedIn) {
          setUser(getCurrentUser());
        }

        // ログイン状態変更を監視
        gapi.auth2.getAuthInstance().isSignedIn.listen((signedIn: boolean) => {
          setIsAuthenticated(signedIn);
          if (signedIn) {
            setUser(getCurrentUser());
          } else {
            setUser(null);
          }
          onAuthChange?.(signedIn);
        });

        onAuthChange?.(signedIn);
      } catch (err) {
        console.error('Failed to initialize Google API:', err);
        setError('Google APIの初期化に失敗しました。環境変数（Client ID）を確認してください。');
      }
    };

    initialize();
  }, [onAuthChange]);

  const handleSignIn = async () => {
    try {
      setError(null);
      await signIn();
    } catch (err) {
      console.error('Sign in error:', err);
      setError('ログインに失敗しました');
    }
  };

  const handleSignOut = async () => {
    try {
      setError(null);
      await signOut();
    } catch (err) {
      console.error('Sign out error:', err);
      setError('ログアウトに失敗しました');
    }
  };

  if (!isInitialized) {
    return <div className="auth-loading">Google APIを初期化中...</div>;
  }

  if (error) {
    return <div className="auth-error">❌ {error}</div>;
  }

  if (isAuthenticated && user) {
    return (
      <div className="auth-container authenticated">
        <div className="user-info">
          {user.imageUrl && <img src={user.imageUrl} alt={user.name} className="user-avatar" />}
          <div className="user-details">
            <p className="user-name">{user.name}</p>
            <p className="user-email">{user.email}</p>
          </div>
        </div>
        <button onClick={handleSignOut} className="auth-button signout">
          ログアウト
        </button>
      </div>
    );
  }

  return (
    <div className="auth-container">
      <button onClick={handleSignIn} className="auth-button signin">
        <svg className="google-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
          <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
          <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
          <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
        </svg>
        Googleでログイン
      </button>
      <p className="auth-note">※ Google Calendar と Google Tasks へのアクセスを許可してください</p>
    </div>
  );
};
