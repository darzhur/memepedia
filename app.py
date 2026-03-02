from fastapi import FastAPI
from fastapi.responses import JSONResponse
from supabase import create_client_async
import os
from dotenv import load_dotenv
import logging

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client_async(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="MCP Memes Server")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/memes")
async def get_memes(limit: int = 10):
    try:
        resp = await supabase.table("memepedia")\
            .select("title, content, source_url")\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()
        memes = resp.data if resp.data else []
        return JSONResponse(content=memes)
    except Exception as e:
        logger.error(f"Ошибка Supabase: {e}")
        return JSONResponse(content={"error": "Не удалось получить мемы"}, status_code=500)

@app.get("/")
async def root():
    return {"status": "MCP Memes server running"}