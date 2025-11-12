
import tweepy, os
from ..logger import logger

def post_to_x(outdir, idea, tweets: list[str], images: list[bytes] | None):
    if not (os.getenv("X_API_KEY") and os.getenv("X_API_SECRET") and os.getenv("X_ACCESS_TOKEN") and os.getenv("X_ACCESS_TOKEN_SECRET")):
        raise RuntimeError("X/Twitter not configured")
    auth = tweepy.OAuth1UserHandler(
        os.getenv("X_API_KEY"), os.getenv("X_API_SECRET"),
        os.getenv("X_ACCESS_TOKEN"), os.getenv("X_ACCESS_TOKEN_SECRET")
    )
    api = tweepy.API(auth)
    if not tweets:
        tweets = [idea["title"]]
    first = api.update_status(status=tweets[0][:260])
    prev = first.id
    for t in tweets[1:]:
        tw = api.update_status(status=t[:260], in_reply_to_status_id=prev, auto_populate_reply_metadata=True)
        prev = tw.id
    logger.info("Posted tweet thread id=%s", first.id)
