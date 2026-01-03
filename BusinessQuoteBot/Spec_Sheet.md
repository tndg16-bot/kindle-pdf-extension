# [BusinessQuoteBot] 仕様書

## 1. 📋 Product Overview
*   **Concept**: 毎朝、ビジネスの賢人（ピーター・ティール、スティーブ・ジョブズ、イーロン・マスク）の名言を日報に届け、一日のモチベーションを高める。
*   **Target Audience**: ビジネスパーソン（自分自身）
*   **Core Value**: 思考の視座を強制的に引き上げる。

## 2. 💻 Technical Specification
*   **Core Features**:
    1.  名言データベース（JSON）からランダムに1つ選択。
    2.  当日（または翌日）の日報ファイル `daily/YYYY-MM-DD.md` を特定。
    3.  `## Morning Motivation` セクションを作成し、名言を追記。
*   **Data Structure**:
    *   `quotes.json`: `{ "author": "Steve Jobs", "text": "...", "category": "Mindset" }`
*   **Tech Stack**: Python (Standard Lib)

## 3. 🚀 Execution Strategy
*   **Schedule**: 毎日 05:00 (`run_sync.bat` に組み込み)
