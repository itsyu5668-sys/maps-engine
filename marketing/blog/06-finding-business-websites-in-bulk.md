---
title: "Finding Business Websites in Bulk: A Guide for Lead Builders"
published: false
description: "How to pull hundreds of business website URLs from Google Maps for enrichment, research, and outreach."
tags: leadgeneration, scraping, webdev, data
cover_image: ""
---

# Finding Business Websites in Bulk: A Guide for Lead Builders

Website URLs are the backbone of modern lead generation. Once you have a business website, you can find an email, check their tech stack, estimate their revenue, and figure out if they are worth pursuing. But getting the URLs in the first place is surprisingly annoying if you do it manually.

I build lead lists for a living, and Google Maps has become my primary source for business website URLs. Here is why and how.

## Why the website is the key field

Think about what you can do once you know a business website:

- Run it through an email finder to get a contact
- Check the tech stack with BuiltWith or Wappalyzer
- See if they have a careers page, which signals team size
- Check their blog for recent activity, which signals engagement
- Look at their site speed and design quality, which signals budget
- Find their social links and check follower counts

Every one of those enrichment steps starts with the website URL. Without it, you are stuck with a name and a phone number, which is 1990s outreach.

## The Google Maps advantage

Google Maps has a website field on almost every business listing. In my experience, website coverage by category looks like this:

- Service businesses like plumbers and electricians: 90 to 100 percent have websites
- Medical and dental: 95 percent
- Restaurants and coffee shops: 80 to 90 percent
- Retail stores: 70 percent
- New or very small businesses: 50 percent or less

That is way better coverage than any business directory. And because business owners maintain their own listings, the URLs are usually current.

## What a bulk pull looks like

Run a query and get back rows where each one has the website field populated. Here is a real example from "electricians in Phoenix AZ":

```json
[
  {
    "name": "Valley Electric",
    "address": "3020 N Central Ave, Phoenix, AZ 85012",
    "rating": 4.7,
    "phone": "+1 602-555-0188",
    "website": "https://valleyelectricphx.com"
  },
  {
    "name": "Desert Wire Electric",
    "address": "411 S 7th Ave, Phoenix, AZ 85003",
    "rating": 4.9,
    "phone": "+1 602-555-0144",
    "website": "https://desertwireelectric.com"
  },
  {
    "name": "AZ Spark Electric",
    "address": "1500 E Thomas Rd, Phoenix, AZ 85014",
    "rating": 4.6,
    "phone": "+1 602-555-0177",
    "website": "http://azsparkelectric.com"
  }
]
```

Every result has a website. That is your enrichment queue.

## From URLs to a working list

Once you have the URLs, the workflow looks like this:

### Step 1: Deduplicate by domain

Some businesses list multiple locations under the same website. If you pull "dentists in Dallas" and "dentists in Fort Worth", you will get some of the same domains. Deduplicate by the website field before enriching.

### Step 2: Check site quality

Visit each site or run it through a tool. Note: is it a real custom site, a Wix or Squarespace template, or a single page? This tells you the business stage.

- Custom site with multiple pages: established, has budget
- Template site with a few pages: small but trying
- Single page or no site: very small, low budget, probably skip

### Step 3: Find the contact path

On each site, find the contact email. If there is a contact form with no email listed, use an email finder tool on the domain.

### Step 4: Enrich with tech and size signals

Run the domain through a tech stack checker. Knowing whether a business uses Shopify, WordPress, or a custom stack tells you what to sell them. A Shopify store is an ecommerce prospect. A WordPress site is a content prospect. A custom stack means they have a developer, which changes your pitch.

## A batch I ran last week

I pulled "roofers in Denver CO" for a client who sells estimating software. Got 20 results. Nineteen had websites. After visiting the sites:

- 8 had real multi page sites, good prospects
- 7 had basic template sites, okay prospects
- 4 had single page sites, skipped

I enriched the 15 good and okay prospects with email finders, got valid emails for 12 of them, and handed the list to the sales team. The whole thing took 90 minutes and cost about four cents in data fees.

## The tool I use

For the bulk pull I use an Apify actor that takes a plain English query and returns the structured rows with website fields populated.

**[AI Google Maps Scraper on Apify](https://apify.com/grand_knightship/ai-google-maps-scraper)**

Input:

```json
{ "query": "roofers in Denver CO" }
```

Output is the JSON above, with website on nearly every row. Two dollars per thousand results.

## Handling the no website results

When a business has no website, do not throw it away. A business with no website but a phone number and a good rating is either a lead for web design services or a sign that the business is too small to be your prospect. Either way, the absence of a website is itself a signal.

I keep a separate list of no website businesses and use it for web design outreach. Those businesses know they need a site, they just have not gotten around to it. A cold call offering to build one lands better than almost any other pitch.

## URL normalization tips

Google Maps sometimes returns URLs with tracking parameters, like:

`https://example.com/?utm_source=gmb`

Clean those up before enrichment. Strip query parameters, normalize http versus https, and strip trailing slashes. Otherwise your deduplication and your email finder will treat the same domain as two different sites.

A quick Python snippet I use:

```python
from urllib.parse import urlparse, urlunparse

def clean_url(url):
    if not url:
        return None
    p = urlparse(url)
    return urlunparse((p.scheme, p.netloc, p.path, "", "", "")).rstrip("/")
```

Run every website field through that before you start enriching.

## Start with one vertical

If you want to test this, pick one business category you understand well. Pull 30 results, visit each site, and build your first enriched list. You will quickly see which signals matter for your specific pitch and which you can ignore.

The website is the gateway to every other enrichment step. Get good at pulling them in bulk, and the rest of your pipeline gets easier.
