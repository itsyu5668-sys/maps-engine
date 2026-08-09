"""
Apify actor shell for the Google Maps Email Extractor.

Thin wrapper, same pattern as actor #1: read the user's one text box,
forward it to the master FastAPI engine on Render, push the returned
leads (each now enriched with a public website contact email) into the
dataset. All real logic lives in the backend, not here.
"""

import os
import httpx
from apify import Actor

# Same engine as actor #1, just a different endpoint path. Set as an env
# var named ENGINE_BASE_URL on the actor (Settings > Environment variables)
# so it is not hardcoded in source.
ENGINE_BASE_URL = os.environ.get("ENGINE_BASE_URL", "https://maps-engine.onrender.com")


async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        query = actor_input.get("query", "").strip()

        if not query:
            await Actor.fail(status_message="No query provided - type what data you need.")
            return

        Actor.log.info(f"Forwarding query to engine: {query}")

        url = f"{ENGINE_BASE_URL}/scrape/maps-emails"
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
        skipped = data.get("skipped_no_email", 0)

        if not results:
            Actor.log.warning(
                f"Engine returned zero email leads ({skipped} businesses had no public email)."
            )

        # This is what Apify meters for Pay-Per-Result pricing - each item
        # pushed here counts as one billable result. Only leads with a found
        # email are pushed, so buyers pay only for usable contact rows.
        await Actor.push_data(results)

        Actor.log.info(
            f"Pushed {len(results)} email leads to the dataset "
            f"({skipped} skipped, no public email found)."
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(Actor.main(main))
