import argparse
from duckduckgo_search import DDGS
import json

def search(query, max_results=5):
    """
    Performs a web search using DuckDuckGo.
    """
    print(f"🕵️ Searching for: {query}...")
    results = []
    try:
        with DDGS() as ddgs:
            # text search
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r['title'],
                    "link": r['href'],
                    "snippet": r['body']
                })
    except Exception as e:
        return {"error": str(e)}

    return results

def main():
    parser = argparse.ArgumentParser(description="Web Search Skill")
    parser.add_argument("query", type=str, help="Search query")
    parser.add_argument("--count", type=int, default=3, help="Number of results")
    args = parser.parse_args()

    results = search(args.query, args.count)
    
    # Output JSON for the Agent to consume
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
