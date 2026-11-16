# الترخيص: @TopVeGa
# العلامة التجارية: VEGA & Logic
# حقوق الطبع والنشر: © 2015 - 2025
import asyncio
import os

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
from pytgcalls import StreamType
from pytgcalls.types import AudioQuality, MediaStream, VideoQuality
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.exceptions import NoActiveGroupCall
from youtubesearchpython import VideosSearch

from config import bot, call_py
from plugins.helpers.queues import QUEUE, add_to_queue, get_queue

DOWNLOAD_DIR = "downloads"


def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:35] + "..."
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "bestaudio",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(filters.command(["/play", "شغل", "تشغيل"], ""))
async def play(client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    if replied:
        if replied.audio or replied.voice:
            await m.delete()
            huehue = await replied.reply("**جاري معالجة الطلب..**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:35] + "..."
                else:
                    songname = replied.audio.file_name[:35] + "..."
            elif replied.voice:
                songname = "ملاحظة صوتية"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/18d25616d9883400af112.png",
                    caption=f"""
**الأغنية في قائمة الانتظار رقم {pos}
العنوان: [{songname}]
الحالة: قيد التشغيل
الطالب: {m.from_user.mention}**
""",
                )
            else:
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(dl),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/18d25616d9883400af112.png",
                    caption=f"""
**بدء تشغيل الأغنية
العنوان: [{songname}]
الحالة: قيد التشغيل
بطلب من: {m.from_user.mention}**
""",
                )
    else:
        if len(m.command) < 2:
            await m.reply("قم بالرد على ملف صوتي أو أعطني شيئاً للبحث عنه")
        else:
            await m.delete()
            huehue = await m.reply("**جاري البحث عن الأغنية... يرجى الانتظار**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await huehue.edit("`لم يتم العثور على أي شيء للاستعلام المحدد`")
            else:
                songname = search[0]
                url = search[1]
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"**خطأ في التحميل** \n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await huehue.delete()
                        await m.reply_photo(
                            photo="https://qu.ax/aTong.jpg",
                            caption=f"""
**الأغنية في قائمة الانتظار رقم {pos}
العنوان: [{songname}]
الحالة: قيد التشغيل
بطلب من: {m.from_user.mention}**
""",
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(ytlink),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await huehue.delete()
                            await m.reply_photo(
                                photo="https://qu.ax/aTong.jpg",
                                caption=f"""
**بدء تشغيل الأغنية
العنوان: [{songname}]
الحالة: قيد التشغيل
بطلب من: {m.from_user.mention}**
""",
                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")


@Client.on_message(filters.command(["/videoplay", "فيديو"], ""))
async def videoplay(client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    if replied:
        if replied.video or replied.document:
            await m.delete()
            huehue = await replied.reply("**جاري معالجة الفيديو....**")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq in ["720", "480", "360"]:
                    Q = int(pq)
                else:
                    Q = 720
                    await huehue.edit(
                        "`يُسمح فقط بـ 720 أو 480 أو 360` \n`سيتم البث الآن بجودة 720p`"
                    )
            try:
                if replied.video:
                    songname = replied.video.file_name[:70]
                elif replied.document:
                    songname = replied.document.file_name[:70]
            except BaseException:
                songname = "ملف فيديو"

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await huehue.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/18d25616d9883400af112.png",
                    caption=f"""
**الفيديو في قائمة الانتظار رقم {pos}
العنوان: [{songname}]
الحالة: قيد التشغيل
بطلب من: {m.from_user.mention}**
""",
                )
            else:
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(dl, AudioQuality.HIGH, VideoQuality.HD_720p),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await huehue.delete()
                await m.reply_photo(
                    photo="https://qu.ax/aTong.jpg",
                    caption=f"""
**بدء تشغيل الفيديو
العنوان: [{songname}]
الحالة: قيد التشغيل
بطلب من: {m.from_user.mention}**
""",
                )
    else:
        if len(m.command) < 2:
            await m.reply("**قم بالرد على ملف صوتي أو أعطني شيئاً للبحث عنه**")
        else:
            await m.delete()
            huehue = await m.reply("**جاري البحث... يرجى الانتظار**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            if search == 0:
                await huehue.edit("**لم يتم العثور على أي شيء للاستعلام المحدد**")
            else:
                songname = search[0]
                url = search[1]
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"**خطأ في التحميل** \n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await huehue.delete()
                        await m.reply_photo(
                            photo="https://qu.ax/aTong.jpg",
                            caption=f"""
**الفيديو في قائمة الانتظار رقم {pos}
العنوان: [{songname}]
الحالة: قيد التشغيل
بطلب من: {m.from_user.mention}**
""",
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(ytlink, AudioQuality.HIGH, VideoQuality.HD_720p),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await huehue.delete()
                            await m.reply_photo(
                                photo="https://qu.ax/aTong.jpg",
                                caption=f"""
**بدء تشغيل الفيديو
العنوان: [{songname}]
الحالة: قيد التشغيل
بطلب من: {m.from_user.mention}**
""",
                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")


@Client.on_message(filters.command(["playfrom", "مين مشغل"], ""))
async def playfrom(client, m: Message):
    chat_id = m.chat.id
    if len(m.command) < 2:
        await m.reply("**أعطني اسم الدردشة أو معرفها**")
    else:
        args = m.text.split(maxsplit=1)[1]
        if ";" in args:
            chat = args.split(";")[0]
            limit = int(args.split(";")[1])
        else:
            chat = args
            limit = 10
            lmt = 9
        await m.delete()
        hmm = await m.reply(f"**جاري جلب {limit} أغنية عشوائية من {chat}**")
        try:
            async for x in bot.search_messages(chat, limit=limit, filter="audio"):
                location = await x.download()
                if x.audio.title:
                    songname = x.audio.title[:30] + "..."
                else:
                    songname = x.audio.file_name[:30] + "..."
                link = x.link
                if chat_id in QUEUE:
                    add_to_queue(chat_id, songname, location, link, "Audio", 0)
                else:
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(location),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, location, link, "Audio", 0)
                    await m.reply_photo(
                        photo="https://telegra.ph/file/18d25616d9883400af112.png",
                        caption=f"""
**بدء تشغيل الأغنية من {chat}
العنوان: [{songname}]
الحالة: قيد التشغيل
بطلب من: {m.from_user.mention}**
""",
                    )
            await hmm.delete()
            await m.reply(
                f"تمت إضافة {lmt} أغنية إلى قائمة الانتظار\nاضغط /playlist لعرض قائمة التشغيل**"
            )
        except Exception as e:
            await hmm.edit(f"**خطأ** \n`{e}`")


@Client.on_message(filters.command(["/playlist", "قائمتي"], ""))
async def playlist(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await m.delete()
            await m.reply(
                f"**يتم الآن تشغيل:** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
        else:
            QUE = f"**يتم الآن تشغيل:** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}` \n\n**قائمة الانتظار:**"
            l = len(chat_queue)
            for x in range(1, l):
                hmm = chat_queue[x][0]
                hmmm = chat_queue[x][2]
                hmmmm = chat_queue[x][3]
                QUE = QUE + "\n" + f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`\n"
            await m.reply(QUE, link_preview_options=LinkPreviewOptions(is_disabled=True))
    else:
        await m.reply("**لا يوجد شيء قيد التشغيل...**")