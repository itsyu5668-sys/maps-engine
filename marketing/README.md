# AI Google Maps Scraper — Free Local Script

Type what business leads you need in plain English and get structured data back:
name, address, rating, phone, and website.

## Free local version (this repo)

```bash
python3 free_local_scraper.py "coffee shops in Austin TX with phone numbers"
```

Outputs JSON business leads. No API keys, no cloud, no signup.

## ⚠️ The catch with running it locally

This script scrapes Google's public search results directly from your IP. Google
will **rate-limit or temporarily block your IP** after a handful of requests, and
the HTML parsing **breaks every time Google changes its markup**. That means:

- You get blocked quickly
- You have to keep fixing the parser
- No proxies, no retries, no scaling

## ☁️ The 1-click cloud version (no setup, no rate limits)

If you want to run this instantly in the cloud with rotating proxies, automatic
HTML-change adaptation, and clean structured JSON — for **$2 per 1,000 results** —

**👉 [Try the AI Google Maps Scraper on Apify](https://apify.com/grand_knightship/ai-google-maps-scraper)**

You type a query, it returns the data. No proxies to manage, no parser to maintain.

## Sample data

See [`google_maps_sample_data.csv`](./google_maps_sample_data.csv) for 100 real
sample leads across 5 niches (coffee shops, plumbers, dentists, gyms, lawyers).

Want that data updated daily? Get the live scraper here:
https://apify.com/grand_knightship/ai-google-maps-scraper
