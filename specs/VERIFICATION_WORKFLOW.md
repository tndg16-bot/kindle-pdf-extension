# 🕵️ Verification Agent Workflow

## 1. 目的 (Objective)
「修正しました」と言ったのに直っていない（空振り）を防ぐ。
AIが書いたコードが本当に反映され、動作するかを別プロセスで検証する。

## 2. フロー (Workflow)

### Step 1: Implementation (Developer)
*   コードを修正する (`replace_file_content`, `write_to_file`).
*   **注意**: この時点では「完了」と報告しない。

### Step 2: Confirmation (Reviewer)
*   **Read File**: 修正したファイルを `view_file` で読み直す。
    *   ❌ 変更箇所が変わっていない -> Step 1へ戻る (Tool Errorの確認)
    *   ✅ 変更されている -> Step 3へ
*   **Compile/Lint**: `npm run build` や `npm run lint` を走らせる。
    *   ❌ エラーが出る -> Step 1へ戻る

### Step 3: Reporting (PM)
*   Step 2をパスして初めて「修正および検証が完了しました」とユーザーに報告する。

## 3. 具体的なアクション (Actionable Rule)
ツール実行後、**必ず** 以下のツールを呼ぶこと。
1.  `view_file` (対象ファイル) -> 自分の目でコードが変わったか見る。
2.  `run_command` (npm run type-check etc) -> エラーがないか見る。
