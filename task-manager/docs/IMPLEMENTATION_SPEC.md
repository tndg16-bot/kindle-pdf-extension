# タスク管理ツール実装仕様書

**Issue Title**: `feat: タスク管理ツール（音声入力対応）の実装`

---

## 📋 概要
Google Calendar/Tasks APIと連携し、音声入力でタスクを素早く登録できるWebアプリを実装します。

## 🎯 目的
作業中に「これタスクに追加しないと」と思ったときに、**別タブを開かず、音声で即座に登録**できるツールを作成する。

## 🔧 技術スタック（提案）
- **フロントエンド**: Vite + React (TypeScript)
- **API連携**: Google Calendar API v3, Google Tasks API
- **認証**: OAuth 2.0
- **音声入力**: Web Speech API（ブラウザ標準、無料）
- **デプロイ**: Vercel（無料プラン）

### 技術選定理由

#### React + TypeScript を選んだ理由
- 認証状態、タスク入力状態などの状態管理が簡潔
- Web Speech APIとの統合が容易
- Vercelへのデプロイが1コマンド
- TypeScriptで型安全性を確保

#### Web Speech API を選んだ理由
- 無料・セットアップ不要
- Chrome/Edge で完全対応（主要ブラウザ）
- ローカル開発可能（localhost は HTTPS 不要）
- オンデバイス認識でプライバシー保護

#### デプロイを推奨する理由
1. 音声入力のため HTTPS が必要 → 本番環境が必要
2. スマホからもアクセス可能になる（外出先でのタスク登録）
3. デプロイコスト: 無料（Vercel）

---

## ✨ 主要機能

### 1. タスク入力フォーム
- **タスク名**（必須）
  - テキスト入力
  - 音声入力対応（マイクボタン）
- **期限**（必須）
  - 日時指定（例: 2025-12-15 14:00）
  - 日付ピッカー + 時刻ピッカー
- **所要時間**（必須）
  - 数値入力（時間単位: 例 2時間）
  - 0.5時間刻みで選択可能

### 2. Google Calendar連携
**カレンダーイベント作成**:
- 指定した開始時刻から所要時間分のイベントを作成
- 例: 期限「2025-12-15 14:00」、所要時間「2時間」
  → 12/15 14:00-16:00 のイベント作成

### 3. Google Tasks連携
**ToDoリストにタスク登録**:
- 期限を設定したToDoタスクを作成
- タスク名と期限を登録

### 4. 音声入力機能（Web Speech API）
- 「タスク名」フィールド横にマイクボタン
- ボタンクリック → 音声認識開始
- 認識結果をリアルタイムでフィールドに反映
- Chrome/Edge 対応（Firefox は非対応）
- HTTPS環境必須（localhost開発は除く）

---

## 🔍 確認事項（ユーザー確認待ち）

### A. GCP設定状況
以下の設定が完了しているか確認してください:

- [ ] GCPプロジェクト作成済みですか？
- [ ] Google Calendar API有効化済みですか？
- [ ] Google Tasks API有効化済みですか？
- [ ] OAuth Client ID取得済みですか？
  - Client ID: `XXXXX.apps.googleusercontent.com` の形式
  - もし未取得の場合、[GCP_SETUP_GUIDE.md](./GCP_SETUP_GUIDE.md)を参照
- [ ] 承認済みリダイレクトURI設定:
  - ローカル開発: `http://localhost:5173`
  - デプロイ後: `https://[your-app].vercel.app`（後で追加でOK）

**確認方法**:
1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 作成したプロジェクトを選択
3. 「APIとサービス」→「認証情報」から確認

### B. 技術スタック承認
- [ ] **React + TypeScript**で問題ないですか？
  - 代替案: Vanilla JS（シンプルだが状態管理が煩雑）
- [ ] **Vercelへのデプロイ**でよろしいですか？
  - 音声入力にHTTPS必須のため、デプロイ推奨
  - 代替案: Cloudflare Pages, Netlify

### C. 仕様確認
- [ ] 期限入力: 「開始時刻」を指定 → 開始時刻から所要時間分のイベント作成
  **例**: 14:00、2時間 → 14:00-16:00 のイベント（✅ 確認済み）
- [ ] カレンダーとTasks両方に登録する仕様でOK?

---

## 📦 実装フェーズ

### Phase 1: プロジェクト初期化
- [ ] Vite + React + TypeScript環境構築
- [ ] プロジェクトフォルダ構成
  ```
  task-manager/
  ├── src/
  │   ├── components/     # UIコンポーネント
  │   ├── services/       # Google API連携
  │   ├── hooks/          # カスタムフック
  │   └── types/          # TypeScript型定義
  ├── public/
  └── package.json
  ```
- [ ] 必要なパッケージインストール
  - `@google-cloud/local-auth`
  - `googleapis`
  - その他依存関係

### Phase 2: 認証実装
- [ ] OAuth 2.0フロー実装
  - Google認証画面へのリダイレクト
  - 認証コールバック処理
- [ ] トークン管理
  - アクセストークンの取得・保存
  - リフレッシュトークン処理
- [ ] 認証状態管理（React Context）

### Phase 3: UI実装
- [ ] タスク入力フォーム
  - タスク名入力
  - 期限選択（日時ピッカー）
  - 所要時間選択
- [ ] 音声入力ボタン
  - マイクアイコン
  - 録音中の視覚フィードバック
  - 認識結果の表示
- [ ] レスポンシブデザイン
  - PC/スマホ対応
  - シンプルで使いやすいUI

### Phase 4: Google API連携
- [ ] Calendar API: イベント作成
  - 開始時刻・終了時刻の計算
  - カレンダーへのイベント登録
- [ ] Tasks API: タスク登録
  - ToDoリストへの登録
  - 期限設定
- [ ] エラーハンドリング
  - API呼び出し失敗時の処理
  - ユーザーへのエラーメッセージ表示

### Phase 5: デプロイ
- [ ] Vercelアカウント設定
- [ ] デプロイ設定
- [ ] 環境変数設定（OAuth Client ID等）
- [ ] 本番環境でのテスト
- [ ] GCPのリダイレクトURI更新（本番URL追加）

---

## 📝 入力/出力仕様

### 入力項目
| 項目 | 型 | 必須 | 説明 | 例 |
|------|-----|------|------|-----|
| タスク名 | テキスト | ✓ | タスクの内容 | 「プロジェクト資料作成」 |
| 期限 | 日時 | ✓ | タスクの開始時刻 | 2025-12-15 14:00 |
| 所要時間 | 数値 | ✓ | 予定時間（時間単位） | 2 |

### 出力仕様
1. **Googleカレンダー**
   - イベント作成: `期限` から `期限 + 所要時間` までのイベント
   - 例: 期限「2025-12-15 14:00」、所要時間「2時間」
     → 12/15 14:00-16:00 のイベント

2. **Google Tasks**
   - ToDoタスク作成
   - タスク名: 入力されたタスク名
   - 期限: 入力された期限

---

## 🧪 テスト計画

### 1. ローカル環境テスト
- [ ] OAuth認証フロー
- [ ] 音声入力の動作確認（Chrome/Edge）
- [ ] カレンダーイベント作成
- [ ] Tasksへのタスク登録

### 2. エラーケーステスト
- [ ] 未認証状態でのアクセス
- [ ] API呼び出し失敗
- [ ] 音声認識失敗
- [ ] 不正な入力値

### 3. デプロイ後テスト
- [ ] HTTPS環境での音声入力
- [ ] スマホからのアクセス
- [ ] 本番環境でのAPI連携

---

## 📚 参考資料

### Google API
- [Google Calendar API v3](https://developers.google.com/calendar/api/guides/overview)
- [Google Tasks API](https://developers.google.com/tasks)
- [OAuth 2.0 for Client-side Web Applications](https://developers.google.com/identity/protocols/oauth2/javascript-implicit-flow)

### Web Speech API
- [Web Speech API - MDN](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)
- [SpeechRecognition API](https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition)
- [Browser Support - Can I Use](https://caniuse.com/speech-recognition)

### デプロイ
- [Vercel Documentation](https://vercel.com/docs)
- [Deploying React Apps](https://vitejs.dev/guide/static-deploy.html#vercel)

---

## ✅ 完了条件

- [ ] OAuth認証が正常に動作する
- [ ] タスク入力フォームが動作する
- [ ] 音声入力が動作する（Chrome/Edge）
- [ ] Google Calendarにイベントが作成される
- [ ] Google Tasksにタスクが登録される
- [ ] エラーハンドリングが適切に実装されている
- [ ] レスポンシブデザインが実装されている
- [ ] Vercelにデプロイされている
- [ ] 本番環境でテスト完了
- [ ] ドキュメントが整備されている

---

**次のアクション**: 上記「確認事項」にご回答いただけましたら、実装を開始します🚀
