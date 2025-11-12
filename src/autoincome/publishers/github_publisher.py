
from github import Github
import pathlib, os
from ..logger import logger

def commit_to_github(outdir: pathlib.Path, idea: dict, md: str, html: str):
    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPO")
    if not (token and repo_name):
        raise RuntimeError("GitHub not configured")
    gh = Github(token)
    repo = gh.get_repo(repo_name)
    date = idea["date"]; slug = idea["slug"]
    dirpath = f"{os.getenv('GITHUB_CONTENT_DIR','site')}/{date}_{slug}"
    def upsert(path, content):
        full = f"{dirpath}/{path}"
        try:
            existing = repo.get_contents(full, ref=os.getenv('GITHUB_BRANCH','main'))
            repo.update_file(full, f"update {full}", content, existing.sha, branch=os.getenv('GITHUB_BRANCH','main'))
        except Exception:
            repo.create_file(full, f"add {full}", content, branch=os.getenv('GITHUB_BRANCH','main'))
    upsert("article.md", md)
    upsert("article.html", html)
    logger.info("Committed to GitHub at %s", dirpath)
