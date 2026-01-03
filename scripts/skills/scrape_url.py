import argparse
import requests
from bs4 import BeautifulSoup
import json

def scrape(url):
    """
    Fetches and extracts main text from a URL.
    """
    print(f"📖 Reading: {url}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
            
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Truncate if too long (to fit in context)
        return text[:5000] 
        
    except Exception as e:
        return f"Error scraping URL: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Web Scraper Skill")
    parser.add_argument("url", type=str, help="URL to scrape")
    args = parser.parse_args()

    result = scrape(args.url)
    
    # Output content directly (or JSON wrap if preferred, but text is fine for LLM reading)
    # Wrapping in JSON to be consistent
    print(json.dumps({"content": result}, ensure_ascii=False))

if __name__ == "__main__":
    main()
