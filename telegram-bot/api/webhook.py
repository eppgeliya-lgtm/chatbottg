import os
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import FastAPI, Request

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()

@app.post("/webhook")
async def handler(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, Update.model_validate(data))
    return {"ok": True}

# Для проверки через браузер
@app.get("/webhook")
async def check():
    return {"ok": True, "message": "Webhook is alive"}
