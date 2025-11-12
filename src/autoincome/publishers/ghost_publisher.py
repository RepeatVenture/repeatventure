
import time, json, requests, jwt, os
from urllib.parse import urljoin
from ..logger import logger
from ..utils.backoff import net_retry

def _ghost_jwt(admin_key: str) -> str:
    key_id, secret = admin_key.split(":")
    iat = int(time.time())
    header = {"alg": "HS256", "kid": key_id, "typ": "JWT"}
    payload = {"iat": iat, "exp": iat + 5 * 60, "aud": "/admin/"}
    return jwt.encode(payload, bytes.fromhex(secret), algorithm="HS256", headers=header)

@net_retry()
def publish_to_ghost(outdir, idea, html: str):
    admin_url = os.getenv("GHOST_ADMIN_URL")
    admin_key = os.getenv("GHOST_ADMIN_KEY")
    if not admin_url or not admin_key:
        raise RuntimeError("Ghost not configured")
    token = _ghost_jwt(admin_key)
    api = urljoin(admin_url.rstrip('/') + '/', "ghost/api/admin/posts/?source=html")
    headers = {"Authorization": f"Ghost {token}", "Content-Type": "application/json"}
    payload = {"posts": [{
        "title": idea["title"],
        "html": html,
        "status": "published",
        "tags": [{"name": t} for t in idea.get("keywords", [])[:5]]
    }]}
    r = requests.post(api, headers=headers, data=json.dumps(payload), timeout=60)
    if r.status_code >= 400:
        raise RuntimeError(f"Ghost publish failed: {r.status_code} {r.text[:200]}")
    data = r.json()
    logger.info("Ghost post published")
    return data
