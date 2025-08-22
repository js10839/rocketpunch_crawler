import csv, os
from datetime import datetime
from ..models import CommunityPost

LOG_DIR = "app/log"
LOG_FILE = os.path.join(LOG_DIR, "posts.csv")

os.makedirs(LOG_DIR, exist_ok=True)

def load_posts() -> list[CommunityPost]:
    posts = []
    if not os.path.exists(LOG_FILE):
        return posts
    with open(LOG_FILE, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            posts.append(CommunityPost(**row))
    return posts

def append_post(post: CommunityPost) -> str:
    write_header = not os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["author","content","timestamp"])
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([post.author, post.content, ts])
    return ts