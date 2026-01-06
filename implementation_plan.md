# Portfolio Content Expansion Plan (Phase 10)

## Goal
トップページのみのシングルページ構成から、マルチページ構成へ拡張し、コンテンツの深さとSEO強度を高める。

## User Review Required
- **階層構造**: 以下のページ構成でよいか？
    - `/projects`: プロジェクト一覧（現在はダッシュボードの一部）。全プロジェクトをカード形式でリッチに表示。
    - `/philosophy`: 理念の詳細。「Life Self-Determination」や「Conductor Mindset」の深掘り記事。
    - `/sessions`: 提供サービス（コーチング、研修）の詳細説明と料金体系。
- **データソース**: プロジェクト詳細は現状 `やりたいことリスト.md` の1行のみ。詳細ページを作るには、各プロジェクトごとのMarkdownファイルが必要になる可能性がある。今回はまず「一覧ページ」の作成までとするか？

## Proposed Changes

### 1. New Pages (Phase 1 Structure)
#### [NEW] src/app/about/page.tsx (Priority: 1)
- **Role**: ストーリー・経歴。人となりで信頼を得る。
- **Content**: プロフィール画像、経歴サマリー、"Life Self-Determination"に至る原体験（ストーリー）。

#### [NEW] src/app/philosophy/page.tsx (Priority: 2)
- **Role**: 思想・考え方。共感で惹きつける。
- **Content**: ノウハウ依存からの卒業、AI活用の思想（Conductor Mindset）、Note記事への導線。

#### [NEW] src/app/sessions/page.tsx (Priority: 3)
- **Role**: セッション詳細＋予約フォーム。予約率を上げる。
- **Content**: 提供サービス詳細、料金、対象者、そして `BookingForm`（現在はトップにあるものを移動）。

#### [NEW] src/app/contact/page.tsx (Priority: 4)
- **Role**: 問い合わせ・SNSリンク。
- **Content**: シンプルな連絡フォームまたはEmailリンク、X/Note等のSNSリンク集。


### 2. Navigation Updates
#### [MODIFY] src/app/page.tsx
- トップページのリンク（Footerなど）を、`#` ではなく `Link href="/philosophy"` 等に書き換え。
- トップのコンテンツ量を調整（詳細ページへ誘導する形に）。

#### [NEW] src/components/Navigation.tsx
- 共通ヘッダーコンポーネントを作成し、全ページでナビゲーション可能にする。

## Verification Plan
### Browser Testing
- `http://localhost:3001/projects` にアクセスし、プロジェクト一覧が表示されるか。
- `http://localhost:3001/philosophy` が表示されるか。
- ナビゲーション（ヘッダー/フッター）のリンク遷移が正しいか。
