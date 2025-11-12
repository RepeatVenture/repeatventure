
import pathlib

def create_build_dir(date: str, slug: str) -> pathlib.Path:
    out = pathlib.Path("build") / f"{date}_{slug}"
    out.mkdir(parents=True, exist_ok=True)
    return out

def write_text(path: pathlib.Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def write_binary(path: pathlib.Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
