import os
from fastapi import FastAPI, Request
from bot import bot, dp
from aiogram.types import Update

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}

@app.get("/webhook")
async def check():
    return {"ok": True, "message": "Webhook is alive"}

