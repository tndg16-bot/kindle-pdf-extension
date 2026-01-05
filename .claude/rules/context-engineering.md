# Context Engineering Rules

このドキュメントは、すべての AI エージェントが従うべきコンテキストエンジニアリングの原則を定義します。

## Core Principles

### 1. Context Isolation (コンテキスト隔離)
各エージェントは独立したコンテキストウィンドウで動作し、必要なスキルのみをロードする。
- **Why**: Attention Scarcity（注意資源の枯渇）を防ぐため
- **How**: `skills/` 内の SKILL.md を必要時のみ参照

### 2. Progressive Disclosure (段階的開示)
情報は必要になった時点で段階的に開示する。
- Level 1: SKILL.md（最初に読む）
- Level 2: scripts/（実行コードが必要な時）
- Level 3: references/（詳細な参照が必要な時）

### 3. File System Memory (ファイルシステムメモリ)
共有状態はコンテキストウィンドウに渡さず、ファイルシステムに永続化する。
- `memories/` フォルダに JSONL 形式でログを保存
- スプリントログ、設計決定、学習結果を記録

## Immutable Global Rules

1. **Sage-First Policy**: 実装完了後は必ず Sage のレビューを通すこと
2. **User Sovereignty**: ユーザー（本山さん）の最終決定権を尊重すること
3. **Philosophy Alignment**: すべての成果物は「人生の自己決定」というブランドに沿うこと

## Agent Coordination

### Supervisor Pattern (Leo)
```
User -> Leo (PM) -> [Mia, Kai, Ken, Sage, Sora] -> Aggregation -> User
```

### Handoff Protocol
- タスク完了時は次のエージェントへ明示的に引き継ぐ
- 引き継ぎ時には必要なコンテキストを文書化する
