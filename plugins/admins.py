# الترخيص: @TopVeGa
# العلامة التجارية: VEGA & Logic
# حقوق الطبع والنشر: © 2015 - 2025
from pyrogram import Client, filters
from pyrogram.errors import (
    ChatAdminRequired,
    FloodWait,
    MessageNotModified,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LinkPreviewOptions,
    Message,
)
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types import AudioQuality, MediaStream
from config import call_py
from plugins.helpers.decorators import is_vega
from plugins.helpers.handlers import skip_current_song, skip_item
from plugins.helpers.queues import QUEUE, clear_queue


@Client.on_message(filters.command(["/skip", "تخطي"], ""))
@is_vega
async def skip(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("**لا يوجد شيء في قائمة الانتظار لتخطيه!**")
        elif op == 1:
            await m.reply("قائمة الانتظار فارغة، مغادرة الدردشة الصوتية**")
        else:
            await m.reply(
                f"**تم تخطي التشغيل** \n**يتم الآن تشغيل** - [{op[0]}]({op[1]}) | `{op[2]}`",
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "**إزالة الأغاني التالية من قائمة الانتظار: -**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(filters.command(["/end", "إيقاف"], ""))
@is_vega
async def stop(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("**تم إنهاء التشغيل**")
        except Exception as e:
            await m.reply(f"**خطأ** \n`{e}`")
    else:
        await m.reply("**لا يوجد شيء قيد التشغيل!**")


@Client.on_message(filters.command(["/pause", "وقف"], ""))
@is_vega
async def pause(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply("**تم إيقاف التشغيل مؤقتاً.**")
        except Exception as e:
            await m.reply(f"**خطأ** \n`{e}`")
    else:
        await m.reply("**لا يوجد شيء قيد التشغيل!**")


@Client.on_message(filters.command(["/resume", "كمل"], ""))
@is_vega
async def resume(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply("تم استئناف التشغيل المتوقف مؤقتاً")
        except Exception as e:
            await m.reply(f"**خطأ** \n`{e}`")
    else:
        await m.reply("**لا يوجد شيء متوقف مؤقتاً!**")