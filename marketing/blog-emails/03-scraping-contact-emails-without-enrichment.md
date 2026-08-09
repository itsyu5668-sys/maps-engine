---
title: "Scraping Contact Emails Without an Enrichment API"
published: false
description: "Why pulling emails directly from business websites beats paying for enrichment APIs, and how to do it honestly."
tags: scraping, email, enrichment, data
cover_image: ""
---

# Scraping Contact Emails Without an Enrichment API

There is an entire industry built on selling you emails you could scrape yourself. Enrichment APIs charge per match, often for emails they guessed using a pattern like firstname@company.com. The honest alternative is to visit the business's own website and pull the email they actually published.

I am not against enrichment APIs for every use case. If you need a CTO's direct email at a 500 person SaaS company, scraping their marketing site will not get it. But for local business lead generation, enrichment is overkill and often wrong.

## The case against enrichment for local business

Most local businesses are small. The owner answers the phone and the email. There is no "Director of Operations" hidden behind a contact form. The email you want is the one on their contact page, usually info@ or office@, and it goes to someone who can make a decision.

Enrichment APIs do two things that hurt you here. First, they guess. If they cannot find a verified email, they return a pattern matched guess. That guess bounces. Second, they charge you for the guess. You pay for data that is wrong.

Scraping the public email costs nothing per email. You pay for the compute to fetch the pages, and the email you get is the one the business chose to publish.

## How the scrape works

For each business:

1. Take the website URL from their Google Maps listing.
2. Fetch the homepage HTML.
3. If no email is on the homepage, fetch /contact, /contact-us, or /about.
4. Regex match any email address in the HTML.
5. Filter out junk: no-reply addresses, example.com, image filenames, vendor emails like wixpress.com or sentry.io.
6. If more than one real email is found, prefer info@, hello@, contact@, sales@.

That is it. No API key, no per match fee, no guesswork.

## The honesty part

I say this in every post because it matters: this method does not verify deliverability. The email is real and public, but it might be a catch all that never gets read, or it might be monitored once a week. If you need guaranteed deliverability, run a verification pass with a tool like ZeroBounce after you scrape.

The tradeoff is clear. Scraping is free per email and honest about what it gets. Verification costs money but confirms the inbox is live. Most cold email workflows need both: scrape for volume, verify for quality.

## Hit rate expectations

Out of 20 Google Maps businesses in a contractor vertical, expect 8 to 11 to return a public email. The rest either have no website, or their site uses a contact form with no visible email address. That 40 to 55 percent hit rate is normal and honest. Anyone promising 90 percent on local business email scraping is either lying or guessing.

## When you still want enrichment

After you have scraped the public email, enrichment can add value for one thing: finding a named contact at the company. If info@ goes to a general inbox and you want the owner's direct email, enrichment tools like Hunter or Apollo can sometimes find it. But use them after the scrape, not instead of it.
