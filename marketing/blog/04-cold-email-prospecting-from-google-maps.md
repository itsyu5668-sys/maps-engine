---
title: "Cold Email Prospecting: Building Lists from Google Maps Business Data"
published: false
description: "How to turn Google Maps business listings into cold email prospect lists that actually convert."
tags: coldemail, sales, leadgeneration, prospecting
cover_image: ""
---

# Cold Email Prospecting: Building Lists from Google Maps Business Data

Cold email only works if your list is good. I learned this after burning through three months of outreach with a 1 percent reply rate and zero meetings. The problem was not my template. The problem was my data. I was emailing generic info@ addresses scraped from a stale directory.

Once I switched to building lists from Google Maps, my reply rate jumped to 9 percent and I started booking real meetings. Here is exactly how I do it.

## Why Google Maps data beats bought lists

A bought list gives you a company name and an email. That is it. You have no context, no signal, no way to know if the company is a fit before you email them.

Google Maps gives you a company name, an address, a phone number, a website, and a star rating. That is five signals you can use to qualify before you send a single email.

The star rating alone is a killer filter. Businesses with high ratings are usually operationally healthy, which means they have budget. Businesses with low ratings have bigger problems than whatever you are selling.

## The list building workflow

### Step 1: Pull businesses by category and city

Start with a query that matches your buyer. If you sell marketing services to gyms, your query is "gyms in Denver CO". If you sell software to law firms, your query is "law firms in Chicago IL".

You get back structured rows:

```json
{
  "name": "Mountain Fitness",
  "address": "1450 Blake St, Denver, CO 80202",
  "rating": 4.6,
  "phone": "+1 303-555-0142",
  "website": "https://mountainfitnessdenver.com"
}
```

### Step 2: Filter by rating and website presence

Drop anything below a 4.0 rating unless you sell to struggling businesses. Drop anything without a website, because no website usually means no budget and no one to read your email.

After this filter you are typically left with 40 to 70 percent of your original pull. That is your real prospect list.

### Step 3: Find the right email

This is the manual part that most people skip and that makes all the difference. Visit each website and find the contact email. For small businesses it is usually on the contact page, the footer, or the about page.

Common patterns:

- hello@businessname.com
- info@businessname.com
- owner firstname@businessname.com

If you cannot find an email on the site, use a tool like Hunter.io or just email the pattern that matches the domain. For a solo owner operated business, the owner reads every inbox.

### Step 4: Write a researched first email

This is where the Maps data pays off. You know their rating, their address, and you visited their site. Reference something real.

> Hi Sarah,
>
> I saw Mountain Fitness has a 4.6 on Google, nice work. The reviews mention your class schedule is hard to keep updated on the site. I help gyms sync their booking calendar to their website automatically. Worth a 10 minute call next week?

That email got a reply because it is specific. It references their actual rating and an actual problem. You cannot write that email from a bought list.

## The tool stack I use

For pulling the raw Maps data I use an Apify actor that takes a plain English query and returns the structured rows. It is two dollars per thousand results.

**[AI Google Maps Scraper on Apify](https://apify.com/grand_knightship/ai-google-maps-scraper)**

Input:

```json
{ "query": "gyms in Denver CO" }
```

Output is the JSON I showed above, ready to enrich and email.

For enrichment I use a spreadsheet plus Hunter.io for email finding. For sending I use a standard cold email tool. Nothing fancy.

## A numbers breakdown

Let me show you the math on a real campaign. Last month I ran outreach to independent bookkeepers in three cities.

- Raw pull: 90 businesses across three cities
- After rating and website filter: 52 prospects
- Emails found: 47 of the 52
- Emails sent: 47
- Replies: 6, which is a 13 percent reply rate
- Meetings booked: 3
- Closed: 1

Total data cost: about 20 cents. The closed deal was worth 400 dollars a month recurring. That is the kind of return you get when your list is actually good.

## Mistakes that kill cold email lists

1. Emailing the info@ address without checking if a real person is behind it. These inboxes are often unmonitored. Always try to find a named contact.
2. Not filtering by rating. You waste emails on businesses that cannot afford you.
3. Sending the same generic template to everyone. Use the Maps data to personalize.
4. Pulling too many cities at once. You end up with a huge list and no time to research each prospect. Go 50 at a time.

## How to think about volume

Cold email is a quality game, not a quantity game. I would rather send 50 highly researched emails than 500 generic ones. The 50 will outperform the 500 every time.

Google Maps gives you the data to do that research efficiently. You are not guessing about who the prospect is. You know their rating, their location, and their website. That is enough to write a great first email.

## Start with one city

If you want to try this, pick one city and one category that matches your buyer. Pull 20 to 40 businesses, filter, enrich, and email. Track your reply rate. If it is above 8 percent, you have a working channel. Scale from there.

The data is sitting right there on Google Maps. The only question is whether you use it.
