---
title: "Market Research with Google Maps: Counting Competitors by City"
published: false
description: "How to use Google Maps business data to size markets, compare cities, and find underserved niches."
tags: marketresearch, data, googlemaps, business
cover_image: ""
---

# Market Research with Google Maps: Counting Competitors by City

Before you open a new location, launch a product, or enter a new market, you need to know how crowded it is. Traditional market research reports cost thousands and are months out of date. Google Maps is free, fresh, and covers almost every business in every city.

I use Maps data as my first pass on any market sizing question. Here is how I do it and what it can tell you.

## The core question: how many of these businesses exist here?

Market research starts with counting. If you want to open a coffee shop in Austin, the first question is how many coffee shops are already there. If you sell software to gyms, the first question is how many gyms are in your target city.

Google Maps can answer that in seconds. Run a query like "coffee shops in Austin TX" and you get back a list. The length of the list is your market size estimate.

But the count is just the start. The structure of the list is where the real insight lives.

## What the data tells you beyond the count

A single row from a Maps pull looks like this:

```json
{
  "name": "Houndstooth Coffee",
  "address": "401 Congress Ave, Austin, TX 78701",
  "rating": 4.6,
  "phone": "+1 512-555-0100",
  "website": "https://houndstoothcoffee.com"
}
```

With a hundred of those rows, you can answer questions that a consultant would charge five thousand dollars to investigate.

### Market density

Count businesses per capita. Pull the population of the city from census data, divide the business count by it. A city with 50 coffee shops and 500,000 people has one shop per 10,000 residents. Compare that across cities to find dense and sparse markets.

Dense markets are competitive but validated, there is clearly demand. Sparse markets are either underserved or unviable, and you need to figure out which.

### Rating ceiling

What is the highest rating in the market? If the top coffee shop in a city is rated 4.4, that is a low ceiling, which means quality is not yet a differentiator. If the top is 4.9, the market rewards quality and you need to compete on it.

### Web presence maturity

What percentage of businesses have websites? In an emerging market, maybe 40 percent. In a mature market, 90 percent. This tells you how sophisticated the local businesses are.

### Chain versus independent ratio

Count how many results are national chains versus independent businesses. A market dominated by chains is hard to enter as an independent. A market full of independents is more fragmented and more entry friendly.

You can spot chains by name, but also by website. Chains point to corporate domains. Independents point to local domains.

## A real comparison I ran

A client was choosing between Austin and Nashville for a new salon location. I pulled "salons in Austin TX" and "salons in Nashville TN" and compared.

| Metric | Austin | Nashville |
|---|---|---|
| Total pulled | 20 | 20 |
| Average rating | 4.5 | 4.3 |
| Top rating | 4.9 | 4.7 |
| Percent with website | 90 | 75 |
| Chains in results | 3 | 1 |

The data suggested Nashville was the better entry point. Lower rating ceiling meant less quality competition. Lower web presence meant less sophistication to compete against. Fewer chains meant more room for an independent.

The client opened in Nashville. The Maps data was not the only factor, but it was the cheapest and fastest signal we had.

## How to pull the data

I use an Apify actor that takes a plain English query and returns structured rows.

**[AI Google Maps Scraper](https://apify.com/grand_knightship/ai-google-maps-scraper)**

Input:

```json
{ "query": "salons in Nashville TN" }
```

Output is the JSON above. Two dollars per thousand results, so running ten city comparisons costs about twenty cents.

## Building a market comparison spreadsheet

Set up a sheet with one row per city and columns for: business count, average rating, top rating, percent with website, percent with phone, chain count. Pull the same category in ten cities and fill in the sheet.

The patterns jump out immediately. You see which cities are saturated, which are underserved, and which have a quality gap you can exploit.

I keep a master sheet of 20 categories across 50 cities that I update quarterly. It is my personal market atlas, and it cost me about two dollars to build.

## Limitations to know about

Google Maps data is not perfect for market research. A few caveats:

1. The count is not exhaustive. Maps caps results, usually around 20 to 60 per query depending on density. For a true count you need to run multiple queries with different subareas.
2. Closed businesses sometimes linger. A business that shut down last month might still appear. Cross check by visiting the website.
3. Ratings skew high. The average Google rating is around 4.2, not 3.0. Adjust your expectations.
4. Chains complicate counting. A Starbucks shows up once per location, so a city with 15 Starbucks counts as 15 coffee shops. Decide whether to include or exclude chains before you analyze.

## When to go deeper

Maps data is your first pass. If a market looks promising, go deeper with a manual audit of the top five competitors. Visit their sites, read their reviews, and note their pricing. The Maps pull tells you the market shape. The manual audit tells you the market texture.

## Start with your own city

If you have never done this, start with your own city and a category you know. Pull "gyms in your city" or "restaurants in your city" and build the comparison sheet. You will immediately see how useful the structured view is compared to scrolling around in Maps.

Market research does not have to be expensive or slow. The data is already on the map. You just need to pull it into a spreadsheet.
