import requests
import json
import subprocess
import os
import winsound  # For notification

# Configuration
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL = "llama3"

def run_skill(skill_name, args):
    """
    Executes a python script in scripts/skills/
    """
    skill_path = os.path.join(os.path.dirname(__file__), "../../skills", f"{skill_name}.py")
    if not os.path.exists(skill_path):
        return f"Error: Skill {skill_name} not found."
    
    # Construct command
    cmd = ["python", skill_path] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        return result.stdout.strip()
    except Exception as e:
        return f"Error executing skill: {e}"

def chat_with_tools(prompt):
    """
    Sends prompt to Llama3 with instructions to use tools.
    """
    system_prompt = """
    あなたはツールを活用できる有能なAIアシスタントです。
    以下のツールを使用できます:
    - web_search(query): ウェブ検索を行い、結果リスト（タイトル・URL）を取得します。
    - scrape_url(url): 指定したURLのページ本文を読み込みます。
    
    質問に対して、まず検索が必要なら `web_search` を使い、その結果から詳しく読むべきページがあれば `scrape_url` を使ってください。
    
    ツールを使用する場合は、必ず以下の形式のJSONオブジェクトのみを出力してください:
    {"tool": "ツール名", "args": ["引数"]}
    
    例:
    {"tool": "web_search", "args": ["最新のiPhone情報"]}
    {"tool": "scrape_url", "args": ["https://example.com/news"]}
    
    既に十分な情報がある場合、または挨拶などは、普通に日本語で回答してください。
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    max_turns = 5
    turn = 0
    
    print(f"🏁 Agent Task Started: {prompt}")
    
    while turn < max_turns:
        turn += 1
        
        # Format conversation history for Llama3 (Simple prompt concatenation for now)
        # Ideally use chat history API if model supports it, but Llama3 often likes a single prompt block.
        # We'll just construct a fresh prompt with history appended.
        
        history_text = ""
        for m in messages:
            if m["role"] == "tool_output":
                history_text += f"\n[Tool Output]: {m['content']}\n"
            elif m["role"] == "assistant":
                history_text += f"\nAI: {m['content']}\n"
            elif m["role"] == "user":
                history_text += f"\nUser: {m['content']}\n"
            elif m["role"] == "system":
                # System prompt is base
                pass
                
        full_prompt = f"{system_prompt}\n{history_text}\nAI:"
        
        payload = {
            "model": MODEL,
            "prompt": full_prompt,
            "stream": False,
            "format": "json" 
        }
        
        try:
            response = requests.post(OLLAMA_API, json=payload)
            response.raise_for_status()
            result = response.json()
            response_text = result.get("response", "")
            
            print(f"🤖 AIの思考 (Turn {turn}): {response_text}")
            
            # Record assistant thought
            messages.append({"role": "assistant", "content": response_text})

            try:
                tool_call = json.loads(response_text)
                if "tool" in tool_call:
                    tool = tool_call["tool"]
                    args = tool_call.get("args", [])
                    if isinstance(args, str): args = [args]
                    
                    print(f"🛠️ ツール実行: {tool} 引数: {args}")
                    tool_output = run_skill(tool, args)
                    tool_output_snippet = tool_output[:300] + "..." if len(tool_output) > 300 else tool_output
                    print(f"📄 実行結果 (Length {len(tool_output)}): {tool_output_snippet}")
                    
                    # Add tool output to history
                    messages.append({"role": "tool_output", "content": tool_output})
                    # Loop continues...
                    
                else:
                    # JSON but no tool? Maybe final answer in JSON?
                    # Or simple thought?
                    # If it looks like a final answer (no tool), break.
                     break
                     
            except json.JSONDecodeError:
                # Text output (Final Answer)
                print(f"💬 最終回答: {response_text}")
                break
                
        except Exception as e:
            print(f"Error: {e}")
            break
            
    except Exception as e:
        return f"Error calling Ollama: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        p = sys.argv[1]
    else:
        p = "What is the latest version of Obsidian?"
    
    chat_with_tools(p)
    
    # Notify completion
    print("🔔 Task Completed!")
    winsound.Beep(1000, 500) # 1000Hz, 500ms
