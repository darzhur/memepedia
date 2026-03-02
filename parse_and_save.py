import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime
import cloudscraper


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

scraper = cloudscraper.create_scraper()
resp = scraper.get("https://memepedia.ru")
print(resp.text[:500])

BASE_URL = "https://memepedia.ru"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


def fetch_memes(limit=10):
    """
    Получаем список последних мемов с memepedia.ru с главной страницы
    """
    scraper = cloudscraper.create_scraper()
    response = scraper.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    memes = []

    for entry in soup.select("h2.entry-title a")[:limit]:
        title = entry.text.strip()
        page_url = entry["href"]

        memes.append({
            "title": title,
            "page_url": page_url
        })

    return memes


def save_to_original_db(meme):
    supabase.table("memepedia").insert({
        "title": meme["title"],
        "source_url": meme["page_url"],
        "created_at": datetime.utcnow().isoformat()
    }).execute()


def main(limit=20):
    memes = fetch_memes(limit=limit)
    for meme in memes:
        print(f"Сохраняем: {meme['title']}")
        save_to_original_db(meme)

    print(f"Готово. Сохранено {len(memes)} мемов в memepedia.")

if __name__ == "__main__":
    main(limit=20)