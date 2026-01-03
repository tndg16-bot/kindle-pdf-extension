import os
import sys
import json
import urllib.request
import urllib.error
import datetime

# Configuration
VAULT_ROOT = r"c:/Users/chatg/Obsidian Vault/papa"
TEMPLATE_PATH = os.path.join(VAULT_ROOT, "Templates", "Blog_Post_Prompt.md")
OUTPUT_DIR = os.path.join(VAULT_ROOT, "Content_Drafts")
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
    print(f"\n✍️  {MODEL_NAME} is writing your article...\n")
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
    print("=== 📝 Antigravity Content Agent (Powered by Ollama) ===")
    print("あなたの文体を模倣したブログ記事/コンテンツを作成します。\n")

    topic = input("Q1. 記事のテーマは何ですか？: ").strip()
    if not topic: return

    audience = input("\nQ2. ターゲット読者は誰ですか？(例: 初心者、経営者): ").strip()
    if not audience: audience = "一般読者"

    print("\nQ3. 文体の参考にしたいテキスト（過去の執筆記事など）があれば貼り付けてください。")
    print("    (なければ Enter でスキップ)")
    print("    入力を終了するには、新しい行で Ctrl+Z (Windows) または Ctrl+D (Mac/Linux) を押してください。")
    
    style_lines = []
    try:
        while True:
            line = input()
            style_lines.append(line)
    except EOFError:
        pass
    
    style_reference = "\n".join(style_lines).strip()
    if not style_reference:
        style_reference = "Standard professional tone."

    # Prepare Prompt
    raw_template = load_template()
    final_prompt = raw_template.replace("{{USER_TOPIC}}", topic)\
                               .replace("{{TARGET_AUDIENCE}}", audience)\
                               .replace("{{STYLE_REFERENCE}}", style_reference)
    
    # Generate
    result = query_ollama(final_prompt)
    
    if result:
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = topic[:10].replace(" ", "_").replace("/", "_")
        filename = f"Article_{timestamp}_{safe_name}.md"
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)
            
        print(f"\n✅ 記事ドラフトを保存しました: {output_path}")

    print("\nPress Enter to exit...")
    input()
    # Dummy input to keep window open if double-clicked logic wasn't enough
    sys.stdin.read(1)

if __name__ == "__main__":
    main()
