"""
Apify actor shell for the Google Maps skin.

This file does almost nothing on purpose: it reads the user's one text
box, forwards it to the master FastAPI engine (deployed separately on
Render), and pushes whatever comes back into the actor's dataset. All
the real logic (query parsing, calling the wrapped Maps actor) lives in
the backend, not here - so every future actor "skin" is just a copy of
this file pointed at a different backend route.
"""

import os
import httpx
from apify import Actor

# Set this to your deployed Render URL once you have it, e.g.
# "https://maps-engine.onrender.com". Can also be set as an env var
# named ENGINE_BASE_URL on the actor itself (Settings > Environment
# variables) so you don't hardcode it in code.
ENGINE_BASE_URL = os.environ.get("ENGINE_BASE_URL", "https://REPLACE-ME.onrender.com")


async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        query = actor_input.get("query", "").strip()

        if not query:
            await Actor.fail(status_message="No query provided - type what data you need.")
            return

        Actor.log.info(f"Forwarding query to engine: {query}")

        url = f"{ENGINE_BASE_URL}/scrape/maps"
        async with httpx.AsyncClient(timeout=300) as client:
            try:
                resp = await client.post(url, json={"query": query})
            except httpx.RequestError as e:
                await Actor.fail(status_message=f"Could not reach engine: {e}")
                return

        if resp.status_code != 200:
            await Actor.fail(
                status_message=f"Engine returned an error ({resp.status_code}): {resp.text[:300]}"
            )
            return

        data = resp.json()
        results = data.get("results", [])

        if not results:
            Actor.log.warning("Engine returned zero results for this query.")

        # This is what Apify meters for Pay-Per-Result pricing - each
        # item pushed here counts as one billable result.
        await Actor.push_data(results)

        Actor.log.info(f"Pushed {len(results)} results to the dataset.")
