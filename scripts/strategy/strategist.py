import os
import sys
import json
import urllib.request
import urllib.error
import glob

# Configuration
VAULT_ROOT = r"c:/Users/chatg/Obsidian Vault/papa"
PERSONA_PROFILE = os.path.join(VAULT_ROOT, "Templates", "Motoyama_Profile.md")
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

# Limit search scope to avoid scanning entire drive (can be customized)
# Searching mainly in 'note' (manuals?), 'BusinessQuoteBot' (project specs?), 'Clippings'
SEARCH_DIRS = [
    os.path.join(VAULT_ROOT, "note"),
    os.path.join(VAULT_ROOT, "Clippings"),
    os.path.join(VAULT_ROOT, "Templates"),
    os.path.join(VAULT_ROOT, "Community_Project")
]

def load_persona():
    try:
        with open(PERSONA_PROFILE, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Personality: Professional Business Coach."

def search_files(query_keywords):
    """
    Simple keyword search. Returns concatenation of relevant file snippets.
    For a real production system, we'd use a Vector DB (ChromaDB/FAISS),
    but for a local agent script, grep-like search is a good start.
    """
    relevant_context = []
    
    # Simple tokenization
    keywords = query_keywords.split()
    
    print(f"🔍 Searching vault for: {keywords} ...")
    
    for d in SEARCH_DIRS:
        # Recursive search in these dirs
        for root, _, files in os.walk(d):
            for file in files:
                if file.endswith(".md"):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Check if ALL keywords exist (AND search) or ANY (OR search)
                            # Let's do a simple score: count keyword occurrences
                            score = sum(content.count(k) for k in keywords)
                            if score > 0:
                                # Add file content (truncated if too long) as context
                                relevant_context.append(f"--- From: {file} ---\n{content[:2000]}\n")
                    except Exception:
                        continue
                        
    # Limit context size to avoid context overflow (approx top 3-5 matches)
    # Sort by "relevance" (not implemented deep here, just taking first few found)
    return "\n".join(relevant_context[:5])

def query_ollama(prompt):
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True
    }
    
    headers = {'Content-Type': 'application/json'}
    req = urllib.request.Request(
        OLLAMA_API_URL, 
        data=json.dumps(data).encode('utf-8'), 
        headers=headers
    )

    print(f"\n🧠 {MODEL_NAME} is thinking (Strategist Mode)...\n")
    print("-" * 50)

    try:
        with urllib.request.urlopen(req) as response:
            for line in response:
                if line:
                    decoded_line = line.decode('utf-8')
                    try:
                        json_obj = json.loads(decoded_line)
                        chunk = json_obj.get("response", "")
                        print(chunk, end='', flush=True)
                        if json_obj.get("done", False):
                            break
                    except json.JSONDecodeError:
                        continue
    except urllib.error.URLError as e:
        print(f"\n\n🛑 Error connecting to Ollama: {e}")

    print("\n" + "-" * 50)

def main():
    print("=== 🧠 Antigravity Strategist Agent ===")
    print("あなたのVault内の知識と人格プロファイルに基づき、戦略的アドバイスを行います。\n")

    question = input("Q. 相談内容や質問を入力してください: ").strip()
    if not question: return

    # 1. Retrieve Context
    context_data = search_files(question)
    if not context_data:
        print("⚠️ 関連するマニュアルやメモが見つかりませんでした。一般的な知識で回答します。")
        context_data = "(No local context found)"
    else:
        print(f"✅ 関連資料を発見しました。これらを参考に回答します。")

    # 2. Load Persona output
    persona = load_persona()

    # 3. Construct Prompt
    system_prompt = f"""
You are "Strategist Agent", acting as the user's second brain.
Your name and personality are defined below.

## Persona Profile
{persona}

## Knowledge Context (From User's Vault)
{context_data}

## User Question
{question}

## Instruction
Answer the question using the 'Knowledge Context' if relevant.
Adopt the tone and thinking style described in 'Persona Profile'.
Be practical, strategic, and concise.
"""
    
    # 4. Generate
    query_ollama(system_prompt)

    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    main()
