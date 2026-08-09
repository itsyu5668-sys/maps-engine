# Actor Builder Template

A repeatable A to Z process for building and shipping an Apify Store actor
that wraps a backend engine. This is the exact workflow used to ship actor
#1 (AI Google Maps Scraper) and actor #2 (AI Google Maps Email Extractor)
on the grand_knightship Apify account, both backed by the same Render
FastAPI service.

Use this as a checklist for every new actor.

---

## 0. What you are building

Two parts:

1. A backend engine (FastAPI on Render) that holds all real logic: query
   parsing, calling wrapped Apify actors, data cleaning, enrichment.
2. A thin Apify actor shell that takes one user input, POSTs it to a backend
   endpoint, and pushes the response into the Apify dataset.

The actor shell does almost nothing on purpose. Every new actor is a copy
of the shell pointed at a different backend route. This keeps the engine
in one place and makes new actors cheap.

---

## 1. Backend: add the endpoint

In `main.py` (the engine), add a new route. Reuse existing helpers
(`parse_query`, `run_maps_actor`, `trim_fields`) wherever possible.

```python
@app.post("/scrape/<new-endpoint>", response_model=NewResponse)
async def scrape_new(req: ScrapeRequest):
    parsed = await parse_query(req.query)
    raw_items = await run_maps_actor(parsed)
    leads = trim_fields(raw_items)
    # ... your enrichment step ...
    return NewResponse(parsed_query=parsed, result_count=len(results), results=results)
```

Rules:
- Reuse `parse_query` for natural language to structured params.
- Reuse `run_maps_actor` for the underlying Maps scrape.
- Reuse `trim_fields` for clean output rows.
- Add enrichment as a separate async function, concurrency limited with
  `asyncio.Semaphore`, real timeouts, real User-Agent.
- Be honest in the docstring about what the endpoint does and does not do.

## 2. Test locally before deploying

```bash
export GROQ_API_KEY=... APIFY_TOKEN=... MAPS_ACTOR_ID=...
python3 -c "
import asyncio, json, main as m
async def run():
    parsed = await m.parse_query('your test query')
    raw = await m.run_maps_actor(parsed)
    leads = m.trim_fields(raw)
    # call your enrichment
    results, skipped = await m.your_enrichment(leads)
    print(len(results), 'skipped', skipped)
    for r in results[:5]: print(json.dumps(r))
asyncio.run(run())
"
```

Confirm real data comes back before you touch Render.

## 3. Push to GitHub and redeploy Render

```bash
git add -A
git commit -m "feat: add /scrape/<endpoint> + actor shell"
git push origin main
```

Trigger a Render deploy (autoDeploy is off by design):

```bash
RENDER_API_KEY=... SID=srv-<id>
curl -X POST -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.render.com/v1/services/$SID/deploys" -d '{"clearCache":"clear"}'
```

Poll until status is `live`:

```bash
curl -H "Authorization: Bearer $RENDER_API_KEY" \
  "https://api.render.com/v1/services/$SID/deploys/$DID"
```

## 4. Verify all endpoints on production

```bash
curl https://maps-engine.onrender.com/health
# must return {"status":"ok"}

curl -X POST https://maps-engine.onrender.com/scrape/maps \
  -H "Content-Type: application/json" \
  -d '{"query":"coffee shops in Austin"}'
# regression: actor #1 must still work

curl -X POST https://maps-engine.onrender.com/scrape/<new-endpoint> \
  -H "Content-Type: application/json" \
  -d '{"query":"your test query"}'
# new endpoint must return real data
```

## 5. Build the actor shell

Create `apify-actor-<name>/` with this structure:

```
apify-actor-<name>/
  .actor/
    actor.json
    input_schema.json
    dataset_schema.json
  src/
    main.py
  Dockerfile
  requirements.txt
  README.md
```

### actor.json

```json
{
  "actorSpecification": 1,
  "name": "ai-google-maps-<name>",
  "title": "AI Google Maps <Title> | <Subtitle>",
  "description": "<under 300 chars, include honesty note>",
  "version": "0.1",
  "input": "./input_schema.json",
  "datasetSchema": "./dataset_schema.json",
  "dockerfile": "../Dockerfile",
  "environmentVariables": {
    "ENGINE_BASE_URL": "https://maps-engine.onrender.com"
  }
}
```

Notes from hard lessons:
- `description` is capped at 300 chars. Put the full honest explanation
  in README.md instead.
- `environmentVariables` values are plain strings, not `{"value": "..."}`.
  The nested form throws "Value must be of type String".

### input_schema.json

Single text box. One required field: `query`.

### dataset_schema.json

Draft 2020-12 JSON schema with rich field metadata: title, description,
example for every field. Mark nullable fields as `["string", "null"]`.
Define a `views.overview` table with the lead fields first.

### src/main.py

The shell. Reads the query, POSTs to the backend endpoint, pushes results.
Use `Actor.main(main)` as the entry point. Do NOT use both
`async with Actor:` and `Actor.main(main)` together, the newer SDK raises
"The actor was already initialized".

### Dockerfile

```dockerfile
FROM apify/actor-python:3.12
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./
CMD ["python3", "-m", "src.main"]
```

### requirements.txt

```
apify>=1.7.0,<2.0.0
httpx>=0.27.0,<1.0.0
```

## 6. Push the actor to Apify

```bash
npm install -g apify-cli  # if not installed
apify login --token $APIFY_TOKEN
cd apify-actor-<name>
apify actors push
```

This creates the actor (if the name is new) or updates it, builds the
Docker image, and returns the Actor ID and Build ID.

If the actor was created but the build failed on a config error, fix the
config and re-run `apify actors push`. It updates in place.

## 7. Run the real end-to-end test

```bash
AID=<actor-id>
curl -X POST -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.apify.com/v2/acts/$AID/run-sync-get-dataset-items" \
  -d '{"query":"your test query"}'
```

This runs the actor synchronously and returns the dataset items directly.
Confirm real data comes back. If the run fails, check the log:

```bash
RUN_ID=<run-id>
curl "https://api.apify.com/v2/actor-runs/$RUN_ID/log?token=$APIFY_TOKEN"
```

## 8. STOP before Publish

Do not click Publish on Apify. Hand the test output back to the user.
The user does pricing and publishing manually on the Apify dashboard.

## 9. Marketing (after user go-ahead, or in parallel)

- Sample CSV: run the endpoint across 5 to 10 verticals, write to
  `marketing/<name>_sample_data.csv`.
- Blog posts: 10 posts in `marketing/blog-<name>/`, human first person
  voice, no em/en dashes (use hyphens or commas), 500 to 800 words each.
- Each post targets a specific use case or vertical.

## 10. SEO Tasks (after user go-ahead only)

Create 10 to 15 Apify Tasks off the actor, each pre-filled with a
different high intent query. Bias toward mid size cities and commercial
lead gen categories.

---

## Gotchas logged from building actors #1 and #2

- `description` field is capped at 300 chars. Long honesty notes go in
  README.md.
- `environmentVariables` must be `{"KEY": "value"}`, not
  `{"KEY": {"value": "value"}}`.
- Do not use `async with Actor:` and `Actor.main(main)` together. Pick
  `Actor.main(main)` and drop the context manager.
- The Apify SDK version that gets resolved can change behavior. Actor #1
  was built with an older SDK that tolerated the double init. Actor #2
  with the current SDK did not. Always test the run after pushing.
- `trim_fields` must always emit phone and website. They are core contact
  fields, not optional based on the query. Google Maps does not have a
  phone for every business, so phone may be null. The schema permits null.
- `max_results` from the parser must be floored at 10. Some underlying
  actors reject `num` values below 10.
- Render autoDeploy should be off. Trigger deploys manually so you control
  timing and can verify each one.

## Credentials used

- GROQ_API_KEY: Groq, for natural language query parsing.
- APIFY_TOKEN: Apify, for running the wrapped Maps actor and pushing the
  actor shell. Token belongs to the grand_knightship account.
- MAPS_ACTOR_ID: the underlying Google Maps actor being wrapped.
  Currently `scraperlink~google-maps-scraper`.
- RENDER_API_KEY: Render, for triggering manual deploys.

All four are set as environment variables on the Render service. The
actor shell only needs `ENGINE_BASE_URL` set on the actor itself.
