# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# async def root():
    return {"status": "ok"}

# @app.get("/memes")
# async def get_memes():
    # твой код для мемов
#     return []

# тест
# uvicorn app:app --reload --host 127.0.0.1 --port 8000
# http://127.0.0.1:8000/memes

# прод
# uvicorn app:app --host 0.0.0.0 --port $PORT