# Maps Engine - Repository Memory

## Project
GitHub: `itsyu5668-sys/maps-engine` (public)
Apify account: `grand_knightship` (token in env APIFY_TOKEN, NOT committed)
Render service: maps-engine.onrender.com (FastAPI)
User is "Wahlberg". No AI/openhands references in commits. No em/en dashes in marketing content.

## Architecture
- Backend engine: `/workspace/maps-engine/main.py` (FastAPI) deployed on Render.
  Holds ALL real logic: `parse_query` (Groq LLM), `run_maps_actor` (wraps
  scraperlink~google-maps-scraper), `trim_fields`, email enrichment.
- Actor shells: thin wrappers in `apify-actor-*` that take one input, POST to
  a backend endpoint, push results to dataset. Copy-of pattern for new actors.

## Deployed actors
- Actor #1: `ai-google-maps-scraper` (ID: FkDDorieSZ97lOMLJ), endpoint /scrape/maps
- Actor #2: `ai-google-maps-email-extractor` (ID: QAWR5a0weHSFNA1Xr, NOT published),
  endpoint /scrape/maps-emails, build 0.1.2, last run SUCCEEDED (9 real Dallas roofer emails)

## Key env vars (set on Render service)
GROQ_API_KEY, APIFY_TOKEN, MAPS_ACTOR_ID=scraperlink~google-maps-scraper,
RENDER_API_KEY (for manual deploys). Actor shells need ENGINE_BASE_URL set on the actor.

## Critical gotchas (hard-won)
- Apify actor.json `description` field: strict 300 char limit. Long honesty notes
  go in README.md (Apify renders README as Store page).
- actor.json `environmentVariables`: must be `{"KEY": "value"}` NOT
  `{"KEY": {"value": "value"}}` (throws "Value must be of type String").
- Apify actor `src/main.py`: use `Actor.main(main)` as entry point. Do NOT combine
  `async with Actor:` AND `Actor.main(main)` - newer SDK raises
  "The actor was already initialized".
- `trim_fields` must always emit phone+website (nullable). Google Maps lacks
  phone for some businesses. Schema permits null.
- `parse_query` max_results floored at 10 (underlying actor rejects num < 10).
- Render autoDeploy is OFF. Trigger deploys manually via API.

## Marketing conventions
- Blog posts: human first-person voice, 500-800 words, no em/en dashes
  (grep -P "[\x{2014}\x{2013}]" to verify clean).
- Sample CSVs: real data from production endpoint, run across 5-10 verticals.
- Honesty required: emails scraped from public business websites, NOT verified,
  NOT deliverability-checked. ~40-50% hit rate for contractors.

## Reusable template
`ACTOR_BUILDER_TEMPLATE.md` at repo root: full A-to-Z actor build process.

## Git workflow
User "openhands" openhands@all-hands.dev + Co-authored-by line in commits.
Commit messages: conventional commits (feat/fix/docs). No AI references.
