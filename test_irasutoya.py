# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import re
import json

def search_irasutoya(query):
    url = f"https://www.irasutoya.com/search?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
    
    # Extract entry links
    entries = re.findall(r'<a href=\'(https://www.irasutoya.com/\d{4}/\d{2}/[^\']+\.html)\'>', html)
    print(f"Query: {query}, Found entries: {len(entries)}")
    
    # For the first entry, get the high-res PNG image
    if entries:
        req_entry = urllib.request.Request(entries[0], headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req_entry, timeout=10) as resp_e:
            entry_html = resp_e.read().decode("utf-8", errors="ignore")
        
        # Blogspot image pattern
        # usually in <div class="separator"><a href="https://.../s1600/....png">
        img_urls = re.findall(r'<a href=\"(https://[^\"]+bp\.blogspot\.com/[^\"]+/s1600/[^\"]+\.png)\"', entry_html)
        if not img_urls:
            img_urls = re.findall(r'<img [^>]*src=\"(https://[^\"]+bp\.blogspot\.com/[^\"]+\.png)\"', entry_html)
        
        print(f"Found images in first entry: {img_urls[:2]}")
        return img_urls[0] if img_urls else None
    return None

if __name__ == "__main__":
    queries = ["満員電車", "行列 順番", "王冠", "エレベーター"]
    for q in queries:
        try:
            img = search_irasutoya(q)
            print(f"Result for {q}: {img}")
        except Exception as e:
            print(f"Error on {q}: {e}")
