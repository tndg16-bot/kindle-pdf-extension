import os
import sys

# Configuration
VAULT_ROOT = r"c:/Users/chatg/Obsidian Vault/papa"
TEMPLATE_PATH = os.path.join(VAULT_ROOT, "Templates", "Spec_Generator_Prompt.md")
OUTPUT_DIR = os.path.join(VAULT_ROOT, "Idea_Lab") # New folder for ideas

def main():
    print("=== アイデア具体化ウィザード ===")
    print("あなたの「ふんわりしたアイデア」を最強の仕様書に変換します。")
    
    idea = input("\nQ1. どんなアプリ/ツールを作りたいですか？: ").strip()
    if not idea: return
    
    audience = input("\nQ2. 誰が使いますか？（ターゲット層）: ").strip()
    if not audience: audience = "一般ユーザー"
    
    # Read Template
    try:
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        print("エラー: テンプレートが見つかりません。")
        return

    # Fill Template
    prompt = template.replace("{{USER_IDEA}}", idea).replace("{{TARGET_AUDIENCE}}", audience)
    
    # Save the prompt
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    safe_name = idea[:10].replace(" ", "_").replace("/", "_")
    output_file = os.path.join(OUTPUT_DIR, f"Prompt_for_{safe_name}.txt")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
        
    print(f"\n完了！以下のファイルに「AIへの命令書」を生成しました。")
    print(f"👉 {output_file}")
    
    print("\n--- 次のアクション ---")
    print("1. このファイルの中身をコピーして、Claude や ChatGPT に貼り付けてください。")
    print("2. AIが詳細な仕様書を出力してくれます。")
    print("3. 気に入ったら `Start_New_Project.bat` でプロジェクト化しましょう！")
    
    os.system("pause")

if __name__ == "__main__":
    main()
