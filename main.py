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
                     (default: "scraperlink~google-maps-scraper",
                      a cheap HTTP-based Maps actor ~$0.50/1k results)

RUN LOCALLY:
  pip install -r requirements.txt
  uvicorn main:app --host 0.0.0.0 --port 8000 --reload

DEPLOY:
  Push to Render (or any host) as a standard FastAPI app.
  Set the 3 env vars above in the host's dashboard.
"""

import os
import json
import re
import logging
import asyncio
from typing import Optional
from urllib.parse import urlparse

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("maps-engine")

app = FastAPI(title="Maps Engine")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
APIFY_TOKEN = os.environ.get("APIFY_TOKEN", "")
MAPS_ACTOR_ID = os.environ.get("MAPS_ACTOR_ID", "scraperlink~google-maps-scraper")

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

    # scraperlink/google-maps-scraper input: a single query string that
    # includes the location (it has no separate location field), plus num/gl/hl.
    search = parsed["search_term"]
    location = parsed["location"]
    query_str = f"{search} in {location}" if location else search

    actor_input = {
        "query": [query_str],
        "num": max(parsed["max_results"], 10),
        "gl": "us",
        "hl": "en",
    }

    params = {"token": APIFY_TOKEN}

    async with httpx.AsyncClient(timeout=180) as client:
        resp = await client.post(APIFY_RUN_URL, params=params, json=actor_input)

    if resp.status_code >= 300:
        log.error("Apify error: %s", resp.text)
        raise HTTPException(502, "Scrape run failed")

    items = resp.json()
    return items


def trim_fields(items: list) -> list:
    """Return clean lead fields. Phone/website are core contact data for lead
    generation, so they are always emitted. Google Maps doesn't have a phone
    for every business, so phone may be null — the dataset schema permits null."""
    trimmed = []
    for it in items:
        row = {
            "name": it.get("title") or it.get("name"),
            "address": it.get("address"),
            "rating": it.get("rating") or it.get("totalScore"),
            "phone": it.get("phone") or it.get("phoneUnformatted") or it.get("phoneNumber"),
            "website": it.get("website"),
        }
        trimmed.append(row)
    return trimmed


@app.post("/scrape/maps", response_model=ScrapeResponse)
async def scrape_maps(req: ScrapeRequest):
    parsed = await parse_query(req.query)
    raw_items = await run_maps_actor(parsed)
    results = trim_fields(raw_items)
    return ScrapeResponse(
        parsed_query=parsed,
        result_count=len(results),
        results=results,
    )


# ---------------------------------------------------------------------------
# Email extraction endpoint (Actor #2)
#
# Honest description of what this does: it visits each business's own public
# website (homepage and common contact-page paths) and regex-extracts the
# email addresses visible on the page. That is the same thing a human visitor
# would see. It does NOT guess emails, does NOT verify deliverability, and
# does NOT use any private/enrichment data source. Businesses that publish no
# public email are skipped, so result counts will be lower than a pure
# business-search run.
# ---------------------------------------------------------------------------

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")

# Local parts and domains that are almost never a real contact address.
JUNK_LOCAL = {
    "noreply", "no-reply", "donotreply", "do-not-reply", "example", "test",
    "sample", "email", "your", "yourname", "user", "youremail", "change",
    "domain", "someone", "sentry", "wpmudev", "placeholder", "example.com",
}
JUNK_DOMAIN = {
    "example.com", "example.org", "example.net", "yourdomain.com", "domain.com",
    "email.com", "wixpress.com", "sentry.io", "sentry-next.wixpress.com",
    "shields.io", "schema.org", "w3.org", "google.com", "googleapis.com",
    "gstatic.com", "cloudflare.com", "jsdelivr.net", "unpkg.com",
    "bootstrap.com", "github.com", "github.io", "wordpress.com",
    "wix.com", "squarespace.com", "shopify.com",
}
JUNK_LOCAL_SUFFIX = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".css", ".js")
# Preferred local parts when more than one real email is found.
PREFERRED_LOCAL = ("info", "hello", "contact", "sales", "admin", "office", "mail", "support", "team")

# Pages most likely to hold a public contact address.
CONTACT_PATHS = ["", "/contact", "/contact-us", "/contactus", "/about", "/about-us"]

EMAIL_FETCH_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

EMAIL_FETCH_CONCURRENCY = 8
EMAIL_FETCH_TIMEOUT = 15.0


class EmailScrapeResponse(BaseModel):
    parsed_query: dict
    result_count: int
    skipped_no_email: int
    results: list


def _is_junk_email(addr: str) -> bool:
    """True if the address looks like a placeholder, an asset URL, or a vendor."""
    addr = addr.strip().lower()
    local, _, domain = addr.partition("@")
    if not domain or domain in JUNK_DOMAIN:
        return True
    if local in JUNK_LOCAL:
        return True
    if any(local.endswith(s) for s in JUNK_LOCAL_SUFFIX):
        return True
    # image filenames parsed out of src attributes: "logo-2x@2x" etc.
    if re.match(r"^[0-9a-f]{8,}$", local):
        return True
    return False


def _pick_best(emails: list) -> Optional[str]:
    """From a deduped set of real emails, pick the most likely contact."""
    if not emails:
        return None
    lowered = []
    for e in emails:
        e = e.strip().rstrip(".").lower()
        if not _is_junk_email(e):
            lowered.append(e)
    if not lowered:
        return None
    uniq = list(dict.fromkeys(lowered))
    for pref in PREFERRED_LOCAL:
        for e in uniq:
            if e.split("@", 1)[0] == pref:
                return e
    # otherwise return the shortest reasonable address (shorter = more generic)
    uniq.sort(key=lambda e: (len(e), e))
    return uniq[0]


def _extract_emails_from_html(html: str) -> list:
    """Pull plain emails out of rendered HTML, also decode basic mailto:."""
    found = []
    # mailto: links first, slightly higher signal
    for m in re.finditer(r'mailto:([^"\'\s>]+)', html, re.I):
        found.append(m.group(1))
    # then any bare address
    for m in EMAIL_RE.finditer(html):
        found.append(m.group(0))
    return found


def _normalize_site_url(raw: str) -> Optional[str]:
    """Clean a Maps website field into a scheme + bare host."""
    if not raw or not isinstance(raw, str):
        return None
    raw = raw.strip()
    if not raw.startswith(("http://", "https://")):
        raw = "https://" + raw
    try:
        p = urlparse(raw)
    except Exception:
        return None
    host = p.netloc.lower()
    if not host or host in {"", "none", "null"}:
        return None
    return f"{p.scheme}://{host}"


async def _fetch_one_site(client: httpx.AsyncClient, base: str) -> Optional[str]:
    """Fetch homepage + contact paths, return the best email found, or None."""
    seen_emails = []
    for path in CONTACT_PATHS:
        url = base + path
        try:
            resp = await client.get(url, headers=EMAIL_FETCH_HEADERS, follow_redirects=True)
        except (httpx.RequestError, httpx.HTTPError):
            continue
        if resp.status_code >= 400:
            continue
        # skip huge responses (avoid parsing MBs of JS)
        text = resp.text
        if len(text) > 2_000_000:
            text = text[:2_000_000]
        seen_emails.extend(_extract_emails_from_html(text))
        if seen_emails:
            # a real address on the homepage is usually enough; stop early
            best = _pick_best(seen_emails)
            if best:
                return best
    return _pick_best(seen_emails)


async def extract_emails(leads: list) -> tuple:
    """Visit each lead's website, extract a public contact email.

    Returns (enriched_leads, skipped_count). Only leads with a found email
    are included in enriched_leads; the rest are counted as skipped.
    """
    targets = []
    for lead in leads:
        base = _normalize_site_url(lead.get("website"))
        targets.append((lead, base))

    sem = asyncio.Semaphore(EMAIL_FETCH_CONCURRENCY)
    found = [None] * len(targets)

    async def worker(idx: int, lead: dict, base: Optional[str]):
        if not base:
            return
        async with sem:
            async with httpx.AsyncClient(timeout=EMAIL_FETCH_TIMEOUT) as client:
                try:
                    email = await _fetch_one_site(client, base)
                except Exception as e:
                    log.warning("email fetch failed for %s: %s", base, e)
                    email = None
        if email:
            lead_with_email = dict(lead)
            lead_with_email["email"] = email
            found[idx] = lead_with_email

    await asyncio.gather(*[worker(i, l, b) for i, (l, b) in enumerate(targets)])

    enriched = [x for x in found if x is not None]
    skipped = len(targets) - len(enriched)
    return enriched, skipped


@app.post("/scrape/maps-emails", response_model=EmailScrapeResponse)
async def scrape_maps_emails(req: ScrapeRequest):
    """Google Maps businesses enriched with a public website contact email.

    The email is pulled directly from each business's own website (homepage
    or contact page). Not every business publishes one, so some leads are
    skipped. We do not verify deliverability or use a private data source.
    """
    parsed = await parse_query(req.query)
    raw_items = await run_maps_actor(parsed)
    leads = trim_fields(raw_items)
    enriched, skipped = await extract_emails(leads)
    return EmailScrapeResponse(
        parsed_query=parsed,
        result_count=len(enriched),
        skipped_no_email=skipped,
        results=enriched,
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
