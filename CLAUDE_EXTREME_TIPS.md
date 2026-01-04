# 🧠 CLAUDE_EXTREME_TIPS.md
**Practical Prompt Engineering Guide from Anthropic Learn**

**Source**: https://www.anthropic.com/learn (Research Date: 2026-01-04)

---

## 🎯 Golden Rules (鉄則)

### 1. 思考を出力させる (The Golden Rule of CoT)
> **"Always have Claude output its thinking. Without outputting its thought process, no thinking occurs!"**

Claudeに「考える」時間を与える最も強力な方法は、思考のみを出力させることです。
*   **Technique**: `<thinking>` タグを使用する。
*   **Effect**: 複雑なタスクの精度が劇的に向上します。

### 2. 明確性の鉄則 (The Golden Rule of Clarity)
> **"Show your prompt to a colleague. If they are confused by the instructions, Claude will likely be too."**

Claudeを「優秀だが記憶喪失の新入社員」として扱ってください。文脈、背景、目的を全て伝える必要があります。

### 3. XMLタグで構造化する (Structure with XML)
命令とデータを明確に分離するために、XMLタグを多用してください。
```xml
<instructions>
  ...
</instructions>

<context>
  ...
</context>

<user_input>
  ...
</user_input>
```

---

## 🛠️ Practical Patterns (実践パターン)

### The `<thinking>` Pattern
複雑な推論が必要な場合、答えの前に思考プロセスを出力させます。

**Prompt Example:**
```markdown
Please answer the following question.
Before answering, please think about the question step-by-step inside <thinking> tags.
Then, provide your final answer inside <answer> tags.
```

### Multishot Prompting (例示)
「説明する」より「例を見せる」方が早くて正確です。

**Prompt Example:**
```xml
<examples>
  <example>
    <input>Today is sunny.</input>
    <output>Weather: Sunny | Sentiment: Positive</output>
  </example>
  <example>
    <input>I lost my keys.</input>
    <output>Weather: N/A | Sentiment: Negative</output>
  </example>
</examples>
```

### Role Assignment (ペルソナ)
役割を与えることで、回答のトーンや専門性を調整します。
*   "You are an expert Data Scientist."
*   "You are a friendly coding tutor."

---

## 🚀 Recommended Resources
*   **Prompt Generator**: Anthropic Console内のツール。タスクの概要を入れるだけで高品質なプロンプトを生成してくれる。
*   **Interactive Tutorial**: `anthropics/prompt-eng-interactive-tutorial` (GitHub) - 実際に手を動かして学べるチュートリアル。
