# Codex CLI 活用コマンド チートシート (PowerShell)

> このリポジトリでよく使う実用コマンドと、Codexへの頼み方テンプレをまとめました。`rg` が無い場合は `Select-String` を使ってください。

## コア操作
- `Get-ChildItem -Force`: 隠し含む一覧。`-Recurse -File` で再帰。
- `rg -n "pattern"`: 高速全文検索。`rg --files` で全ファイル一覧。
- `Select-String -Path **\\*.md -Pattern "語句"`: `rg` 無い場合の代替。
- `git status` / `git diff` / `git log --oneline -20`: 変更と履歴の確認。
- `Resolve-Path .\\相対\\path` / `Get-Location`: 絶対パスと現在地確認。

## ノート/Obsidian向け
- `rg -n "^# .+" --glob "*.md"`: 見出し一覧（タイトル拾い）。
- `Get-ChildItem -Recurse -File | Sort LastWriteTime -Desc | Select -First 20 Name,LastWriteTime`: 最近更新ノート。
- `rg -n "タグ|キーワード" --glob "*.md"`: タグ/キーワード横断検索。
- `rg -n "^\\[.*\\]\\(.*\\)" --glob "*.md"`: リンクの棚卸し。

## プロジェクト/環境
- `python -V` / `node -v` / `git --version`: バージョン確認。
- Python: `python -m venv .venv; .\\.venv\\Scripts\\Activate.ps1`
- Node: `npm init -y`（必要なら `npm i -D prettier eslint`）
- Rust: `cargo init`（bin/lib）

## テスト/品質（ある場合）
- Node: `npm test` / `npm run lint` / `npx prettier -c .`
- Python: `pytest -q` / `ruff check .` / `black --check .`
- Rust: `cargo test -q` / `cargo fmt -- --check` / `cargo clippy -q`

## Codexへの頼み方テンプレ（効率化）
- 計画依頼: 「この作業を3–5ステップで計画して。完了ごとに更新して」
- 探索依頼: 「リポ内でXを参照している箇所を`rg`で一覧化して要約して」
- 差分編集: 「`path/to/file` の関数YにZを追加。影響箇所も更新して。パッチで」
- 範囲読解: 「`path/to/file:120-200` を読み、ロジックを3点で要約して」
- 実行と検証: 「`pytest -q` を実行して失敗の要約と修正方針を出して」
- 安全配慮: 「破壊的操作は事前に確認し、最小変更で」
- 出力制御: 「大出力は要約→必要ならファイル保存。コマンドは行頭に」
- 権限関連: 「必要なら権限昇格の理由を述べて確認をとってから実行して」

## 組み合わせ例
- 「まず`rg -n "TODO"`で洗い出し→優先度付け→小さくパッチ→`git diff`確認、の計画を作って進めて」
- 「Obsidianの`.md`から`#`見出しを収集して`Index.md`を生成して。重複は除外」
- 「`git log -- path.md`で変更履歴を要約し、重要変更を3点抽出して」

---
補足:
- `rg` が未インストールの場合は `choco install ripgrep`（Chocolatey）等で導入。職場端末などで不可なら `Select-String` を使用。
- 破壊的操作（`rm`, `git reset`, 大量置換など）は事前に確認する運用にしましょう。
