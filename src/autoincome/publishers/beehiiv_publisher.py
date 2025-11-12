
import requests, json, os
from ..logger import logger
from ..utils.backoff import net_retry

BASE = "https://api.beehiiv.com/v2"

@net_retry()
def publish_to_beehiiv(outdir, idea, html: str, blurb: str):
    key = os.getenv("BEEHIIV_API_KEY")
    pub = os.getenv("BEEHIIV_PUBLICATION_ID")
    if not key or not pub:
        raise RuntimeError("Beehiiv not configured")
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {"title": idea["title"], "subtitle": blurb[:140], "content": html, "audience": "all", "status": "draft"}
    r = requests.post(f"{BASE}/publications/{pub}/posts", headers=headers, data=json.dumps(payload), timeout=60)
    if r.status_code >= 400:
        raise RuntimeError(f"Beehiiv failed: {r.status_code} {r.text[:200]}")
    logger.info("Beehiiv draft created")
    return r.json()
