from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup
import logging
import requests

try:
    response = requests.get("https://memepedia.ru", timeout=5)
    print("Статус:", response.status_code)
    print("Первые 200 символов ответа:", response.text[:200])
except requests.exceptions.RequestException as e:
    print("Ошибка доступа к сайту:", e)

app = FastAPI(title="MCP Memes Server")

BASE_URL = "https://memepedia.ru"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_latest_memes(limit: int = 10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    resp = requests.get(BASE_URL, headers=headers, timeout=5)
    logger.info(f"HTTP status: {resp.status_code}")
    logger.info(f"Final URL after redirects: {resp.url}")
    logger.info(f"Response snippet (первые 1000 символов): {resp.text[:500]}")

    soup = BeautifulSoup(resp.text, "html.parser")
    logger.info(f"All h2 tags with class 'entry-title': {soup.find_all('h2', class_='entry-title')}")

    memes = []
    for entry in soup.find_all("h2", class_="entry-title")[:limit]:
        a_tag = entry.find("a")
        if not a_tag:
            continue
        title = a_tag.text.strip()
        url = BASE_URL + a_tag['href']
        memes.append({
            "title": title,
            "url": url
        })

    return memes

@app.get("/memes")
async def get_memes():
    data = fetch_latest_memes(limit=10)  # возвращаем 10 последних мемов
    return JSONResponse(content=data)

@app.get("/")
async def root():
    return {"status": "MCP Memes server running"}