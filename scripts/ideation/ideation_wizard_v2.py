import os
import sys
import json
import urllib.request
import urllib.error
import datetime

# Configuration
VAULT_ROOT = r"c:/Users/chatg/Obsidian Vault/papa"
TEMPLATE_PATH = os.path.join(VAULT_ROOT, "Templates", "Spec_Generator_Prompt.md")
OUTPUT_DIR = os.path.join(VAULT_ROOT, "Idea_Lab")
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3" # Ensure this model is pulled in Ollama

def load_template():
    try:
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Template not found at {TEMPLATE_PATH}")
        sys.exit(1)

def query_ollama(prompt):
    """
    Sends prompt to Ollama and streams the response.
    """
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

    full_response = ""
    
    print(f"\n🤖 {MODEL_NAME} is thinking...\n")
    print("-" * 50)

    try:
        with urllib.request.urlopen(req) as response:
            for line in response:
                if line:
                    decoded_line = line.decode('utf-8')
                    try:
                        json_obj = json.loads(decoded_line)
                        chunk = json_obj.get("response", "")
                        
                        # Print to console immediately (streaming)
                        print(chunk, end='', flush=True)
                        
                        full_response += chunk
                        
                        if json_obj.get("done", False):
                            break
                    except json.JSONDecodeError:
                        continue
    except urllib.error.URLError as e:
        print(f"\n\n🛑 Error connecting to Ollama: {e}")
        print("Please ensure Ollama is running (run 'ollama serve' in a terminal).")
        return None
        
    print("\n" + "-" * 50)
    return full_response

def main():
    print("=== 💡 Antigravity Ideation Agent (Powered by Ollama) ===")
    print("AIと対話しながら、最強の仕様書を作りましょう。\n")

    idea = input("Q1. どんなアプリ/ツールを作りたいですか？: ").strip()
    if not idea: 
        print("アイデアが入力されませんでした。終了します。")
        return

    audience = input("\nQ2. 誰が使いますか？（ターゲット層）: ").strip()
    if not audience: audience = "一般ユーザー"

    # Verify Ollama connection check (simple check)
    try:
        urllib.request.urlopen("http://localhost:11434", timeout=1)
    except urllib.error.URLError:
        print("\n⚠️  Warning: Ollama connection failed. Is it running?")
        print("Run 'ollama serve' or start the Ollama app first.")
        # We continue, let query_ollama handle the actual error gracefully

    # Prepare Prompt
    raw_template = load_template()
    final_prompt = raw_template.replace("{{USER_IDEA}}", idea).replace("{{TARGET_AUDIENCE}}", audience)
    
    # Generate
    result = query_ollama(final_prompt)
    
    if result:
        # Save to file
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = idea[:10].replace(" ", "_").replace("/", "_").replace(":", "").replace("?", "")
        filename = f"Spec_{timestamp}_{safe_name}.md"
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)
            
        print(f"\n✅ 仕様書を保存しました: {output_path}")
        print("Claude Code 等を使って、すぐに開発を始められます！")

    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    main()
