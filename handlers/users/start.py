from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from stickers.dn_stickers import ryuk_hi
from utils.db_api import db_helpers


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    await message.answer_sticker(sticker=ryuk_hi)
    await message.answer(f"hello, {message.from_user.full_name}!\n\n"
                         f"You have the privilege of using the Death Note, so read the rules before you start:\n\n"
                         f"🍎 /rules 🖋 (click here) \n\n"
                         f"If you have read the rules, you can start using the death note: \n\n"
                         f"📓 /write_down 📓 (click here) \n\n"
                         f"Your Death Note:\n\n /death_list 📔 (click here)")
    name = message.from_user.full_name
    await db_helpers.add_user(id_user=message.from_user.id,
                              name=name)
