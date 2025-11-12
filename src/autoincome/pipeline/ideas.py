
from datetime import date
def pick_topic(niche: str) -> dict:
    today = date.today().isoformat()
    return {
        "slug": f"{today}-automation-quick-win",
        "title": "A 30-Minute Automation That Saves You 3 Hours/Week",
        "keywords": ["automation", "solopreneur", "time-savings"],
        "date": today,
    }
