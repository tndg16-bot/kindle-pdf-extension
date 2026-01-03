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

# List of 10 source files (Mixing Gmail clippings and normal clippings)
SOURCE_FILES = [
    r"Apps/remotely-save/papa/Gmail/20251124-070300_AI×仕組み化で初年度から2000万以上稼いできた私が考える”最も幸せになる方法.md",
    r"Apps/remotely-save/papa/Gmail/20251125-070345_最強のモチベUP方法をひらめきました。365日ずっと鬼行動できる方法。.md",
    r"Apps/remotely-save/papa/Gmail/20251126-071041_放置で”着金額を増やし続けるマネーマシン”を量産する私の仕組み化フロー.md",
    r"Apps/remotely-save/papa/Gmail/20251127-070921_75,000円のステッパーで作業効率＋月収が3倍以上に爆上がりした件.md",
    r"Apps/remotely-save/papa/Gmail/20251128-180842_スピードを速めるだけで無双できる話.md",
    r"Apps/remotely-save/papa/Gmail/20251130-070841_「ネットビジネスで自動化・仕組み化はもう厳しくなってきている・・・」.md",
    r"Apps/remotely-save/papa/Gmail/20251201-181044_いいからさっさと売ってみろ。.md",
    r"Clippings/【AI×癒し風景動画】圧倒的な収益化が可能となる癒しの風景動画をわずか10分で作成する方法を完全再現  RxB(アルビー).md",
    r"Clippings/【ゼロから始める】ハイクオリティなAI動画を簡単に作る方法【Midjourney×Runway】  RxB(アルビー).md",
    r"Apps/remotely-save/papa/Gmail/20251214-120722_10人中10人が釘刺しになる最強のライティングとは？.md"
]

def load_template():
    try:
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Template not found at {TEMPLATE_PATH}")
        sys.exit(1)

def read_source_file(rel_path):
    abs_path = os.path.join(VAULT_ROOT, rel_path)
    try:
        with open(abs_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Limit content size to avoid context limit issues (roughly first 2000 chars)
            return content[:2000] 
    except FileNotFoundError:
        print(f"Skipping (not found): {rel_path}")
        return None

def query_ollama(prompt):
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False # No streaming for bulk processing to keep output clean
    }
    
    headers = {'Content-Type': 'application/json'}
    req = urllib.request.Request(
        OLLAMA_API_URL, 
        data=json.dumps(data).encode('utf-8'), 
        headers=headers
    )

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get("response", "")
    except urllib.error.URLError as e:
        print(f"Error connecting to Ollama: {e}")
        return None

def main():
    print("=== 🔄 Bulk SNS Post Generator ===")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"Bulk_Tweet_Batch_{timestamp}.md"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    template = load_template()
    
    with open(output_path, 'w', encoding='utf-8') as f_out:
        f_out.write(f"# Bulk SNS Drafts - {timestamp}\n\n")
        
        for i, rel_path in enumerate(SOURCE_FILES, 1):
            print(f"Processing ({i}/10): {os.path.basename(rel_path)}...")
            
            content = read_source_file(rel_path)
            if not content: continue
            
            prompt = template.replace("{{USER_TOPIC}}", content)
            response = query_ollama(prompt)
            
            if response:
                source_name = os.path.basename(rel_path)
                f_out.write(f"## {i}. Source: {source_name}\n\n")
                f_out.write(response)
                f_out.write("\n\n---\n\n")
                f_out.flush()
            else:
                f_out.write(f"## {i}. Failed to generate for {os.path.basename(rel_path)}\n\n")
                f_out.flush()

    print(f"\n✅ Done! Check the output file: {output_path}")

if __name__ == "__main__":
    main()
