from loader import db
from loader import bot, storage
from src.utils.db_api import db_gino
from src.utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    import src.middlewares
    src.middlewares.setup(dp)

    await set_default_commands(dp)

    from src.utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await db_gino.on_startup(dp)
    await db.gino.create_all()


async def on_shutdown(dp):
    await bot.close()
    await storage.close()


if __name__ == '__main__':
    from aiogram import executor
    from src.handlers import dp

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
