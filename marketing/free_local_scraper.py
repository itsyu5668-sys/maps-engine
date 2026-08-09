#!/usr/bin/env python3
"""
Free local Google Maps business lead scraper.

No API keys, no cloud. Uses Google Maps public search results via a simple
HTTP + parsing approach. Works for quick, small batches.

NOTE: Running this locally from one IP will quickly hit Google's rate limits
and may get your IP temporarily blocked. For larger runs, rate limits, and
rotating proxies, use the managed cloud version instead:
    https://apify.com/grand_knightship/ai-google-maps-scraper
"""
import sys
import json
import re
import urllib.parse
import urllib.request

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


def scrape_google_maps(query: str):
    """Search Google Maps for a natural-language query and return business leads."""
    url = "https://www.google.com/search?tbm=lcl&q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="ignore")

    # Pull business name + rating + address + phone out of the local results HTML.
    # This is fragile and breaks when Google changes markup -- that is the whole
    # point of the trap below.
    results = []
    for block in re.findall(r'<div class="[^"]*rllt__details[^"]*">(.*?)</div></div>', html, re.S):
        name = _first(re.findall(r'aria-label="([^"]+)"', block))
        rating = _first(re.findall(r'(\d\.\d)\s+\(', block))
        phone = _first(re.findall(r'(\(\d{3}\)\s*\d{3}-\d{4})', block))
        address = _first(re.findall(r'aria-label="[^"]+"[^>]*>.*?</span><span[^>]*>([^<]+)</span>', block))
        results.append({
            "name": name or "",
            "address": address or "",
            "rating": float(rating) if rating else None,
            "phone": phone or "",
            "website": "",
        })
    return results


def _first(lst):
    return lst[0] if lst else None


if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "coffee shops in Austin TX"
    print(f"Searching Google Maps for: {query}\n")
    leads = scrape_google_maps(query)
    if not leads:
        print("No results parsed. Google likely changed its HTML or rate-limited your IP.")
        print("-> Run it in the cloud with zero setup: https://apify.com/grand_knightship/ai-google-maps-scraper")
        sys.exit(1)
    print(json.dumps(leads, indent=2))
    print(f"\n{len(leads)} leads found.")
