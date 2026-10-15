# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
import re
import os
import time

def fetch_one(query, out_name):
    url = f"https://www.irasutoya.com/feeds/posts/default?q={urllib.parse.quote(query)}&alt=json"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    with urllib.request.urlopen(req, timeout=10) as r:
        d = json.loads(r.read().decode("utf-8"))
    
    entries = d.get("feed", {}).get("entry", [])
    if not entries:
        print(f"No entry for {query}")
        return None
    
    e = entries[0]
    title = e.get("title", {}).get("$t")
    print(f"Query '{query}' -> Title: {title}")
    
    # Check media$thumbnail or content
    thumb = e.get("media$thumbnail", {}).get("url")
    content = e.get("content", {}).get("$t", "")
    
    img_url = None
    # Look for original png in content
    matches = re.findall(r'(https://[^\"]+bp\.blogspot\.com/[^\"]+\.png)', content)
    if matches:
        img_url = matches[0]
    elif thumb:
        img_url = thumb
    
    if img_url:
        # Scale up to /s800/
        img_url = re.sub(r'/s\d+[^/]*/', '/s800/', img_url)
        os.makedirs("assets/irasutoya", exist_ok=True)
        dest = os.path.join("assets/irasutoya", out_name)
        req_img = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req_img, timeout=10) as resp, open(dest, "wb") as f:
            f.write(resp.read())
        print(f"  -> Saved {dest} ({os.path.getsize(dest)} bytes)")
        return dest
    return None

if __name__ == "__main__":
    targets = [
        ("満員電車", "crowded_train.png"),    # Crowded train -> Sorted array O(N) shift
        ("行列", "queue_line.png"),            # Queue line -> Priority queue waiting
        ("王様", "king_crown.png"),            # King with crown -> Root element in O(1)
        ("エレベーター", "elevator.png"),      # Elevator -> Sift-up bubble up
    ]
    for q, fn in targets:
        try:
            fetch_one(q, fn)
            time.sleep(1.5)
        except Exception as err:
            print(f"Error {q}: {err}")

