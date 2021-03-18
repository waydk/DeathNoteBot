from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from states.death_note import DeathNote
from stickers.dn_stickers import ryuk_write_down, death_note_sticker
from utils.db_api import db_helpers


@dp.message_handler(Command("write_down"))
async def write_in_death_note(message: types.Message):
    await message.answer("📓 You dared to use the death notebook, brave thing to do! Good luck!")
    await message.answer_sticker(death_note_sticker)
    await message.answer("Write the victim's first and last name \n"
                         "⚫------------------------------------- ⚫\n"
                         "    🖋example: Yagami Light")
    await DeathNote.surname_first_name.set()


@dp.message_handler(state=DeathNote.surname_first_name)
async def write_surname_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    surname_first_name = message.text
    victim_id = message.message_id
    await state.update_data(surname_first_name=surname_first_name,
                            user_id=user_id, victim_id=victim_id)
    await message.answer_sticker(ryuk_write_down)
    await message.answer("Write down the cause of death ✒\n\nUnless you want to give yours,"
                         "then the victim will die of a heart attack 💔⚰\n\nFor that,"
                         "write none ✒ ")
    await DeathNote.next()


@dp.message_handler(state=DeathNote.cause_of_death)
async def write_cause(message: types.Message, state: FSMContext):
    cause_of_death = message.text
    if cause_of_death == "None" or cause_of_death == "none":
        cause_of_death = "Heart attack"
    await state.update_data(cause_of_death=cause_of_death)
    data = await state.get_data()

    surname_first_name = data.get("surname_first_name")
    cause_of_death = data.get("cause_of_death")
    user_id = data.get("user_id")
    victim_id = data.get("victim_id")

    await db_helpers.add_victim(id_user=user_id, id_victim=victim_id, name_victim=surname_first_name,
                                reason=cause_of_death)

    await message.answer(f"✒ {surname_first_name} was recorded in the death notebook\n\n"
                         f"☠ Cause of death: "
                         f"{cause_of_death} 🍎 \n\n"
                         f"📓 Open death note:  /death_list")

    await state.finish()
