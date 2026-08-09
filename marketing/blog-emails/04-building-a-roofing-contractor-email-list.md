---
title: "Building a Roofing Contractor Email List That Converts"
published: false
description: "A step by step walkthrough of building a roofing contractor email list from Google Maps data, with real numbers."
tags: roofing, emaillist, leadgeneration, contractors
cover_image: ""
---

# Building a Roofing Contractor Email List That Converts

Roofing is my favorite vertical for email lead generation. The average roof job is $10,000 plus, contractors are easy to find on Google Maps, and most of them run a real website with a public contact email. If you sell to roofers, the list building is the easy part.

I built a Dallas roofing email list last week to test a new scraping workflow. Here are the real numbers and the exact process.

## The query

One search: "roofing contractors in Dallas with emails". That returns every roofer Google Maps has for Dallas, each enriched with a public email scraped from the roofer's own website.

## The raw numbers

- Businesses found on Maps: 20
- Businesses with a website: 20
- Businesses with a findable public email: 9
- Skipped, no public email: 11
- Hit rate: 45 percent

That 45 percent is normal for roofers. The 11 that were skipped either use a contact form with no visible email, or their site is a single page with just a phone number. They are not lost leads, they are phone leads.

## What the data looks like

Each row in the list:

```json
{
  "name": "Arrington Roofing",
  "address": "2203 Obenchain St, Dallas, TX 75208",
  "rating": 4.9,
  "phone": "+1 214-774-1972",
  "website": "https://arringtonroofing.com/",
  "email": "info@arringtonroofing.com"
}
```

That is a real business with a real public email. I did not guess info@. I scraped it off their contact page.

## Filtering before you send

Out of 9 emails, I filtered before sending:

- Dropped 1 with a rating under 4.5 (operational problems, not a buyer).
- Dropped 1 with a yahoo.com email (too small, owner operator, no budget).
- Kept 7.

That 7 is my send list. At a 10 percent reply rate, I expect 1 meeting. For a $10,000 average roof job and a 20 percent close on the meeting, the expected value is around $2,000 per send. The list cost me about $0.02 in scraping compute.

## The send

I do not send a template. Each email references the roofer's rating, their city, and a specific problem. The Maps data makes this easy because I already have the rating and the website.

A real send: "Saw Arrington Roofing is at 4.9 stars across Dallas. Most roofers I work with are booked 8 weeks out but losing gutter repair upsells because they do not quote it on the first visit. I built a one page add-on that fixes that. Open to a quick look?"

## What I learned

The hit rate on roofing emails is consistent across cities. I have run the same query in Houston, Atlanta, and Phoenix, and the findable email rate stays between 40 and 50 percent. That makes the math predictable. If I need 100 email leads, I scrape 220 roofers.

The skipped 55 percent are not wasted. They go into a separate cold call list with just name and phone. Same data, two channels.
