import asyncio
import time
import aiohttp

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    BotCommand
)
from aiogram.types.input_file import URLInputFile

from config import (
    BOT_TOKEN,
    API_URL,
    CHANNEL_USERNAME,
    SPAM_DELAY,
    GITHUB_URL,
    SUPPORT_USERNAME
)


bot = Bot(
    token=BOT_TOKEN
)

dp = Dispatcher()


user_requests = {}



# ======================
# Keyboards
# ======================

def main_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🎬 دانلود ویدیو",
                    callback_data="download"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🤝 همکاری با ما",
                    callback_data="cooperation"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🎯 هدف توسعه",
                    callback_data="goal"
                )
            ],

            [
                InlineKeyboardButton(
                    text="💻 GitHub",
                    url=GITHUB_URL
                ),

                InlineKeyboardButton(
                    text="👤 پشتیبانی",
                    url=f"https://t.me/{SUPPORT_USERNAME.replace('@','')}"
                )
            ]
        ]
    )



def join_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="📢 عضویت کانال",
                    url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"
                )
            ],

            [
                InlineKeyboardButton(
                    text="✅ بررسی عضویت",
                    callback_data="check_join"
                )
            ]
        ]
    )



# ======================
# Anti Spam
# ======================

def check_spam(user_id):

    now = time.time()

    if user_id in user_requests:

        diff = now - user_requests[user_id]

        if diff < SPAM_DELAY:

            return int(SPAM_DELAY - diff)


    user_requests[user_id] = now

    return 0



# ======================
# Force Join
# ======================

async def check_member(user_id):

    try:

        member = await bot.get_chat_member(
            CHANNEL_USERNAME,
            user_id
        )

        return member.status in [
            "member",
            "administrator",
            "creator"
        ]

    except:

        return False



async def require_join(message):

    if await check_member(
        message.from_user.id
    ):

        return True


    await message.answer(

        "🔒 <b>دسترسی محدود</b>\n\n"

        "برای استفاده از ربات ابتدا عضو کانال شوید.",

        reply_markup=join_keyboard(),

        parse_mode="HTML"

    )

    return False



# ======================
# Start Tag
# ======================

@dp.message(Command("start"))
async def start(message: Message):

    if not await require_join(message):

        return


    await message.answer(

        "╭━━━ 🎬 DownloaderCrowBot ━━━╮\n\n"

        "👋 سلام\n\n"

        "🎥 لینک ویدیو را ارسال کنید\n"

        "تا دانلود شود.\n\n"

        "╰━━━━━━━━━━━━━━╯",

        reply_markup=main_keyboard()

    )



# ======================
# Debug Tag
# ======================

@dp.message(Command("debug"))
async def debug(message: Message):

    await message.answer(

        "🛠 <b>Debug Mode</b>\n\n"

        "🟢 Bot: Online\n"

        "🟢 API: Ready\n"

        "🟢 Force Join: Active\n"

        "🟢 Anti Spam: Active\n"

        "🟢 Direct Stream: Active\n\n"

        "✅ سیستم آماده تست و رفع باگ است.",

        parse_mode="HTML"

    )



# ======================
# Menu Callback
# ======================

@dp.callback_query()
async def menu(callback: CallbackQuery):


    if callback.data == "download":

        await callback.message.answer(

            "🎬 لینک اینستاگرام را ارسال کنید."

        )


    elif callback.data == "cooperation":

        await callback.message.edit_text(

            "🤝 <b>همکاری با ما</b>\n\n"

            "ما آماده همکاری در پروژه‌های دیجیتال هستیم.\n\n"

            "🤖 ربات تلگرام\n"

            "🌐 وب‌سایت\n"

            "⚙️ API و سرویس اختصاصی\n"

            "📱 اپلیکیشن\n\n"

            "برای همکاری با ما ارتباط بگیرید.",

            parse_mode="HTML"

        )


    elif callback.data == "goal":

        await callback.message.edit_text(

            "🎯 <b>هدف توسعه</b>\n\n"

            "ساخت ابزارهای سریع و کاربردی\n"

            "برای ساده‌تر کردن کار کاربران.\n\n"

            "🚀 توسعه مداوم\n"

            "⚡ افزایش سرعت\n"

            "🌐 اضافه کردن سرویس‌های بیشتر",

            parse_mode="HTML"

        )


    elif callback.data == "check_join":

        if await check_member(
            callback.from_user.id
        ):

            await callback.message.edit_text(

                "✅ عضویت تایید شد.\n\n"

                "حالا لینک ویدیو را ارسال کنید."

            )

        else:

            await callback.answer(

                "❌ هنوز عضو کانال نیستید",

                show_alert=True

            )



# ======================
# Download
# ======================

@dp.message()
async def download(message: Message):


    if not await require_join(message):

        return



    remaining = check_spam(
        message.from_user.id
    )


    if remaining:

        await message.answer(

            f"⚠️ لطفاً {remaining} ثانیه صبر کنید."

        )

        return



    url = message.text


    if not url or "instagram.com" not in url:

        return



    if "/stories/" in url:

        await message.answer(

            "⏳ دانلود استوری\n\n"

            "این قابلیت به زودی اضافه خواهد شد."

        )

        return



    status = await message.answer(

        "⏳ در حال آماده سازی..."

    )



    try:

        async with aiohttp.ClientSession() as session:

            async with session.get(

                f"{API_URL}/stream",

                params={
                    "url": url
                }

            ) as response:

                data = await response.json()



        if data.get("status") != "success":

            await status.edit_text(

                "❌ دانلود ناموفق بود."

            )

            return



        video = URLInputFile(

            data["video_url"],

            filename="instagram.mp4"

        )


        await status.delete()


        await message.answer_video(

            video,

            caption=(

                "╭━━━ 🎬 Instagram Downloader ━━━╮\n\n"

                "✅ ویدیو آماده شد\n\n"

                "📊 اطلاعات فایل:\n"

                "├ 📦 حجم: Original\n"

                "├ 🎞 کیفیت: Original\n"

                "└ 📁 فرمت: MP4\n\n"

                "😊 همیشه لبخند بزن\n\n"

                "━━━━━━━━━━━━━━\n"

                "🤖 @Downloadercrowbot\n"

                "╰━━━━━━━━━━━━━━╯"

            )

        )


    except Exception as e:

        await status.edit_text(

            f"❌ خطا:\n{e}"

        )



async def main():

    await bot.set_my_commands([

        BotCommand(
            command="start",
            description="🏠 خانه"
        ),

        BotCommand(
            command="debug",
            description="🛠 رفع ارور"
        )

    ])


    print(
        "🤖 Bot Started"
    )


    await dp.start_polling(bot)



if __name__ == "__main__":

    asyncio.run(main())