
import markdown
def md_to_html(md: str) -> str:
    return markdown.markdown(md, extensions=["extra", "fenced_code", "tables"])
