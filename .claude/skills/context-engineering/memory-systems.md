---
description: メモリシステム設計。セッション間の永続化と知識の蓄積・取得パターン。
triggers:
  - セッション間永続化
  - エンティティ一貫性維持
  - 蓄積知識に基づく推論
  - 時間認識システム構築
---

# Memory System Design

## When to Activate
- セッション間で永続化が必要なエージェント構築時
- 会話間でエンティティの一貫性を維持する必要がある時
- 蓄積された知識に基づく推論を実装する時
- 過去のインタラクションから学習するシステム設計時
- 時間経過とともに成長するナレッジベース構築時

## Core Concepts

### メモリスペクトラム

```
[即時]                                      [永続]
  |                                           |
Working Memory ─── Episodic ─── Semantic ─── Storage
(コンテキスト)      (出来事)      (知識)      (DB)
```

| レイヤー | 特徴 | レイテンシ | 永続性 |
|---------|------|-----------|--------|
| Working Memory | コンテキストウィンドウ内 | ゼロ | セッション終了で消失 |
| Episodic Memory | 具体的な出来事の記録 | 低 | 中期保持 |
| Semantic Memory | 抽象化された知識 | 中 | 長期保持 |
| Permanent Storage | DB/ファイル | 高（取得必要） | 永続 |

### Memory Implementation Patterns

#### 1. Vector Store（ベクトルストア）
```python
# 概念的な例
def store_memory(text, embedding_model, vector_db):
    embedding = embedding_model.encode(text)
    vector_db.insert(embedding, metadata={"text": text})

def retrieve_memory(query, embedding_model, vector_db, k=5):
    query_embedding = embedding_model.encode(query)
    return vector_db.search(query_embedding, top_k=k)
```
- **利点**: シンプル、高速な類似検索
- **欠点**: 関係性や時間構造がない

#### 2. Knowledge Graph（ナレッジグラフ）
```
[Entity A] ─── relationship ──→ [Entity B]
     │                              │
  [Property]                    [Property]
```
- **利点**: 関係性を保持、推論に適する
- **欠点**: 構築・維持が複雑

#### 3. Temporal Knowledge Graph（時間的ナレッジグラフ）
```
[Entity] ─── relationship ──→ [Entity]
              │
         [valid_from, valid_to]
```
- **利点**: 時間認識クエリ、状態変化の追跡
- **欠点**: 最も複雑

## Memory Retrieval Patterns

### 1. Recency-based（新しさベース）
最近の記憶を優先的に取得

### 2. Importance-based（重要度ベース）
重要とマークされた記憶を優先

### 3. Relevance-based（関連性ベース）
クエリとの類似度で取得

### 4. Hybrid（ハイブリッド）
```
score = α * recency + β * importance + γ * relevance
```

## Memory Consolidation（記憶の統合）

セッション終了時や定期的に行う処理：
1. **要約**: 詳細な記憶を抽象化
2. **インデックス更新**: 検索インデックスを最新化
3. **刈り込み**: 古い/不要な記憶を削除
4. **関連付け**: 新しい記憶と既存知識を接続

## Integration with Context

### コンテキストへの注入パターン
```
[System Prompt]
↓
[Retrieved Memories (関連記憶)]
↓
[Recent Messages (直近の会話)]
↓
[Current Query]
```

### バジェット管理
- メモリ用のトークンバジェットを事前に確保
- 取得した記憶を関連度でソート→切り詰め
- 重要な記憶は常に含める（固定枠）

## Guidelines

### 本山チームへの適用
現在使用中のメモリシステム：
- **ANTIGRAVITY.md**: Semantic Memory（学習・間違いの記録）
- **TEAM_RULES.md**: Procedural Memory（手続き的知識）
- **task.md**: Episodic Memory（プロジェクト履歴）
- **specs/**: Reference Memory（仕様書）

### 推奨改善
1. `.claude/memories/` フォルダの活用強化
2. 会話サマリの自動保存
3. プロジェクト間での知識共有

---

*Source: Agent Skills for Context Engineering by muratcankoylan*
