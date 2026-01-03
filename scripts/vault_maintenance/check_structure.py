import os
import re
import datetime

# Configuration
VAULT_ROOT = r"c:/Users/chatg/Obsidian Vault/papa"
REPORT_FILE = os.path.join(VAULT_ROOT, "Vault_Maintenance_Report.md")
EXCLUDE_DIRS = {'.git', '.obsidian', 'scripts', 'Templates', 'node_modules', 'Apps'} # Apps might have code
EXCLUDE_EXTS = {'.py', '.js', '.css', '.html', '.json', '.xml', '.bat'}

def scan_vault(vault_root):
    all_files = set()
    linked_files = set()
    root_files = []
    
    # Simple regex for [[Link]] or [[Link|Alias]]
    link_pattern = re.compile(r'\[\[(.*?)(?:\|.*?)?\]\]')
    
    print("Vaultをスキャン中...")
    
    for root, dirs, files in os.walk(vault_root):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if any(file.endswith(ext) for ext in EXCLUDE_EXTS):
                continue
            
            # Record file existence
            # Note: Links usually refer to the filename without extension, or relative path.
            # For simplicity, we track 'Base Name' matching.
            filename = file
            basename = os.path.splitext(file)[0]
            
            rel_path = os.path.relpath(os.path.join(root, file), vault_root)
            all_files.add(basename) 
            
            # Check for Root Files
            if root == vault_root:
                root_files.append(file)
            
            # Scan content for links (only if text file)
            if file.endswith('.md') or file.endswith('.txt'):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        links = link_pattern.findall(content)
                        for link in links:
                            # Link might contain #header or /folder
                            clean_link = link.split('#')[0].split('/')[-1]
                            linked_files.add(clean_link)
                except Exception as e:
                    print(f"Error reading {file}: {e}")

    # Determine Orphans
    # Files that exist but are NOT in linked_files
    # Note: This is an approximation.
    orphans = []
    for f in all_files:
        if f not in linked_files:
            # Check if it's a daily note (usually orphans are okay for daily notes)
            if re.match(r'\d{4}-\d{2}-\d{2}', f):
                continue 
            orphans.append(f)
            
    return orphans, root_files

def generate_report(orphans, root_files):
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"# 🛠️ Vault 構造診断レポート\n")
        f.write(f"**作成日時**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        
        f.write("## ⚠️ 孤立ファイル (Orphans)\n")
        f.write("他のノートからリンクされていないファイルです（日報は除外）。\n")
        f.write(f"**合計: {len(orphans)}件**\n\n")
        for o in sorted(orphans):
            f.write(f"- [[{o}]]\n")
            
        f.write("\n## 📦 ルート直下のファイル (Root Files)\n")
        f.write("フォルダ整理の候補です。\n")
        f.write(f"**合計: {len(root_files)}件**\n\n")
        for r in sorted(root_files):
            f.write(f"- {r}\n")
            
    print(f"レポートを作成しました: {REPORT_FILE}")

def main():
    orphans, root_files = scan_vault(VAULT_ROOT)
    generate_report(orphans, root_files)
    
    # Open Report
    os.system(f"start \"\" \"{REPORT_FILE}\"")

if __name__ == "__main__":
    main()
