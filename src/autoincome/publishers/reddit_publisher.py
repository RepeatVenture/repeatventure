
import os, praw
from ..logger import logger

def post_to_reddit(outdir, idea, reddit_payload: dict):
    need = ["REDDIT_CLIENT_ID","REDDIT_CLIENT_SECRET","REDDIT_USERNAME","REDDIT_PASSWORD","REDDIT_SUBREDDIT"]
    if any(not os.getenv(k) for k in need):
        raise RuntimeError("Reddit not configured")
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD"),
        user_agent="autoincome/1.1"
    )
    title = reddit_payload.get("title") or idea["title"]
    body = reddit_payload.get("body","")
    sub = reddit.subreddit(os.getenv("REDDIT_SUBREDDIT"))
    post = sub.submit(title=title, selftext=body)
    logger.info("Reddit posted: https://reddit.com%s", post.permalink)
