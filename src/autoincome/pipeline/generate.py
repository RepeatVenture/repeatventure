
import os, json, pathlib, argparse
from openai import OpenAI
from ..config import settings
from ..logger import logger
from .ideas import pick_topic
from .render import md_to_html
from .package import create_build_dir, write_text, write_binary

from ..publishers.ghost_publisher import publish_to_ghost
from ..publishers.buffer_publisher import post_via_buffer
from ..publishers.beehiiv_publisher import publish_to_beehiiv
from ..publishers.twitter_publisher import post_to_x
from ..publishers.reddit_publisher import post_to_reddit
from ..publishers.github_publisher import commit_to_github

def _client():
    return OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

def generate_content(client, idea: dict) -> dict:
    if not client:
        return {
            "article_md": "# Configure OPENAI_API_KEY to generate\n",
            "newsletter_blurb": "Add OPENAI_API_KEY to enable content generation.",
            "tweets": [idea["title"]],
            "reddit": {"title": idea["title"], "body": "Configure OPENAI_API_KEY."}
        }
    system = f"You are a strategist for '{settings.brand_name}'. Tone: {settings.brand_tone}. Niche: {settings.content_niche}."
    user = f"""Create:
1) A 1200-1600 word Markdown article titled "{idea['title']}" with a walkthrough, checklist, and mini case study.
2) A 120-160 word newsletter intro.
3) 3 tweet-length posts (max 260 chars).
4) 1 Reddit post (title + body, helpful).

Return **only** JSON with keys: article_md, newsletter_blurb, tweets (list), reddit (dict with title, body)."""
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        temperature=0.7
    )
    txt = resp.choices[0].message.content
    try:
        data = json.loads(txt)
    except Exception:
        data = {"article_md": txt, "newsletter_blurb": txt[:300], "tweets": [], "reddit": {"title": idea["title"], "body": txt[:1000]}}
    return data

def generate_images(client, idea: dict) -> list[bytes]:
    if not client:
        return []
    prompt = f"Minimal, high-contrast header illustration for article: {idea['title']} — topic {settings.content_niche}. No text."
    img = client.images.generate(prompt=prompt, size="1024x1024", n=1)
    import base64
    return [base64.b64decode(img.data[0].b64_json)]

def run_full_pipeline(dry_run: bool=False):
    idea = pick_topic(settings.content_niche)
    outdir = create_build_dir(idea["date"], idea["slug"])
    client = _client()

    data = generate_content(client, idea)
    article_md = data["article_md"]
    html = md_to_html(article_md)

    write_text(outdir / "article.md", article_md)
    write_text(outdir / "article.html", html)
    write_text(outdir / "newsletter.txt", data["newsletter_blurb"])
    write_text(outdir / "tweets.json", json.dumps(data.get("tweets", []), indent=2))
    write_text(outdir / "reddit.json", json.dumps(data.get("reddit", {}), indent=2))

    images = []
    if client:
        try:
            images = generate_images(client, idea)
        except Exception as e:
            logger.info("Image generation failed: %s", e)
    for i, b in enumerate(images):
        write_binary(outdir / f"image_{i+1}.png", b)

    if not dry_run:
        for fn in [
            lambda: publish_to_ghost(outdir, idea, html),
            lambda: publish_to_beehiiv(outdir, idea, html, data["newsletter_blurb"]),
            lambda: post_via_buffer((data.get("tweets",[idea["title"]])[0])),
            lambda: post_to_x(outdir, idea, data.get("tweets", []), images[:1] if images else None),
            lambda: post_to_reddit(outdir, idea, data.get("reddit", {})),
            lambda: commit_to_github(outdir, idea, article_md, html),
        ]:
            try:
                fn()
            except Exception as e:
                logger.info("Publisher skipped or failed: %s", e)

    logger.info("Done. Output in %s", outdir)

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    run_full_pipeline(dry_run=args.dry_run)
