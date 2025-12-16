from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update
import os

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@app.get("/")
async def health():
    return {"status": "ok"}

@app.post("/")
async def telegram_webhook(request: Request):
    update = Update.model_validate(await request.json())
    await dp.feed_update(bot, update)
    return {"ok": True}
