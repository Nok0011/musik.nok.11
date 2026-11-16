# الترخيص: @TopVeGa
# العلامة التجارية: VEGA & Logic
# حقوق الطبع والنشر: © 2015 - 2025
import os
import sys
from datetime import datetime
from time import time
from pyrogram import Client, filters
from pyrogram.types import Message
from config import SUDO_USERS

START_TIME = datetime.utcnow()
TIME_DURATION_UNITS = (
    ("أسبوع", 60 * 60 * 24 * 7),
    ("يوم", 60 * 60 * 24),
    ("ساعة", 60 * 60),
    ("دقيقة", 60),
    ("ثانية", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else ""))
    return ", ".join(parts)


@Client.on_message(filters.command(["/ping", "بينج"], ""))
async def ping(client, m: Message):
    start = time()
    current_time = datetime.utcnow()
    m_reply = await m.edit("جاري القياس...")
    delta_ping = time() - start
    await m_reply.edit("0% ▒▒▒▒▒▒▒▒▒▒")
    await m_reply.edit("20% ██▒▒▒▒▒▒▒▒")
    await m_reply.edit("40% ████▒▒▒▒▒▒")
    await m_reply.edit("60% ██████▒▒▒▒")
    await m_reply.edit("80% ████████▒▒")
    await m_reply.edit("100% ██████████")
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m_reply.edit(f"**بينج!! بوت الموسيقى**\n**المقياس**  - {delta_ping * 1000:.3f} ms \n**مدة التشغيل** - {uptime}")


@Client.on_message(filters.command(["/pong", "بينج"], ""))
async def pong(client, m: Message):
    start = time()
    current_time = datetime.utcnow()
    pkim = await m.edit("جاري القياس...")
    delta_ping = time() - start
    await pkim.edit("❏◈===❏")
    await pkim.edit("❏=◈==❏")
    await pkim.edit("❏==◈=❏")
    await pkim.edit("❏===◈❏")
    await pkim.edit("❏==◈=❏")
    await pkim.edit("❏=◈==❏")
    await pkim.edit("❏◈===❏")
    await pkim.edit("❏=◈==❏")
    await pkim.edit("❏==◈=❏")
    await pkim.edit("❏===◈❏")
    await pkim.edit("❏==◈=❏")
    await pkim.edit("❏=◈==❏")
    await pkim.edit("❏◈===❏")
    await pkim.edit("❏=◈==❏")
    await pkim.edit("❏==◈=❏")
    await pkim.edit("❏===◈❏")
    await pkim.edit("❏===◈❏◈")
    await pkim.edit("❏====❏◈◈")
    await pkim.edit("**بينغ!**")
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await pkim.edit(
        f"**بوت الموسيقى**\n**المقياس** : {delta_ping * 1000:.3f} ms\n**مدة تشغيل البوت** : {uptime}")


@Client.on_message(
    filters.user(SUDO_USERS) & filters.command(["/restart", "إعادة تشغيل"], "")
)
async def restart(client, m: Message):
    await m.delete()
    kim = await m.reply("1")
    await kim.edit("2")
    await kim.edit("3")
    await kim.edit("4")
    await kim.edit("5")
    await kim.edit("6")
    await kim.edit("7")
    await kim.edit("8")
    await kim.edit("9")
    await kim.edit("**تم إعادة تشغيل بوت الموسيقى**")
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()


@Client.on_message(filters.command(["/help", "المساعدة"], ""))
async def help(client, m: Message):
    await m.delete()
    HELP = f"""
<b>مرحباً {m.from_user.mention}!
قائمة مساعدة مشغل الموسيقى
الأوامر المتاحة للجميع
• /play [اسم الأغنية | رابط يوتيوب | رد على ملف صوتي] - لتشغيل أغنية
• /videoplay [اسم الفيديو | رابط يوتيوب | رد على ملف فيديو] - لتشغيل فيديو
• /playlist لعرض قائمة التشغيل
• /ping - للتحقق من الحالة
• /id - لعرض معرف المستخدم
• /video - اسم الفيديو | رابط يوتيوب للبحث عن فيديو
• /song - اسم الأغنية | رابط يوتيوب للبحث عن أغنية
• /help - لعرض قائمة الأوامر
• /join - للانضمام إلى المجموعة
الأوامر المتاحة للمشرفين
• /resume - لاستئناف تشغيل الأغنية أو الفيديو
• /pause - لإيقاف تشغيل الأغنية أو الفيديو مؤقتاً
• /skip - لتخطي الأغنية أو الفيديو
• /end - لإنهاء التشغيل</b>
"""
    await m.reply(HELP)