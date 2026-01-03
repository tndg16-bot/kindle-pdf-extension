import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import datetime
import os
import argparse
import sys
import ssl

def fetch_rss(keyword):
    """
    Fetches RSS feed from Google News for a given keyword.
    """
    base_url = "https://news.google.com/rss/search"
    params = {
        "q": keyword,
        "hl": "ja",
        "gl": "JP",
        "ceid": "JP:ja"
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    print(f"Fetching news for: {keyword}...")
    
    try:
        # Create a context that doesn't verify SSL certificates (optional, but helps in some local envs)
        # For production use, verify=True is better, but standard urllib context is strict.
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=context) as response:
            return response.read()
    except Exception as e:
        print(f"Error fetching {keyword}: {e}")
        return None

def parse_rss(xml_data):
    """
    Parses RSS XML data and returns a list of dictionaries.
    """
    items = []
    if not xml_data:
        return items
        
    try:
        root = ET.fromstring(xml_data)
        for item in root.findall(".//item"):
            title = item.find("title").text
            link = item.find("link").text
            pub_date = item.find("pubDate").text
            
            # Simple date parsing/formatting if needed, or keep raw
            # Google News date format: "Mon, 01 Jan 2026 12:00:00 GMT"
            items.append({
                "title": title,
                "link": link,
                "pub_date": pub_date
            })
    except Exception as e:
        print(f"Error parsing XML: {e}")
        
    return items

def load_existing_links(filepath):
    """
    Reads the output file to find already logged links to prevent duplicates.
    """
    existing_links = set()
    if not os.path.exists(filepath):
        return existing_links
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if "](" in line and ")" in line:
                    # Extract URL from markdown link [Title](URL)
                    parts = line.split("](")
                    if len(parts) > 1:
                        url_part = parts[1].split(")")[0]
                        existing_links.add(url_part)
    except Exception as e:
        print(f"Error reading existing file: {e}")
        
    return existing_links

def main():
    parser = argparse.ArgumentParser(description="Google News RSS Fetcher for Antigravity Research Agent")
    parser.add_argument("--keywords", nargs="+", help="List of keywords to search for", required=True)
    parser.add_argument("--output", help="Path to the output Markdown file", required=True)
    
    args = parser.parse_args()
    
    existing_links = load_existing_links(args.output)
    
    new_entries = []
    
    for keyword in args.keywords:
        xml_data = fetch_rss(keyword)
        items = parse_rss(xml_data)
        
        count = 0
        for item in items:
            if item["link"] not in existing_links:
                new_entries.append(item)
                existing_links.add(item["link"]) # Add to set to prevent dupes within same run
                count += 1
                if count >= 5: # Limit to top 5 new items per keyword to avoid flooding
                    break
    
    if new_entries:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        with open(args.output, 'a', encoding='utf-8') as f:
            f.write(f"\n## 📅 Checked: {timestamp}\n")
            for entry in new_entries:
                f.write(f"- [{entry['title']}]({entry['link']}) ({entry['pub_date']})\n")
            f.write("\n---\n")
            
        print(f"Success! Added {len(new_entries)} new articles to {args.output}")
    else:
        print("No new articles found.")

if __name__ == "__main__":
    main()
