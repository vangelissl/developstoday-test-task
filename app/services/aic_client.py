import httpx
from datetime import datetime, timedelta, UTC

from ..config import settings

CACHE_TTL_MINUTES = 30

# { external_id: (data, fetched_at) }
_cache: dict[int, tuple[dict, datetime]] = {}


def _is_cached(external_id: int) -> bool:
    if external_id not in _cache:
        return False
    _, fetched_at = _cache[external_id]
    return datetime.now() - fetched_at < timedelta(minutes=CACHE_TTL_MINUTES)


async def fetch_artwork(external_id: int) -> dict:
    if _is_cached(external_id):
        return _cache[external_id][0]

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.aic_base_url}/artworks/{external_id}")

    if response.status_code == 404:
        raise ValueError(
            f"Artwork {external_id} not found in Art Institute of Chicago API")

    response.raise_for_status()
    data = response.json()["data"]
    _cache[external_id] = (data, datetime.now())
    return data


def parse_artwork(data: dict) -> dict:
    image_id = data.get("image_id")
    return {
        "title": data.get("title"),
        "artist": data.get("artist_display"),
        "image_url": f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg" if image_id else None,
    }
