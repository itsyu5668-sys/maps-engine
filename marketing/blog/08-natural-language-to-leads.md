---
title: "From Natural Language to Leads: Why Query Parsing Changed My Workflow"
published: false
description: "How typing a plain English sentence instead of configuring scraper inputs made my lead generation workflow faster and less error prone."
tags: ai, leadgeneration, nlp, productivity
cover_image: ""
---

# From Natural Language to Leads: Why Query Parsing Changed My Workflow

For years, configuring a scraper meant filling out a form. You picked a search term, a location, a category code, a radius, a result count, and six other parameters. Get one wrong and you got garbage data or no data. I spent more time configuring scrapers than using their output.

Then I started passing my queries through a language model first, and it changed how I work. Let me explain what that actually looks like and why it matters.

## The old way: config forms

A traditional scraper input looks like this:

```json
{
  "searchStringsArray": ["coffee shops"],
  "locationQuery": "Austin, TX, US",
  "maxCrawledPlacesPerSearch": 20,
  "depthOfSearch": 1,
  "countryCode": "us",
  "language": "en"
}
```

That is fine if you scrape the same thing every day. But I switch categories constantly. One day it is dentists in Dallas, the next it is plumbers in Miami. Every time I had to remember the exact field names and values. Every typo meant a failed run.

## The new way: a sentence

Now my input is this:

```json
{ "query": "coffee shops in Austin TX with phone numbers" }
```

That is it. One field, one sentence. Behind the scenes a language model parses it into the structured config above. I never see the config. I just type what I want in plain English and get leads back.

## What the parser actually does

The model reads the sentence and extracts five things:

1. The search term, like "coffee shops"
2. The location, like "Austin, TX"
3. The result count, defaulting to 20 if I do not specify
4. Whether I mentioned phone numbers
5. Whether I mentioned websites

It returns strict JSON that the scraper understands. No config form, no field name guessing.

For example, "top 50 coffee shops in Austin, need websites" becomes:

```json
{
  "search_term": "coffee shops",
  "location": "Austin, TX",
  "max_results": 50,
  "want_phone": false,
  "want_website": true
}
```

The model handles ambiguity that would break a rigid form. "Restaurants near downtown Chicago" becomes a search for restaurants in Chicago. "Best dentists in the Dallas area" becomes dentists in Dallas, TX. The model knows that "the Dallas area" means Dallas.

## Why this is better in practice

### Speed

I used to spend two minutes per query filling out the config form. Now I spend five seconds typing a sentence. Across a day of 20 queries that is 40 minutes saved.

### Fewer errors

I never fat finger a field name or pick the wrong country code. The model handles normalization. If I type "US" or "United States" or "USA", it all maps correctly.

### Better queries

Because the input is just English, I write more natural queries. "Plumbers in Miami with high ratings" is something I would actually think. I would never manually set a rating filter in a config form. The natural input lets me express what I actually want.

### Onboarding

When I hand this tool to a junior team member, I do not have to teach them the config schema. I tell them to type a sentence. They get it on the first try.

## Where the model adds value beyond parsing

The parser does a few smart things that a rigid form cannot:

- Infers a real location. If I say "coffee shops" with no location, it defaults to United States rather than failing.
- Handles count phrasing. "Top 50" and "50 best" and "give me fifty" all become 50.
- Detects field requests. "With phone numbers" and "need contact info" both flag the phone field.
- Normalizes categories. "Dentist" and "dental offices" and "dentistry" all map to the same search.

These sound small, but they remove the friction that made me avoid running small one off queries.

## A day in the workflow

Here is how I actually use this on a normal day.

Morning: I have a client meeting about entering the Phoenix market for HVAC services. I type "HVAC contractors in Phoenix AZ" and get 20 leads in 15 seconds. I scan the ratings and websites during the call.

Afternoon: A different client wants to target med spas. I type "med spas in Scottsdale AZ" and get a fresh list. I enrich the websites and build an outreach sheet.

End of day: I want to test a new vertical. I type "tattoo shops in Austin TX" just to see what is out there. Five seconds later I have data.

None of those queries required me to remember field names, open a config form, or fix a typo. I just typed and got data.

## The tool I built around this

I wrapped this parser in an Apify actor so anyone can use it without setting up their own language model.

**[AI Google Maps Scraper on Apify](https://apify.com/grand_knightship/ai-google-maps-scraper)**

You type:

```json
{ "query": "coffee shops in Austin TX with phone numbers" }
```

You get back:

```json
[
  {
    "name": "Epoch Coffee",
    "address": "221 W N Loop Blvd, Austin, TX 78751",
    "rating": 4.5,
    "phone": "+1 512-454-3762",
    "website": "http://www.epochcoffee.com/"
  }
]
```

The parser, the scraper, and the cleanup all happen behind the endpoint. Two dollars per thousand results.

## When natural language is not enough

I want to be honest about limitations. The parser handles 90 percent of my queries perfectly. The other 10 percent need manual tweaking:

- Very specific radius queries like "within 2 miles of zip 78704" are not parsed reliably. I fall back to a manual config for those.
- Multi city queries like "dentists in Dallas and Fort Worth" get collapsed into one city. I run them separately.
- Non English queries work but are less reliable. I stick to English.

For those edge cases I keep the manual config option around. Natural language is the default, not the only path.

## Why this pattern is spreading

Query parsing is not unique to Maps scraping. It is a pattern that works anywhere a user facing tool has a complex config. The model translates intent into config, and the user never sees the config.

Expect to see this in every scraping and data tool over the next two years. The config form is dying. The sentence box is replacing it.

If you have not tried working this way, run one query and you will feel the difference immediately. The friction drop is real.
