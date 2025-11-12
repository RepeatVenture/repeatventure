
from tenacity import retry, stop_after_attempt, wait_exponential

def net_retry():
    return retry(reraise=True, stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=30))
