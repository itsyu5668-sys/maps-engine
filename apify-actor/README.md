# AI Google Maps Scraper | Natural-Language Search

Search Google Maps by typing what you want in plain English. Get clean JSON leads back - no spreadsheets to configure, no API keys to manage, no settings panels. Just one search box.

Type something like `dentists in Tampa with phone numbers` and the actor returns structured business listings ready for your CRM, cold outreach, or spreadsheet.

## Why use this actor

- One search box. No `searchStringsArray`, no `locationQuery`, no field mapping. Type a sentence, get leads.
- Plain-English parsing. Ask for "top 50 coffee shops in Austin, need websites" and it understands the count, the place, and which fields you want.
- Clean, predictable output. Every result has the same shape - name, address, rating, and the extras you asked for (phone, website).
- Fast and cheap. HTTP-based scraping, ~7 seconds for 20 results, $2 per 1,000 results.

## Input

One field.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `query` | string | yes | A plain-English request for Google Maps data, 3 to 500 characters. |

Examples:
- `Italian restaurants in Miami with phone numbers`
- `top 50 coffee shops in Austin, need websites`
- `HVAC contractors in Raleigh NC`
- `personal injury lawyers in Phoenix AZ with phone and website`

## Output

Each result is one business. Fields returned depend on what you asked for, plus the basics.

| Field | Always returned | Description |
| --- | --- | --- |
| `name` | yes | Business name |
| `address` | yes | Full street address |
| `rating` | yes | Google star rating |
| `phone` | when requested | Formatted phone number, when Google has one |
| `website` | when requested | Business website URL |

### Sample output

```json
[
  {
    "name": "Epoch Coffee",
    "address": "221 W N Loop Blvd, Austin, TX 78751, United States",
    "rating": 4.5,
    "phone": "+1 512-454-3762",
    "website": "https://epochcoffee.com"
  },
  {
    "name": "Mozart's Coffee Roasters",
    "address": "3825 Lake Austin Blvd, Austin, TX 78703, United States",
    "rating": 4.5,
    "phone": "+1 512-477-2900"
  }
]
```

## Pricing

Pay per result. You are charged $0.002 for each business returned ($2 per 1,000 results). Runs that return zero results cost nothing beyond the actor start.

## Use cases

- Lead generation for sales teams (real estate agents, dentists, plumbers, lawyers, HVAC, roofing, med spas)
- Building local business directories
- Market research and competitor mapping
- Enriching contact lists with phones and websites

## How it works

You type a request. A fast language model turns it into a structured Google Maps search (what to find, where, how many, which fields). The actor runs an HTTP-based Google Maps scraper, trims the output to only the fields you asked for, and pushes clean JSON to the dataset. No browser, no fluff.
