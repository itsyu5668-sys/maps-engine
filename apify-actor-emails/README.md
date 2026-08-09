# AI Google Maps Email Extractor | Business Contact Emails

Extract a public contact email from each Google Maps business's own website.
One plain-English input. Returns structured leads with name, address, rating,
phone, website, and email.

## Input

A single natural-language string describing the businesses you want contact
emails for. Include the business type and city for the best results.

```json
{"query": "roofing contractors in Dallas with emails"}
```

## Output (dataset)

One row per business with a found public contact email:

```json
{
  "name": "T Rock Roofing & Contracting",
  "address": "9330 Lyndon B Johnson Fwy #900, Dallas, TX 75243, United States",
  "rating": 4.9,
  "phone": "+1 469-931-9867",
  "website": "https://www.dallasroofer.com/",
  "email": "info@dallasroofer.com"
}
```

## How it works (read this before you buy)

We pull the email address directly from each business's own website (homepage
or contact page), the same one a visitor would see. We do not guess emails, do
not verify deliverability, and do not use any private or enrichment data source.

Not every business lists a public email, so result counts will be lower than a
pure business-search run. In our testing on contractor verticals, roughly
40 to 50 percent of Google Maps businesses publish a findable email on their
own site. The rest are skipped and not billed.

Only leads with a found email are returned and billed. If a run returns 10
results, you pay for 10 results, not for the businesses that had no email.

## Best use cases

- Contractor lead generation: roofers, plumbers, electricians, HVAC, fence
  companies, painters. These trades usually run a real website with a contact
  page and an info@ or office@ address.
- Service-business B2B outreach: dentists, law firms, accounting firms, real
  estate agents, insurance brokers.
- Local partner and vendor outreach.

It works less well for pure retail chains, franchises with no local site, or
businesses that only list a phone number on Maps.

## Pricing

Pay-Per-Result. You pay only for leads that include a found email. See the
Pricing tab for the per-1k rate.
