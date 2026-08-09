---
title: "Scraping Google Maps Without Getting Blocked: What Actually Works"
published: false
description: "The honest truth about scraping Google Maps at scale, why most free methods fail, and what to use instead."
tags: scraping, googlemaps, python, webdev
cover_image: ""
---

# Scraping Google Maps Without Getting Blocked: What Actually Works

I have tried to scrape Google Maps six different ways over the last four years. Some worked for a day. Some worked for a hundred requests. None of the free methods survived contact with production traffic. This is the honest breakdown of what works, what fails, and why.

## First, why Google Maps is hard to scrape

Google Maps is not a static website. It is a JavaScript heavy application that loads business data through a combination of internal APIs and signed endpoints. When you load the page, your browser makes dozens of XHR requests to fetch the place data, the reviews, the photos, and the sidebar listings.

That means a simple requests.get call does not work. You either get an empty shell of HTML or you get a CAPTCHA wall. I learned this the hard way in 2022 when I built a scraper that worked perfectly in testing and returned nothing on the first real run.

## Method 1: Plain requests with a fake user agent

This is the approach every beginner tutorial shows. You set a desktop user agent header, hit the Google local search endpoint, and parse the HTML with a regex or BeautifulSoup.

```python
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 ..."}
resp = requests.get(f"https://www.google.com/search?tbm=lcl&q={query}", headers=headers)
soup = BeautifulSoup(resp.text, "html.parser")
```

What happens: it works for about 20 to 50 requests from a residential IP. Then Google serves you a CAPTCHA or a 429 Too Many Requests response. On a datacenter IP it fails almost immediately.

Verdict: fine for a quick test of ten businesses. Useless for anything real.

## Method 2: Selenium or Playwright with headless Chrome

The next step up is running a real browser in headless mode, navigating to Google Maps, waiting for the results to render, and extracting them from the DOM.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.google.com/maps/search/plumbers+miami")
    page.wait_for_selector(".Nv2PK")
    results = page.query_selector_all(".Nv2PK")
```

What happens: it works better than plain requests because you are running a real browser. But it is slow, maybe 2 to 5 seconds per page, and Google still detects automation through fingerprinting. After a few hundred requests you start getting CAPTCHAs again.

Verdict: better, but slow and still gets blocked at scale. You also pay for the browser overhead in memory and CPU.

## Method 3: Rotating residential proxies

This is where serious scrapers end up. You combine Playwright or requests with a pool of residential proxy IPs. Each request goes out from a different IP address, so Google sees traffic from what looks like a hundred different homes instead of one server.

What happens: it works, and it can scale to tens of thousands of requests. The problem is cost. Residential proxies run anywhere from 2 to 15 dollars per gigabyte. Scraping Google Maps is data heavy because of all the JavaScript and images, so a serious run can cost you 50 to 200 dollars in proxy fees alone.

Verdict: this is how the pros do it. But it is expensive and you are maintaining a complex stack.

## Method 4: Wrapping an existing Apify actor

This is the approach I landed on. Instead of scraping Google myself, I use an actor that already solved the proxy and parsing problems. Apify has several Google Maps scrapers maintained by teams who do nothing but keep them working.

I wrapped one in a thin service that takes a plain English query, calls the actor, and returns clean JSON. The actor handles proxies, retries, and HTML changes. I just get data.

**[Here is the actor I use and sell](https://apify.com/grand_knightship/ai-google-maps-scraper)**

The input is one line:

```json
{ "query": "electricians in Phoenix AZ" }
```

And the output is a clean list:

```json
[
  {
    "name": "Phoenix Electric LLC",
    "address": "1234 E Camelback Rd, Phoenix, AZ 85014",
    "rating": 4.7,
    "phone": "+1 602-555-0100",
    "website": "https://phoenixelectricllc.com"
  }
]
```

Cost is two dollars per thousand results. That is cheaper than running my own proxy pool and I do not have to maintain anything.

## Why wrapping is smarter than building

I used to think building my own scraper was the pure approach. Then I spent a weekend fixing a parser because Google changed one CSS class name. Then I spent another weekend debugging a proxy rotation issue. Then I spent a third weekend rewriting the whole thing because Google shipped a new Maps version.

The lesson: scraping Google Maps is not a one time engineering task. It is an ongoing maintenance burden. Someone has to watch it every week and fix it when it breaks.

If scraping is not your core business, do not own that maintenance. Wrap an actor that someone else maintains and focus on what you actually do, which is probably sales, marketing, or analysis.

## What I tell people who ask

If you need ten businesses for a quick test, use the requests method and accept it will break.

If you need a thousand businesses a week, use a wrapped Apify actor. The cost is predictable, the data is clean, and you do not lose weekends to Google changing their HTML.

If you need a million businesses a month and you have an engineering team, build your own stack with residential proxies. But honestly, at that point you should question whether scraping is the right approach at all.

## The takeaway

Google Maps is one of the most valuable business data sources on the internet. It is also one of the hardest to scrape reliably. Do not let the difficulty stop you from using the data. Just pick the method that matches your scale and stop trying to build everything from scratch.
