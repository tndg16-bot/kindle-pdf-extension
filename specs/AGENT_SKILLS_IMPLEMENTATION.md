# Agent Skills for Context Engineering 実装仕様書

**作成日**: 2026-01-06  
**ステータス**: サブエージェント実装待ち  
**参照元**: https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering

---

## 概要

Context Engineering（コンテキストエンジニアリング）とは、LLMのコンテキストウィンドウを管理する技術。
プロンプトエンジニアリングが「効果的な指示の作成」に焦点を当てるのに対し、
コンテキストエンジニアリングは「モデルの限られたアテンションバジェットに入る全情報のキュレーション」を扱う。

---

## 実装するスキル

### 1. context-fundamentals（基礎）
**発動条件**:
- 新規エージェントシステム設計時
- 予期しないエージェント動作のデバッグ時
- コンテキスト使用の最適化時

**コア概念**:
- コンテキストは複数のコンポーネント（システムプロンプト、ツール定義、履歴、ツール出力）で構成
- アテンションメカニズムは有限バジェットを作成
- Progressive Disclosure（必要時のみ情報ロード）で管理
- 最小の高シグナルトークンセットをキュレートする

### 2. multi-agent-patterns（マルチエージェント）
**発動条件**:
- 単一エージェントのコンテキスト制限がタスク複雑性を制約する時
- タスクが並列サブタスクに分解される時
- 異なるサブタスクが異なるツールセットを必要とする時

**コア概念**:
- 3つの主要パターン:
  1. **Supervisor/Orchestrator**: 中央集権制御
  2. **Peer-to-peer/Swarm**: 柔軟なハンドオフ
  3. **Hierarchical**: 階層的抽象化
- **Context Isolation（コンテキスト分離）** が重要な設計原則
- サブエージェントは組織的役割のシミュレーションではなく、コンテキスト分割のために存在

### 3. memory-systems（メモリシステム）
**発動条件**:
- セッション間で永続化が必要な時
- エンティティの一貫性維持が必要な時
- 蓄積された知識に基づく推論が必要な時

**コア概念**:
- メモリはスペクトラム上に存在（即時コンテキスト ⇔ 永続ストレージ）
- Working Memory（コンテキストウィンドウ）: ゼロレイテンシだがセッション終了で消失
- Permanent Storage: 無期限永続化だが取得が必要
- 実装オプション: Vector Store, Knowledge Graph, Temporal Knowledge Graph

---

## 実装計画

### ファイル構成
```
.claude/skills/
├── context-engineering/
│   ├── context-fundamentals.md
│   ├── multi-agent-patterns.md
│   └── memory-systems.md
└── (既存のスキルファイル)
```

### 各スキルファイルのフォーマット
```markdown
---
description: [スキル説明]
triggers:
  - [発動トリガー1]
  - [発動トリガー2]
---

# [スキル名]

## When to Activate
[発動条件]

## Core Concepts
[コア概念]

## Guidelines
[ガイドライン]
```

---

## 実装手順

1. ブランチ作成: `feature/agent-skills-context-engineering`
2. `.claude/skills/context-engineering/` フォルダ作成
3. 3つのスキルファイル作成
4. 既存の TEAM_RULES.md に参照を追加
5. コミット → プッシュ → PR作成
6. @tndg16-bot にメンションして通知

---

## 検証方法
- スキルファイルが正しいフォーマットで作成されていること
- Claude Codeがスキルを認識できること（`/skills` コマンドで確認）

---

*このファイルはサブエージェント（Codex/Claude Code）への実装指示書です。*
