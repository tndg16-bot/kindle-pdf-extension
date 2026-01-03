import os
import sys
import json
import urllib.request
import urllib.error
import datetime

# Configuration
VAULT_ROOT = r"c:/Users/chatg/Obsidian Vault/papa"
TEMPLATE_PATH = os.path.join(VAULT_ROOT, "Templates", "Design_Prompt.md")
OUTPUT_DIR = os.path.join(VAULT_ROOT, "Design_Lab")
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
        "stream": True # Streaming for cool effect
    }
    
    headers = {'Content-Type': 'application/json'}
    req = urllib.request.Request(
        OLLAMA_API_URL, 
        data=json.dumps(data).encode('utf-8'), 
        headers=headers
    )

    full_response = ""
    print(f"\n🎨 {MODEL_NAME} is designing...\n")
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
    print("=== 🎨 Antigravity Designer Agent (Powered by Ollama) ===")
    print("あなたのアイデアを、最強の画像生成プロンプトやデザインコードに変換します。\n")

    concept = input("Q1. デザインのコンセプトや作りたい画像のイメージは？: ").strip()
    if not concept: return

    print("\nQ2. 出力先のAI/形式を選んでください:")
    print("1. Midjourney (Keywords)")
    print("2. DALL-E 3 (Natural Language)")
    print("3. Web Design (CSS/Colors)")
    
    mode_input = input("番号を入力 [1]: ").strip()
    
    target_output = "MIDJOURNEY"
    if mode_input == "2":
        target_output = "DALLE3"
    elif mode_input == "3":
        target_output = "WEB_DESIGN"

    # Prepare Prompt
    raw_template = load_template()
    final_prompt = raw_template.replace("{{USER_CONCEPT}}", concept).replace("{{TARGET_OUTPUT}}", target_output)
    
    # Generate
    result = query_ollama(final_prompt)
    
    if result:
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = concept[:10].replace(" ", "_").replace("/", "_")
        filename = f"Design_{target_output}_{timestamp}_{safe_name}.md"
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)
            
        print(f"\n✅ デザイン案を保存しました: {output_path}")

    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    main()
