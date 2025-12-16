import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    Update
)
from aiogram.filters import CommandStart

# 🔐 ТОЛЬКО через env
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
KEYWORD = os.getenv("KEYWORD")
PHOTO_URL = os.getenv("PHOTO_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()

# --- Keyboards ---

get_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📥 Получить", callback_data="get_material")]
    ]
)

subscribe_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔔 Подписаться", url="https://t.me/gbjyfc")],
        [InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_sub")]
    ]
)

# --- Utils ---

async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in {"member", "administrator", "creator"}
    except Exception:
        return False

# --- Handlers ---

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет 👋\n\nНажми кнопку ниже, чтобы получить материал.",
        reply_markup=get_button
    )

@dp.message(F.text)
async def keyword_detector(message: Message):
    if message.chat.type in {"group", "supergroup"}:
        if KEYWORD.lower() in message.text.lower():
            await message.reply("👋 Напиши мне в личку 👉 @NataliaSamsonovabot")

@dp.callback_query(F.data == "get_material")
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

@dp.callback_query(F.data == "check_sub")
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

# --- Webhook endpoint ---

@app.post("/")
async def telegram_webhook(request: Request):
    update = Update.model_validate(await request.json())
    await dp.feed_update(bot, update)
    return {"ok": True}
