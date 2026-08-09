"""
Master Engine - Google Maps skin
One endpoint: takes a natural-language query, parses it into structured
Google Maps search params via a fast LLM call, then calls an existing
proven Apify Google Maps actor to do the actual scraping, and returns
clean JSON.

This wraps an existing actor rather than scraping Maps directly -
faster to ship, more reliable, and Google's anti-bot problem becomes
someone else's problem to maintain.

ENV VARS REQUIRED:
  GROQ_API_KEY    - https://console.groq.com
  APIFY_TOKEN     - https://console.apify.com/account/integrations
  MAPS_ACTOR_ID   - the Apify actor ID you're wrapping
                     (e.g. "compass/crawler-google-places")

RUN LOCALLY:
  pip install -r requirements.txt
  uvicorn main:app --host 0.0.0.0 --port 8000 --reload

DEPLOY:
  Push to Render (or any host) as a standard FastAPI app.
  Set the 3 env vars above in the host's dashboard.
"""

import os
import json
import logging
from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("maps-engine")

app = FastAPI(title="Maps Engine")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
APIFY_TOKEN = os.environ.get("APIFY_TOKEN", "")
MAPS_ACTOR_ID = os.environ.get("MAPS_ACTOR_ID", "compass~crawler-google-places")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
APIFY_RUN_URL = f"https://api.apify.com/v2/acts/{MAPS_ACTOR_ID}/run-sync-get-dataset-items"

# Safety ceiling only - NOT a pricing cap anymore. Since you're charging
# per-record (via Apify's Pay-Per-Result pricing on the actor itself, not
# in this code), a run costs you roughly the same per-record regardless
# of size, so there's no profit reason to cap it low. This ceiling just
# stops a single accidental/malicious request (e.g. "get me 500000 leads")
# from running for hours or hammering the underlying actor. Raise it if
# legitimate bulk customers need more.
MAX_RESULTS_PER_RUN = 10000

PARSE_SYSTEM_PROMPT = """You convert a casual English request for Google Maps \
business data into a strict JSON object. Output ONLY the JSON, nothing else.

Schema:
{
  "search_term": string,   // e.g. "italian restaurants"
  "location": string,      // e.g. "Miami, FL" - infer a real place; if the
                            // user gave no location, use "United States"
  "max_results": integer,  // user's requested count, capped at 60; default 20
  "want_phone": boolean,   // true if they mentioned phone numbers/contact
  "want_website": boolean  // true if they mentioned websites/emails
}

Examples:
"Italian restaurants in Miami with phone numbers"
-> {"search_term":"italian restaurants","location":"Miami, FL","max_results":20,"want_phone":true,"want_website":false}

"top 50 coffee shops in Austin, need websites"
-> {"search_term":"coffee shops","location":"Austin, TX","max_results":50,"want_phone":false,"want_website":true}
"""


class ScrapeRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)


class ScrapeResponse(BaseModel):
    parsed_query: dict
    result_count: int
    results: list


async def parse_query(user_query: str) -> dict:
    """Turn free text into structured Maps search params via Groq."""
    if not GROQ_API_KEY:
        raise HTTPException(500, "Server misconfigured: missing GROQ_API_KEY")

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": PARSE_SYSTEM_PROMPT},
            {"role": "user", "content": user_query},
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(GROQ_URL, json=payload, headers=headers)

    if resp.status_code != 200:
        log.error("Groq error: %s", resp.text)
        raise HTTPException(502, "Query parsing failed")

    raw = resp.json()["choices"][0]["message"]["content"]
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        log.error("Bad JSON from parser: %s", raw)
        raise HTTPException(502, "Query parsing returned invalid JSON")

    # Enforce the cap regardless of what the model or user asked for.
    parsed["max_results"] = min(
        int(parsed.get("max_results", 20) or 20), MAX_RESULTS_PER_RUN
    )
    # Note: no per-run price is calculated here. Pricing is handled by
    # Apify's own Pay-Per-Result (PPR) billing on your actor - you set the
    # price per result in the actor's Pricing tab on Apify Console, and
    # Apify meters + charges the user automatically per item pushed to
    # the dataset. This backend's only job is to return the right number
    # of correctly-shaped results; it does not need to touch money.
    parsed.setdefault("search_term", user_query)
    parsed.setdefault("location", "United States")
    parsed.setdefault("want_phone", False)
    parsed.setdefault("want_website", False)
    return parsed


async def run_maps_actor(parsed: dict) -> list:
    """Call the existing Apify Google Maps actor with structured input."""
    if not APIFY_TOKEN:
        raise HTTPException(500, "Server misconfigured: missing APIFY_TOKEN")

    actor_input = {
        "searchStringsArray": [parsed["search_term"]],
        "locationQuery": parsed["location"],
        "maxCrawledPlacesPerSearch": parsed["max_results"],
        "language": "en",
    }

    params = {"token": APIFY_TOKEN}

    async with httpx.AsyncClient(timeout=180) as client:
        resp = await client.post(APIFY_RUN_URL, params=params, json=actor_input)

    if resp.status_code >= 300:
        log.error("Apify error: %s", resp.text)
        raise HTTPException(502, "Scrape run failed")

    items = resp.json()
    return items


def trim_fields(items: list, want_phone: bool, want_website: bool) -> list:
    """Return only the fields the user actually asked for, plus basics."""
    trimmed = []
    for it in items:
        row = {
            "name": it.get("title") or it.get("name"),
            "address": it.get("address"),
            "rating": it.get("totalScore") or it.get("rating"),
        }
        if want_phone:
            row["phone"] = it.get("phone") or it.get("phoneUnformatted")
        if want_website:
            row["website"] = it.get("website")
        trimmed.append(row)
    return trimmed


@app.post("/scrape/maps", response_model=ScrapeResponse)
async def scrape_maps(req: ScrapeRequest):
    parsed = await parse_query(req.query)
    raw_items = await run_maps_actor(parsed)
    results = trim_fields(raw_items, parsed["want_phone"], parsed["want_website"])
    return ScrapeResponse(
        parsed_query=parsed,
        result_count=len(results),
        results=results,
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
