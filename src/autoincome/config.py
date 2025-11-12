
import os
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseModel):
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    # Ghost
    ghost_admin_url: str | None = os.getenv("GHOST_ADMIN_URL")
    ghost_admin_key: str | None = os.getenv("GHOST_ADMIN_KEY")
    # Buffer
    buffer_access_token: str | None = os.getenv("BUFFER_ACCESS_TOKEN")
    buffer_profile_ids: str | None = os.getenv("BUFFER_PROFILE_IDS")
    # Beehiiv
    beehiiv_api_key: str | None = os.getenv("BEEHIIV_API_KEY")
    beehiiv_publication_id: str | None = os.getenv("BEEHIIV_PUBLICATION_ID")
    # X
    x_api_key: str | None = os.getenv("X_API_KEY")
    x_api_secret: str | None = os.getenv("X_API_SECRET")
    x_access_token: str | None = os.getenv("X_ACCESS_TOKEN")
    x_access_token_secret: str | None = os.getenv("X_ACCESS_TOKEN_SECRET")
    # Reddit
    reddit_client_id: str | None = os.getenv("REDDIT_CLIENT_ID")
    reddit_client_secret: str | None = os.getenv("REDDIT_CLIENT_SECRET")
    reddit_username: str | None = os.getenv("REDDIT_USERNAME")
    reddit_password: str | None = os.getenv("REDDIT_PASSWORD")
    reddit_subreddit: str | None = os.getenv("REDDIT_SUBREDDIT")
    # GitHub
    github_token: str | None = os.getenv("GITHUB_TOKEN")
    github_repo: str | None = os.getenv("GITHUB_REPO")
    github_branch: str = os.getenv("GITHUB_BRANCH", "main")
    github_content_dir: str = os.getenv("GITHUB_CONTENT_DIR", "site")
    # Gumroad
    gumroad_access_token: str | None = os.getenv("GUMROAD_ACCESS_TOKEN")
    gumroad_product_ids: str | None = os.getenv("GUMROAD_PRODUCT_IDS")
    # App
    cron: str = os.getenv("AUTO_POST_SCHEDULE_CRON", "5 10 * * *")
    brand_name: str = os.getenv("BRAND_NAME", "RepeatVenture")
    brand_tone: str = os.getenv("BRAND_TONE", "insightful, forward-thinking, data-driven, a bit witty")
    content_niche: str = os.getenv("CONTENT_NICHE", "AI automation, solopreneur income systems, digital scalability")

settings = Settings()
