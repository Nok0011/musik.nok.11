# الترخيص: @TopVeGa
# العلامة التجارية: VEGA & Logic
# حقوق الطبع والنشر: © 2015 - 2025
from pyrogram.raw.base import Update
from pyrogram.types import LinkPreviewOptions
from pytgcalls.types import AudioQuality, MediaStream, StreamEnded, VideoQuality

from config import bot, call_py
from plugins.helpers.queues import QUEUE, clear_queue, get_queue, pop_an_item


async def skip_current_song(chat_id):
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            return 1
        else:
            songname = chat_queue[1][0]
            url = chat_queue[1][1]
            link = chat_queue[1][2]
            type = chat_queue[1][3]
            Q = chat_queue[1][4]
            if type == "Audio":
                await call_py.change_stream(
                    chat_id,
                    MediaStream(
                        url,
                        audio_parameters=AudioQuality.HIGH,
                    ),
                )
            elif type == "Video":
                await call_py.change_stream(
                    chat_id,
                    MediaStream(
                        url,
                        audio_parameters=AudioQuality.HIGH,
                        video_parameters=VideoQuality.HD_720p,
                    ),
                )
            pop_an_item(chat_id)
            return [songname, link, type]
    else:
        return 0


async def skip_item(chat_id, h):
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        try:
            x = int(h)
            songname = chat_queue[x][0]
            chat_queue.pop(x)
            return songname
        except Exception as e:
            print(e)
            return 0
    else:
        return 0


@call_py.on_stream_end()
async def on_end_handler(_, update: Update):
    if isinstance(update, StreamEnded):
        chat_id = update.chat_id
        print(chat_id)
        op = await skip_current_song(chat_id)
        if op == 0:
            return
        else:
            await bot.send_message(
                chat_id,
                f"**يتم الآن تشغيل** \n[{op[0]}]({op[1]}) | `{op[2]}`",
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )