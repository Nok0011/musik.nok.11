# الترخيص: @TopVeGa
# العلامة التجارية: VEGA & Logic
# حقوق الطبع والنشر: © 2015 - 2025
import asyncio
from pytgcalls import idle
from config import call_py, bot


async def main():
    print("بدء تشغيل عميل بنجاح")
    await bot.start()
    print("بدء تشغيل عميل PYTGCALLS")
    await call_py.start()
    await idle()
    print("إيقاف البوت المستخدم")
    await bot.stop()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())