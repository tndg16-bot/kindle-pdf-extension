# 📅 タスク管理ツール

音声入力対応・Google Calendar/Tasks 連携タスク管理Webアプリ

## ✨ 機能

- 🎤 **音声入力対応**: タスク名を音声で入力可能（Chrome/Edge）
- 📅 **Google Calendar連携**: 指定した期限から所要時間分のイベントを自動作成
- ✅ **Google Tasks連携**: ToDoリストに自動登録
- 📱 **レスポンシブデザイン**: PC/スマホ両対応
- 🔐 **OAuth 2.0認証**: Googleアカウントで安全にログイン

## 🚀 クイックスタート

### 1. 環境設定

`.env.local` ファイルを作成し、GCPから取得したClient IDを設定:

```bash
cp .env.example .env.local
```

`.env.local` を編集:

```env
VITE_GOOGLE_CLIENT_ID=あなたのClient ID.apps.googleusercontent.com
```

### 2. 依存関係のインストール

```bash
npm install
```

### 3. 開発サーバー起動

```bash
npm run dev
```

ブラウザで `http://localhost:5173` を開きます。

## 📝 使い方

1. **Googleアカウントでログイン**
   - 「Googleでログイン」ボタンをクリック
   - Google Calendar と Google Tasks へのアクセスを許可

2. **タスクを登録**
   - タスク名を入力（音声入力も可能）
   - 期限（日時）を選択
   - 所要時間を選択
   - 「カレンダーに登録」ボタンをクリック

3. **自動登録完了**
   - Google Calendarにイベントが作成されます
   - Google Tasksにタスクが登録されます

## 🎤 音声入力について

### 対応ブラウザ
- ✅ Google Chrome（完全対応）
- ✅ Microsoft Edge（完全対応）
- ❌ Firefox（非対応）
- ⚠️ Safari（部分対応）

### 使い方
1. タスク名入力欄の右側にあるマイクボタンをクリック
2. 音声認識が開始されます（ボタンが赤色に変わります）
3. タスク名を話します
4. 認識結果がリアルタイムで入力欄に反映されます

## 🔧 技術スタック

- **フロントエンド**: Vite + React + TypeScript
- **API連携**: Google Calendar API v3, Google Tasks API
- **認証**: OAuth 2.0
- **音声認識**: Web Speech API（ブラウザ標準）

## 📂 プロジェクト構造

```
task-manager/app/
├── src/
│   ├── components/       # UIコンポーネント
│   │   ├── AuthButton.tsx        # 認証ボタン
│   │   ├── AuthButton.css
│   │   ├── TaskForm.tsx          # タスク入力フォーム
│   │   └── TaskForm.css
│   ├── hooks/            # カスタムフック
│   │   └── useSpeechRecognition.ts  # 音声認識フック
│   ├── services/         # Google API連携
│   │   └── googleApi.ts
│   ├── types/            # TypeScript型定義
│   │   └── index.ts
│   ├── App.tsx           # メインコンポーネント
│   ├── App.css
│   └── main.tsx
├── .env.example          # 環境変数サンプル
├── .env.local            # 環境変数（Git除外）
├── package.json
└── README.md
```

## 🔐 セキュリティ

- `.env.local` はGitにコミットされません（`.gitignore`で除外）
- Client IDは公開しても問題ありませんが、念のため環境変数で管理
- OAuth 2.0フローにより、パスワードを直接扱うことはありません

## 🆘 トラブルシューティング

### Q1. 「Google APIの初期化に失敗しました」と表示される
**A**: `.env.local` ファイルにClient IDが正しく設定されているか確認してください。

### Q2. 音声入力ボタンが表示されない
**A**: Chrome または Edge ブラウザを使用してください。Firefoxは非対応です。

### Q3. 「音声認識エラー: not-allowed」が表示される
**A**: ブラウザのマイク権限を許可してください。URLバー左側の錠前アイコンから設定できます。

### Q4. カレンダーにイベントが作成されない
**A**:
- Googleアカウントでログインしているか確認
- Google Calendar APIへのアクセス権限を許可しているか確認
- ブラウザのコンソールでエラーメッセージを確認

## 📚 関連ドキュメント

- [GCP完全設定ガイド](../docs/GCP_COMPLETE_SETUP_GUIDE.md) - Google Cloud Platform の設定手順
- [実装仕様書](../docs/IMPLEMENTATION_SPEC.md) - 詳細な技術仕様

## 📄 ライセンス

MIT License

## 🤝 貢献

Issue や Pull Request は大歓迎です！

---

Made with ❤️ by Claude Code
