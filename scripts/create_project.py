import os
import shutil
import sys
import datetime
import urllib.request

# Configuration
VAULT_ROOT = r"c:/Users/chatg/Obsidian Vault/papa"
TEMPLATE_PATH = os.path.join(VAULT_ROOT, "Templates", "Project_Plan.md")
PROJECTS_ROOT = VAULT_ROOT 

def main():
    print("=== 新しいプロジェクトを作成します ===")
    project_name = input("プロジェクト名を入力してください: ").strip()
    
    if not project_name:
        print("キャンセルされました。")
        return

    # Create Project Directory
    project_dir = os.path.join(PROJECTS_ROOT, project_name)
    if os.path.exists(project_dir):
        print(f"エラー: フォルダ '{project_name}' は既に存在します。")
        os.system("pause")
        return

    try:
        os.makedirs(project_dir)
        print(f"フォルダを作成しました: {project_dir}")
        
        # Copy Template
        # Using specific name for the plan
        note_name = f"{project_name}_Project_Plan.md" # Changed to be more explicit
        plan_file = os.path.join(project_dir, note_name)
        
        if os.path.exists(TEMPLATE_PATH):
            with open(TEMPLATE_PATH, 'r', encoding='utf-8') as src:
                content = src.read()
            
            # Replace placeholders
            content = content.replace("[Project Name]", project_name)
            content = content.replace("YYYY-MM-DD", datetime.date.today().strftime('%Y-%m-%d'))
            
            with open(plan_file, 'w', encoding='utf-8') as dst:
                dst.write(content)
            print(f"計画書を作成しました: {note_name}")
            
            # Create Agent Shortcuts
            create_shortcuts(project_dir)
            
            # Open in Obsidian using Absolute Path Logic
            # This handles cases where 'vault name' is ambiguous
            encoded_path = urllib.request.pathname2url(plan_file)
            # Remove initial slash if present on Windows (pathname2url adds ///C:/...)
            # Actually obsidian://open?path=... handles file:/// URI usually, 
            # but let's be safer: construct path param.
            # pathname2url returns ///C|/... or similar on windows depending on ver.
            # Simpler: just use quote on the string
            import urllib.parse
            # Force forward slashes
            safe_path = plan_file.replace('\\', '/')
            encoded_path = urllib.parse.quote(safe_path)
            
            uri = f"obsidian://open?path={encoded_path}"
            
            print(f"Obsidianで開いています... ({uri})")
            os.system(f"start \"\" \"{uri}\"")
            
        else:
            print(f"エラー: テンプレートファイルが見つかりません ({TEMPLATE_PATH})")
            os.system("pause")
    
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        os.system("pause")
    
    # 完了
    # Batch file has pause, so we don't need it here unless run directly
    # But adding it ensures user sees errors if run via double click on py file
    # print("完了しました。")
    print("完了しました。")
    create_shortcuts(project_dir)

def create_shortcuts(project_dir):
    """
    Creates shortcuts (bat files) to the agent scripts in the new project directory.
    This allows easy access to agents from the project folder.
    """
    agent_scripts = {
        "Run_Research_Agent": r"..\scripts\asp_monitor\run_research_agent.bat",
        "Run_Ideation_Agent": r"..\scripts\ideation\run_ideation_agent.bat",
        "Run_SNS_Agent": r"..\scripts\sns\run_sns_agent.bat",
        "Run_Content_Agent": r"..\scripts\content\run_content_agent.bat",
        "Run_Design_Agent": r"..\scripts\design\run_design_agent.bat",
        "Run_Strategist_Agent": r"..\scripts\strategy\run_strategist.bat"
    }
    
    print("\n--- エージェントへのショートカットを作成中 ---")
    for name, relative_target in agent_scripts.items():
        bat_name = os.path.join(project_dir, f"{name}.bat")
        
        # We use 'call' and absolute path or relative path from project dir
        # Since project dir is at root level (e.g. papa/ProjectA),
        # scripts are at papa/scripts/...
        # So ..\scripts\... should work fine.
        
        # We need to make sure the target bat file chdirs to its own location,
        # which our written bat files do (cd /d "%~dp0").
        
        content = f"@echo off\n"
        content = content + f"echo Calling {name}...\n"
        content = content + f"call \"{relative_target}\"\n"
        
        try:
            with open(bat_name, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"作成: {name}.bat")
        except Exception as e:
            print(f"失敗: {name}.bat ({e})")

if __name__ == "__main__":
    main()
