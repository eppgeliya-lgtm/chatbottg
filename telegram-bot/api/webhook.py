import os
from fastapi import FastAPI, Request
from bot import bot, dp  # импортируем bot и dp из bot.py
from aiogram.types import Update

app = FastAPI()

# POST-запрос для Telegram
@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# GET-запрос для проверки, что webhook доступен
@app.get("/webhook")
async def check():
    return {"ok": True, "message": "Webhook is alive"}
