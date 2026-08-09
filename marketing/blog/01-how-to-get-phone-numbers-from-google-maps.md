---
title: "How to Get Phone Numbers from Google Maps in Bulk"
published: false
description: "Pulling real phone numbers out of Google Maps for cold calling and SMS outreach, without getting your IP blocked."
tags: leadgeneration, googlemaps, sales, scraping
cover_image: ""
---

# How to Get Phone Numbers from Google Maps in Bulk

I spent three years building outbound lists for a solar installation company. Every week it was the same grind: find local HVAC guys, find roofers, find electricians, dump their phone numbers into a spreadsheet, hand it to the SDR team. For a long time I did this by hand because I did not trust any of the scraping tools on the market.

Then I figured out that Google Maps is basically a giant phone book with ratings attached. If you know how to query it the right way, you can pull hundreds of verified business phone numbers in minutes. Let me walk through how it actually works and what the gotchas are.

## Why Google Maps is the best phone number source

Most business directories are stale. Yelp, Yellow Pages, Manta, they all have data that is months or years old. Google Maps is different because business owners update their own listings to keep showing up in local search. If a plumber changes their phone number, they fix it on Google within a week because otherwise they lose jobs.

That means the phone numbers you pull from Google Maps are about as fresh as you can get without calling the businesses yourself.

## The manual way and why it falls apart

You can search something like "plumbers in Miami" on Google Maps, click each result, and copy the phone number into a sheet. For ten businesses that is fine. For a hundred it takes an entire afternoon. For a thousand it is impossible without help.

The problem is not just time. It is also that you cannot filter. You end up with every plumber on the map, including the ones with one star and no website, the ones that closed last month, the ones that are actually national chains.

## What a bulk query looks like

Here is a real example. I ran this query last Tuesday for a client who sells CRM software to dental offices:

```
dentists in Dallas TX with phone numbers
```

Twenty results came back in about twelve seconds. Every single one had a phone number. Here are three of them:

```json
[
  {
    "name": "Clear Creek Dental",
    "address": "1900 N Coit Rd, McKinney, TX 75071",
    "rating": 4.8,
    "phone": "+1 972-540-5557",
    "website": "https://clearcreekdental.com"
  },
  {
    "name": "Smile Design Studio",
    "address": "4232 Lbj Fwy, Dallas, TX 75244",
    "rating": 4.9,
    "phone": "+1 972-386-7777",
    "website": "https://smiledesignstudio.com"
  },
  {
    "name": "Uptown Dentistry",
    "address": "3102 Oak Lawn Ave, Dallas, TX 75219",
    "rating": 4.7,
    "phone": "+1 214-522-3000",
    "website": "https://uptowndentistry.com"
  }
]
```

That is the exact shape I hand to the SDR team. Name, address, rating, phone, website. Nothing else, because nothing else matters for cold outreach.

## The phone number coverage question

Here is something nobody tells you. Not every Google Maps listing has a phone number. In my experience the coverage looks like this:

- Home services like plumbers, electricians, and roofers: about 95 to 100 percent have phone numbers
- Medical and dental: about 90 percent
- Restaurants and coffee shops: about 60 to 70 percent
- Retail stores: about 50 percent

The reason is simple. A plumber wants you to call them, that is how they book jobs. A coffee shop often does not want calls clogging up their line, so they leave the field blank.

If you are building a cold calling list, stick to service businesses. You will get near complete phone coverage.

## How I actually run these now

I use an Apify actor called AI Google Maps Scraper. You type a plain English sentence, it returns the structured JSON above. It costs two dollars per thousand results, which is cheap enough that I do not think about it.

**[Try it here if you want to skip the manual work](https://apify.com/grand_knightship/ai-google-maps-scraper)**

The input is just:

```json
{ "query": "plumbers in Miami FL with phone numbers" }
```

And the output is the clean JSON I showed earlier. No proxies to manage, no HTML to parse, no CAPTCHAs to solve.

## A few things I learned the hard way

1. Always include the city and state in your query. If you just say "plumbers" you get a random scatter across the country and your list is useless for territory based sales.
2. Pull ratings even if you do not think you need them. A 2 star plumber is usually a waste of a sales call. I filter anything below 4.0.
3. Grab the website too. Even if you are cold calling, the website tells you whether the business is big enough to be worth your time. A one page Wix site means a solo operator. A real site means they have a budget.
4. Deduplicate by phone number, not by name. Some businesses list themselves under multiple names but use the same phone line.

## Wrapping up

If you do outbound sales, local SEO, or market research, Google Maps phone numbers are one of the highest value data sets you can get your hands on. The data is fresh, the coverage is good for service businesses, and the structure is consistent.

Start with a small test query for your own city. If you are selling to plumbers, run "plumbers in your city with phone numbers" and see what comes back. You will be surprised how clean it is.
