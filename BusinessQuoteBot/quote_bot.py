import os
import json
import random
import datetime

# Configuration
VAULT_ROOT = r"c:/Users/chatg/Obsidian Vault/papa"
DAILY_DIR = os.path.join(VAULT_ROOT, "daily")
DATA_FILE = os.path.join(VAULT_ROOT, "BusinessQuoteBot", "quotes.json")

def main():
    print("=== BusinessQuoteBot Running ===")
    
    # Load Quotes
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            quotes = json.load(f)
    except Exception as e:
        print(f"Error loading quotes: {e}")
        return

    # Select Random Quote
    quote = random.choice(quotes)
    content = f"\n## 💡 Morning Motivation\n> **\"{quote['text']}\"**\n> — *{quote['author']}*\n"

    # Determine Target Date (Today)
    # Note: If running at 05:00, we target Today.
    target_date = datetime.date.today()
    daily_file = os.path.join(DAILY_DIR, f"{target_date.strftime('%Y-%m-%d')}.md")

    # Update Daily Note
    if os.path.exists(daily_file):
        # Check if already added? 
        # Simple check: search for "Morning Motivation"
        with open(daily_file, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        
        if "Morning Motivation" not in existing_content:
            with open(daily_file, 'a', encoding='utf-8') as f:
                f.write(content)
            print(f"Quote added to {daily_file}")
        else:
            print("Quote already exists for today.")
    else:
        # If daily note doesn't exist, create it?
        # Calendar sync usually creates it, or we create it.
        # Let's create it if missing.
        print(f"Creating new daily note: {daily_file}")
        with open(daily_file, 'w', encoding='utf-8') as f:
            f.write(f"# {target_date.strftime('%Y-%m-%d')}\n")
            f.write(content)

if __name__ == "__main__":
    main()
