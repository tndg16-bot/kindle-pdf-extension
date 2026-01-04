# 🧠 ANTIGRAVITY.md - チーム共有ブレイン

このファイルは **Antigravity（PM）を中心とするAIエージェントチーム** の共有知識ベースです。
全てのエージェント（Antigravity, Claude Code, Ollama等）がこのファイルを参照し、**間違いがあれば追記・更新**します。

---

## 📋 基本ルール

### 検証ルール（最重要）
- **全ての実装は検証手段を持つこと**
- コード変更後は必ず `npm test` または `pytest` で確認
- UIの変更はブラウザツールで実際に動作確認
- 検証が通らない限り「完了」とは言わない

### コミットルール
- セマンティックコミットメッセージを使用 (feat:, fix:, docs:, etc.)
- 1コミット = 1つの論理的な変更
- テストが通る状態でのみコミット
- テストが通る状態でのみコミット

## 🇯🇵 Language Protocol
User Rules dictate strict Japanese usage.
*   **Chat Response**: Japanese.
*   **Planning Artifacts (Plans, Tasks)**: Japanese.
*   **Documentation (Specs, Guides)**: Japanese.
*   **Code Comments**: English permitted, but Japanese preferred for complex logic.
*   **Commit Messages**: English permitted.

## 🧠 Skill Crystallization (Context Management)
To prevent context loss:
*   **New Policy = New Rule**: When a workflow is agreed upon, IMMEDIATELY record it here or in a dedicated `.md` file.
*   **Protocol Loading Rule**: Before any "Deep Thinking" or "Major Planning" step, Agents **MUST READ this file (`ANTIGRAVITY.md`)** to refresh context.
    *   *Trigger*: Start of a new Task, Project Phase transition, or when User asks for a complex plan.
*   **Reference First**: Sub-Agents must consult these protocols before acting.

---
ユーザーから授かった「失敗しないための鉄則」。

1.  **ゴール明確化 (Goal Clarity)**: 「〇〇したい」とゴールを最初に明確に伝える。
2.  **徹底ヒアリング (Consultation)**: 実装前に徹底的にインタビューして擦り合わせる (consult-specスキルを活用)。
3.  **最大思考 (Ultra-Think)**: 複雑な問題は `thinking` モードで深く考えさせる。
4.  **計画重視 (Plan Mode)**: `plan` モードで確度の高い実装計画を立ててから動く。
5.  **粘り強さ (Ralph Plugin)**: エラーが出ても `Ralph wiggum` の精神で粘り強く修正させる。

---

## 🚫 やってはいけないこと（学習済みエラー）

| 日付 | エージェント | 間違い | 対策 |
|------|-------------|--------|------|
| 2026-01-03 | 初期設定 | - | このセクションに間違いを追記していく |
| 2026-01-04 | Antigravity | 要件定義が浅いまま進行しようとした | **Deep Dive (Phase 1.5)** の徹底。ロジック/体験の核心を聞くまで実装しない。ステップバイステップで確認する。 |
| 2026-01-04 | Claude | 名前空間の衝突 (Home vs HomeIcon) | `lucide-react` 等のアイコンをインポートする際は、必ず `Recipe as RecipeIcon` のようにエイリアスを貼るか、コンポーネント名を具体的(TaskPage等)にする。 |
| 2026-01-04 | Antigravity | ドメイン知識不足 (マンダラチャートの常識欠如) | **Phase 0.5: Knowledge Input** をルール化。実装前に必ず「その分野のベストプラクティス/常識」を検索し、知識ファイルを作成してから要件定義に入る。 |
| 2026-01-04 | Antigravity | 修正の適用ミス (One-Shot失敗) | コード修正時は、対象行が本当に合っているか `view_file` で確認し、修正内容を **トリプルチェック** する。一発で直す気概を持つ。 |

### Phase 0.5: Knowledge Input (Know before you Build)
新しいドメイン（例：マンダラチャート、会計、特定のAPI）を扱う際は、必ず最初に **Web検索** を行い、**常識・定石・ベストプラクティス** をインプットすること。
「知っているつもり」を排除し、ユーザーと知識レベルを合わせる。得た知識は `specs/DOMAIN_KNOWLEDGE.md` 等にまとめる。

*※ 間違いが発生したら、このテーブルに追記してください*

---

## 🛠️ プロジェクト固有の設定

### ファイル構造
```
.claude/
├── skills/          # スキル定義
├── commands/        # スラッシュコマンド
├── personas/        # ペルソナ定義
├── settings.json    # 権限設定
└── mcp.json         # MCP設定
```

### 使用ツール
- **テスト**: pytest, npm test
- **フォーマット**: Prettier, Black
- **ブラウザ**: Playwright (MCP経由)
- **デザイン**: Figma MCP (UI実装時は必須) - デザイントークン取得用

### デザイン実装ルール (Figma First)
フロントエンド実装時は、必ず **Figma MCP** を使用してデザイントークン (`get_variable_defs`) を取得し、Tailwind CSS等に反映させること。
「雰囲気でCSSを書く」ことを禁止する。

---

## 💡 環境構築ナレッジ (Environment Setup Knowledge)

**MCPサーバーの正しいインストール手順**
曖昧な指示では失敗するため、以下の具体的な手順を実行すること。

### 1. Context7 (Documentation)
*   **Command**: `npm install -g c7-mcp-server`
*   **Config**: `mcp.json` に `"command": "c7-mcp-server"` を指定。

### 2. Serena (Coding Agent)
*   **Download**: `git clone https://github.com/oraios/serena .claude/mcp/serena`
*   **Install**: ディレクトリ内で `pip install .`
*   **注意**: Python 3.12以上では動作しない場合がある（Python 3.10/3.11推奨）。
    *   **Workaround**: Python 3.13環境の場合、`pyproject.toml` の `requires-python` を `">=3.11"` に変更（`<3.12`制限を削除）してから `pip install` することで動作可能。

### 3. Playwright (Browser)
*   **Command**: `npm install -g @modelcontextprotocol/server-playwright`

---

## 📝 更新履歴

| 日付 | 更新者 | 内容 |
|------|--------|------|
| 2026-01-03 | Antigravity | 初版作成 |
| 2026-01-03 | Antigravity | MCPインストール手順を追記 (Context7, Serena) |
