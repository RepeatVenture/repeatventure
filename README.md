
# autoincome (RepeatVenture edition) — fully automated content generation & publishing

Generates content and auto-publishes to **Ghost**, **Buffer** (multi-network social), **Beehiiv**, **Twitter/X**, **Reddit**, and **GitHub Pages**. Any platform missing credentials is **skipped gracefully**.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.template .env
# fill in the keys you actually use
```

Run once (generate + publish):
```bash
python scripts/run_once.py
```

Daemon scheduler:
```bash
python -m autoincome.main
```

## Configure `.env`

Only fill what you use. Missing creds = module skipped.

```
# Brand
BRAND_NAME=RepeatVenture
BRAND_TONE=insightful, forward-thinking, data-driven, a bit witty
CONTENT_NICHE=AI automation, solopreneur income systems, digital scalability

# OpenAI
OPENAI_API_KEY=

# Ghost (Admin API)
GHOST_ADMIN_URL=         # e.g. https://yourblog.ghost.io
GHOST_ADMIN_KEY=         # Admin API key format: key_id:secret

# Buffer
BUFFER_ACCESS_TOKEN=
BUFFER_PROFILE_IDS=      # comma-separated profile IDs

# Beehiiv (optional)
BEEHIIV_API_KEY=
BEEHIIV_PUBLICATION_ID=

# X / Twitter (optional direct, Buffer is preferred)
X_API_KEY=
X_API_SECRET=
X_ACCESS_TOKEN=
X_ACCESS_TOKEN_SECRET=

# Reddit (optional)
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USERNAME=
REDDIT_PASSWORD=
REDDIT_SUBREDDIT=

# GitHub Pages (optional)
GITHUB_TOKEN=
GITHUB_REPO=owner/repo
GITHUB_BRANCH=main
GITHUB_CONTENT_DIR=site

# Gumroad (optional offer codes)
GUMROAD_ACCESS_TOKEN=
GUMROAD_PRODUCT_IDS=     # comma-separated product ids

# Scheduler
AUTO_POST_SCHEDULE_CRON=5 10 * * *
```

## Platform Behavior

- **Ghost**: publishes full HTML article as **published** using Admin API.
- **Buffer**: posts the first social update (tweet-length) to all listed profiles (immediate or scheduled).
- **Beehiiv**: creates a **draft** issue from HTML.
- **X/Twitter**: direct thread posting if keys present (you can rely on Buffer instead).
- **Reddit**: posts to a specified subreddit.
- **GitHub**: commits Markdown + HTML to your Pages repo.

## Logs
Logs write to `logs/run.log`. Re-running same day reuses the same idea slug to avoid duplicates.
