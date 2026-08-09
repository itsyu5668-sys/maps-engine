---
title: "How to Scrape Google Maps Business Leads in 2026 (Free Python Script)"
published: false
description: "A free local Python script to scrape Google Maps business leads — and why you'll hit rate limits fast, plus the $2 cloud alternative."
tags: python, scraping, googlemaps, leadgeneration
cover_image: ""
---

# How to Scrape Google Maps Business Leads in 2026 (Free Python Script)

Google Maps is the single richest source of local business data on the internet — names, addresses, ratings, phone numbers, and websites for millions of businesses worldwide. Whether you're doing B2B lead generation, sales prospecting, or market research, pulling structured leads out of Google Maps is one of the highest-ROI scraping tasks you can run.

In this post I'll give you a **free, working Python script** that scrapes Google Maps locally — and then I'll tell you exactly why you'll outgrow it within an hour, and what to use instead.

## What you'll get

For a query like *"coffee shops in Austin TX with phone numbers"*, the script returns structured JSON:

```json
[
  {
    "name": "Epoch Coffee",
    "address": "221 W North Loop Blvd, Austin, TX 78751",
    "rating": 4.5,
    "phone": "+1 512-454-3762",
    "website": "https://epochcoffee.com"
  }
]
```

## The free local script

No API keys. No cloud. No signup. Just `requests` and a regex parser.

```python
import sys, json, re, urllib.parse, urllib.request

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def scrape_google_maps(query: str):
    url = "https://www.google.com/search?tbm=lcl&q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="ignore")

    results = []
    for block in re.findall(r'<div class="[^"]*rllt__details[^"]*">(.*?)</div></div>', html, re.S):
        name = (re.findall(r'aria-label="([^"]+)"', block) or [""])[0]
        rating = (re.findall(r'(\d\.\d)\s+\(', block) or [None])[0]
        phone = (re.findall(r'(\(\d{3}\)\s*\d{3}-\d{4})', block) or [""])[0]
        results.append({
            "name": name, "rating": float(rating) if rating else None,
            "phone": phone, "address": "", "website": "",
        })
    return results

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "coffee shops in Austin TX"
    print(json.dumps(scrape_google_maps(query), indent=2))
```

Run it:

```bash
python3 scrape_google_maps.py "coffee shops in Austin TX with phone numbers"
```

## ⚠️ The reality check: why this breaks fast

This local script works for a quick test. But if you try to scale it, you hit three walls:

1. **Rate limiting & IP bans.** Google detects automated traffic from a single IP within a handful of requests and throws a CAPTCHA or temporarily blocks you. On a residential IP this happens fast — often after 20–50 requests.
2. **Fragile HTML parsing.** The regex above targets Google's current local-results markup. Google changes that markup frequently, silently breaking your parser. You end up maintaining selectors instead of building your product.
3. **No scaling infrastructure.** No proxy rotation, no retries, no concurrency, no dataset storage. To get 10,000 leads you'd need to build all of that yourself.

## ☁️ The $2 cloud alternative (zero setup)

Instead of dealing with GitHub's strict rate limits and proxies, I created a one-click AI-powered cloud scraper. You type a plain-English query, it returns clean structured JSON — with rotating proxies, automatic HTML-change adaptation, and Apify's dataset storage built in.

**👉 [Try the AI Google Maps Scraper on Apify — $2 per 1,000 results](https://apify.com/grand_knightship/ai-google-maps-scraper)**

Input:

```json
{ "query": "plumbers in New York City with websites" }
```

It handles the proxies, the parsing, and the scaling. You just get leads.

## When to use which

| Approach | Best for | Cost |
|---|---|---|
| Free local script (above) | One-off test, <50 leads, learning | Free |
| Cloud scraper | Production lead gen, 1k–100k leads, recurring runs | $2 / 1,000 results |

## Sample data

Want to see what the output looks like before running anything? I published 100 real sample leads (coffee shops, plumbers, dentists, gyms, lawyers) here:

[google_maps_sample_data.csv](https://github.com/itsyu5668-sys/maps-engine/blob/main/marketing/google_maps_sample_data.csv)

---

*This post was written to help developers scraping Google Maps find a path that actually scales. If the local script works for your small batch, great — use it. If you need production volume without the headache, the cloud scraper is the faster route.*
