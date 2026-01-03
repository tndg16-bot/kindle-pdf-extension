import os
import sys
import json
import urllib.request
import urllib.error
import datetime

# Configuration
VAULT_ROOT = r"c:/Users/chatg/Obsidian Vault/papa"
TEMPLATE_PATH = os.path.join(VAULT_ROOT, "Templates", "SNS_Post_Prompt.md")
OUTPUT_DIR = os.path.join(VAULT_ROOT, "SNS_Drafts")
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

def load_template():
    try:
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Template not found at {TEMPLATE_PATH}")
        sys.exit(1)

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

    full_response = ""
    print(f"\n🐦 {MODEL_NAME} is drafting tweets...\n")
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
                        full_response += chunk
                        if json_obj.get("done", False):
                            break
                    except json.JSONDecodeError:
                        continue
    except urllib.error.URLError as e:
        print(f"\n\n🛑 Error connecting to Ollama: {e}")
        return None
        
    print("\n" + "-" * 50)
    return full_response

def main():
    print("=== 📣 Antigravity SNS Agent (Powered by Ollama) ===")
    print("X(Twitter)への投稿案を3パターン自動生成します。\n")

    topic = input("投稿したいテーマや、要約したい文章を入力してください: ").strip()
    if not topic: 
        print("入力がありませんでした。")
        return

    # Verify Ollama
    try:
        urllib.request.urlopen("http://localhost:11434", timeout=1)
    except urllib.error.URLError:
        print("\n⚠️  Warning: Ollama connection failed.")

    # Prepare Prompt
    raw_template = load_template()
    final_prompt = raw_template.replace("{{USER_TOPIC}}", topic)
    
    # Generate
    result = query_ollama(final_prompt)
    
    if result:
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = topic[:10].replace(" ", "_").replace("/", "_").replace("\n", "")
        filename = f"Tweet_{timestamp}_{safe_name}.md"
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)
            
        print(f"\n✅ 下書きを保存しました: {output_path}")

    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    main()
