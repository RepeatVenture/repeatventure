
import os, requests
from ..logger import logger
from ..utils.backoff import net_retry

BASE = "https://api.gumroad.com/v2"

def _token():
    tok = os.getenv("GUMROAD_ACCESS_TOKEN")
    if not tok:
        raise RuntimeError("Gumroad not configured")
    return tok

@net_retry()
def create_offer_code(product_id: str, name: str, percent_off: int = 0, amount_off: int | None = None):
    params = {"access_token": _token(), "product_id": product_id, "name": name}
    if percent_off:
        params["percent_off"] = percent_off
    if amount_off is not None:
        params["amount_off"] = amount_off
    r = requests.post(f"{BASE}/offer_codes", data=params, timeout=60)
    r.raise_for_status()
    return r.json()
