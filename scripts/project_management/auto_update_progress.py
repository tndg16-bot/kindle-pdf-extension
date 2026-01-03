import os
import datetime
import glob

# Configuration
VAULT_ROOT = r"c:/Users/chatg/Obsidian Vault/papa"
EXCLUDE_DIRS = {'.git', '.obsidian', 'scripts', 'Templates', 'node_modules'}

def get_modified_files(project_dir, days=1):
    """Returns a list of files modified within the last 'days'."""
    modified_files = []
    threshold = datetime.datetime.now().timestamp() - (days * 86400)
    
    for root, dirs, files in os.walk(project_dir):
        # Remove excluded dirs to prevent recursion
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            filepath = os.path.join(root, file)
            try:
                mtime = os.path.getmtime(filepath)
                if mtime > threshold:
                    # Don't list the plan file itself if it was just updated
                    if file.endswith("_Project_Plan.md") or file == "Plan.md":
                        continue
                    # Relative path for readability
                    rel_path = os.path.relpath(filepath, project_dir)
                    modified_files.append(rel_path)
            except OSError:
                continue
                
    return modified_files

def update_plan_file(plan_path, modified_files):
    """Appends a new row to the Daily Log section."""
    today = datetime.date.today().strftime('%Y-%m-%d')
    
    if not modified_files:
        # Optional: Log "No changes" or just skip?
        # User might want confirmation that it ran.
        status = "変化なし"
        comment = "変更されたファイルはありませんでした。"
    else:
        status = "進行中"
        # Determine strict file list or count
        if len(modified_files) > 3:
            comment = f"{len(modified_files)}個のファイルを更新 ({', '.join(modified_files[:3])}...)"
        else:
            comment = f"ファイルを更新: {', '.join(modified_files)}"
    
    # Read file
    with open(plan_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Check if entry for today already exists? (To prevent duplicate runs in same day appending multiple lines)
    # Simple check: Look at last few lines.
    
    # Find the table end or append position.
    # Looking for the table header | 日付 |...
    
    table_header_found = False
    insert_index = -1
    
    for i, line in enumerate(lines):
        if "| 日付 | ステータス | AIコメント |" in line:
            table_header_found = True
        if table_header_found and line.strip() == "":
            # End of table (empty line)
            insert_index = i
            # But wait, sometimes there is no empty line at end of file.
            break
    
    if insert_index == -1 and table_header_found:
        insert_index = len(lines) # Append to end
        
    if table_header_found:
        # Check if today is already logged in the last few lines
        # (Naive check)
        already_logged = False
        for line in lines[max(0, insert_index-5):insert_index]:
            if today in line:
                already_logged = True
                break
        
        if not already_logged:
            new_line = f"| {today} | {status} | {comment} |\n"
            lines.insert(insert_index, new_line)
            
            with open(plan_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"Updated: {plan_path} with status '{status}'")
        else:
            print(f"Skipped: {plan_path} (Already logged for today)")
    else:
        print(f"Skipped: {plan_path} (Table not found)")

def main():
    print("=== プロジェクト進捗自動更新を開始します ===")
    
    # Find all project plan files
    # Heuristic: Looks for files ending in _Project_Plan.md or named Plan.md in subdirectories
    for root, dirs, files in os.walk(VAULT_ROOT):
        # Exclude
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if file.endswith("_Project_Plan.md") or file == "Plan.md":
                # Found a project plan
                # The project directory is the folder containing this file
                project_dir = root
                plan_path = os.path.join(root, file)
                
                print(f"Checking project: {project_dir}")
                modified = get_modified_files(project_dir)
                update_plan_file(plan_path, modified)

    print("=== 完了 ===")

if __name__ == "__main__":
    main()
