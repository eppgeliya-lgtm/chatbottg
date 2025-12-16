import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import CommandStart

BOT_TOKEN = "8525182861:AAEZlNNf0m1U_KS7ZcuB9WksJkGlvvmflfM"
CHANNEL_ID = -1001343482992
KEYWORD = "Хочу"
PHOTO_URL = "https://sun9-54.userapi.com/s/v1/ig2/iJUFH3WYpQeoE4ey_5AeHpQpEeNAg9rX6AqB0iRfbwbErDdAnJDQy3YCGQA0MQQ8nmuz_tmDAxp25DlOwRQHx9Fx.jpg?quality=95&as=32x32,48x48,72x72,108x108,160x160,240x240,360x360,480x480,540x540,640x640,720x720,1024x1024&from=bu&cs=1024x0"  # ссылка на фото

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

get_button = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="📥 Получить", callback_data="get_material")]]
)

subscribe_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔔 Подписаться", url="https://t.me/gbjyfc")],
        [InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_sub")]
    ]
)

async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ("member", "administrator", "creator")
    except:
        return False

@dp.message(CommandStart())
async def start(message: Message):
    if message.chat.type == "private":
        await message.answer(
            "Привет 👋\n\nНажми кнопку ниже, чтобы получить материал.",
            reply_markup=get_button
        )

@dp.message(F.text)
async def keyword_detector(message: Message):
    if message.chat.type in ["group", "supergroup"]:
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

async def main():
    print("Бот запущен ✅")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
