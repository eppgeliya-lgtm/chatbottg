from fastapi import FastAPI, Request
from bot import bot, dp
from aiogram.types import Update

app = FastAPI()

# POST-запрос от Telegram
@app.post("/webhook")
async def webhook(request: Request):
    """
    Telegram будет слать обновления сюда через POST
    """
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}

# GET-запрос для проверки доступности webhook
@app.get("/webhook")
async def check_webhook():
    """
    Проверка доступности webhook через браузер
    """
    return {"ok": True, "message": "Webhook is alive"}
