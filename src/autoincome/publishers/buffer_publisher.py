
import os, requests
from ..logger import logger
from ..utils.backoff import net_retry

API = "https://api.bufferapp.com/1"

@net_retry()
def post_via_buffer(text: str, link: str | None = None, media_url: str | None = None, scheduled_at: int | None = None):
    token = os.getenv("BUFFER_ACCESS_TOKEN")
    profile_ids = [p.strip() for p in os.getenv("BUFFER_PROFILE_IDS","").split(",") if p.strip()]
    if not token or not profile_ids:
        raise RuntimeError("Buffer not configured")

    payload = {"text": (text + (f"\n{link}" if link else ""))[:280]}
    for idx, pid in enumerate(profile_ids):
        payload[f"profile_ids[{idx}]"] = pid
    if scheduled_at:
        payload["scheduled_at"] = int(scheduled_at)
    else:
        payload["now"] = True
    r = requests.post(f"{API}/updates/create.json", data=payload, params={"access_token": token}, timeout=60)
    if r.status_code >= 400:
        raise RuntimeError(f"Buffer post failed: {r.status_code} {r.text[:200]}")
    logger.info("Buffer post queued/sent")
    return r.json()
