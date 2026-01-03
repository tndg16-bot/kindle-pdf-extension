# 📄 Skill: Local AI Processing (`ollama-process`)

This skill defines how Antigravity (PM) delegates heavy text processing to the Local AI (Ollama) to save costs.

## 🎯 Objective
Use the local Ollama instance (model: `llama3` or similar) to:
1.  Summarize long documentation.
2.  Parse error logs.
3.  Draft initial ideas.
*Goal: Reduce token usage for paid APIs (Claude).*

## 🛠️ Setup Steps (For User/PM)
1.  **Verify Ollama**: Ensure `ollama serve` is running.
2.  **Pull Model**: Run `ollama pull llama3` (or `mistral`, `gemma2`).
3.  **Test**: Run `ollama run llama3 "Hello"` to confirm response.

## 📜 Workflow (How to Delegate)
When you (Antigravity) encounter a large text file or log:
1.  **Do NOT** feed it to Claude immediately.
2.  **Execute**:
    ```bash
    type large_log.txt | ollama run llama3 "Summarize the error in this log concisely:" > summary.txt
    ```
3.  **Review**: Read `summary.txt`.
4.  **Escalate**: If the summary is clear, use it. Only if AI power is insufficient, pass the *summary* (not the full log) to Claude.

## ✅ Verification
- [ ] Model is downloaded.
- [ ] Command line pipe works (`echo "test" | ollama run...`).
- [ ] Response time is acceptable.
