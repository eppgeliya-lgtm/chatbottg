import os
import asyncio
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import CommandStart

BOT_TOKEN = os.environ.get("8525182861:AAEZlNNf0m1U_KS7ZcuB9WksJkGlvvmflfM")  # берём из Environment Variables
CHANNEL_ID = -1001343482992
KEYWORD = "Хочу"
PHOTO_URL = "https://sun9-54.userapi.com/s/v1/ig2/iJUFH3WYpQeoE4ey_5AeHpQpEeNAg9rX6AqB0iRfbwbErDdAnJDQy3YCGQA0MQQ8nmuz_tmDAxp25DlOwRQHx9Fx.jpg"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()

# Кнопки
get_button = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="📥 Получить", callback_data="get_material")]]
)

subscribe_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔔 Подписаться", url="https://t.me/gbjyfc")],
        [InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_sub")]
    ]
)

# Проверка подписки
async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ("member", "administrator", "creator")
    except:
        return False

# /start
@dp.message(CommandStart())
async def start(message: Message):
    if message.chat.type == "private":
        await message.answer(
            "Привет 👋\n\nНажми кнопку ниже, чтобы получить материал.",
            reply_markup=get_button
        )

# Ключевое слово в группах
@dp.message(lambda message: True)
async def keyword_detector(message: Message):
    if message.chat.type in ["group", "supergroup"]:
        if KEYWORD.lower() in message.text.lower():
            await message.reply("👋 Напиши мне в личку 👉 @NataliaSamsonovabot")

# Получить материал
@dp.callback_query(lambda c: c.data == "get_material")
async def get_material(callback: CallbackQuery):
    if not await check_subscription(callback.from_user.id):
        await callback.message.answer(
            "❗ Подпишись на канал 👇",
            reply_markup=subscribe_button
        )
        await callback.answer()
        return

    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo=PHOTO_URL,
        caption="🎉 Вот твой материал!"
    )
    await callback.answer()

# Проверка подписки
@dp.callback_query(lambda c: c.data == "check_sub")
async def check_again(callback: CallbackQuery):
    if await check_subscription(callback.from_user.id):
        await bot.send_photo(
            chat_id=callback.from_user.id,
            photo=PHOTO_URL,
            caption="🎉 Спасибо за подписку!"
        )
    else:
        await callback.message.answer("❌ Ты ещё не подписан")
    await callback.answer()

# FastAPI webhook endpoint
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = types.Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}

# GET для проверки URL через браузер
@app.get("/webhook")
async def check():
    return {"ok": True, "message": "Webhook is alive"}


