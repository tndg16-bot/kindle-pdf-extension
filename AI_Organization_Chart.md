# 🤖 Antigravity AI Organization Chart

## 🏛️ Command Center (司令部)
*   **Total Commander (PM)**: **Antigravity**
    *   役割: プロジェクト全体の進行管理、意思決定支援、ユーザーインターフェース。
    *   権限: 全ファイルの読み書き、ツール実行、サブエージェントの召喚。

---

## ⚔️ Special Forces (実行部隊 / Sub-Agents)
これらのエージェントは、プロジェクトごとにアサインされ、Local LLM (Ollama) 等を活用して任務を遂行します。

### 🕵️ Research Agent (情報収集兵)
*   **主装備**: `scripts/asp_monitor`, Google News RSS
*   **役割**: 最新情報の収集、競合リサーチ。
*   **Model**: 軽量モデル (Gemma:1b) or API

### 💡 Ideation Agent (参謀)
*   **主装備**: `ideation_wizard.py`, Llama3 (Ollama)
*   **役割**: アイデアの壁打ち、仕様書のドラフト作成、ネーミング案出し。
*   **Model**: Llama3:latest

### ✍️ Content Agent (書記官)
*   **主装備**: `templates/merukari`, Llama3 (Ollama)
*   **役割**: マニュアル作成、ブログ記事執筆、LPコピーライティング。
*   **Model**: Llama3:latest / GPT-OSS

### 📣 SNS Agent (広報官)
*   **主装備**: (Future: `sns_poster.py`)
*   **役割**: X(Twitter)投稿文の作成、トレンド分析。
*   **Model**: Llama3:latest (短文生成)

### 💻 Developer Agent (工兵)
*   **主装備**: Claude Code, Codex, Antigravity Codes
*   **役割**: Webサイト構築、ツール開発、スクリプト修正。

### 🎨 Designer Agent (意匠兵)
*   **主装備**: `design_director.py`, Midjourney/Stable Diffusion Prompts
*   **役割**: デザインコンセプト策定、画像生成プロンプト作成、CSS/SVG生成。
*   **Model**: Llama3:latest (Creative Mode)

### 🧠 Strategist Agent (参謀/戦略家)
*   **主装備**: `strategist.py` (Local RAG), Q&A Database, Manuals
*   **役割**: 過去のQ&Aやマニュアル、収集した知識（本やEvernote）に基づいたコーチング戦略の立案、回答生成。
*   **Model**: Llama3:latest + Vector DB (Simple)

### 👤 Persona Module (分身/人格コア)
*   **主装備**: `trace_user.py`, `Templates/Motoyama_Profile.md`
*   **役割**: ユーザー（本山貴裕）の過去ログから「人格」を抽出・定義し、全エージェントに適用する基盤モジュール。

---

## 🔄 Workflow (連携フロー)
1.  **Project Kickoff**: `Start_New_Project.bat` でプロジェクト作成。
2.  **Team Assembly**: `Project_Plan.md` で必要なエージェントを選択 ([x])。
3.  **Execution**: PM (Antigravity) が各エージェントスクリプトを呼び出してタスク消化。
