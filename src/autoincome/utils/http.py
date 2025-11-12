
import requests
def json_or_raise(resp: requests.Response):
    resp.raise_for_status()
    return resp.json() if resp.text.strip() else {}
