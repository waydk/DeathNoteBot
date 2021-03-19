from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp, _
from src.states.death_note import DeathNote
from src.stickers.dn_stickers import ryuk_write_down, death_note_sticker
from src.utils.db_api import db_helpers


@dp.message_handler(Command("write_down"))
async def write_in_death_note(message: types.Message):
    text_dare = _("📓 You dared to use the death notebook, brave thing to do! Good luck!")
    text_victim = _("Write the victim's first and last name \n"
                    "⚫------------------------------------- ⚫\n"
                    "    🖋example: Yagami Light")
    await message.answer(text_dare)
    await message.answer_sticker(death_note_sticker)
    await message.answer(text_victim)
    await DeathNote.surname_first_name.set()


@dp.message_handler(state=DeathNote.surname_first_name)
async def write_surname_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    surname_first_name = message.text
    victim_id = message.message_id
    await state.update_data(surname_first_name=surname_first_name,
                            user_id=user_id, victim_id=victim_id)
    await message.answer_sticker(ryuk_write_down)
    text_cause_of_death = _("Write down the cause of death ✒\n\nUnless you want to give yours,"
                            "then the victim will die of a heart attack 💔⚰\n\nFor that,"
                            "write none ✒ ")
    await message.answer(text_cause_of_death)
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
    text_death_note = _("✒ {} was recorded in the death notebook\n\n"
                        "☠ Cause of death: "
                        "{} 🍎 \n\n"
                        "📓 Open death note:  /death_list").format(surname_first_name, cause_of_death)
    await message.answer(text_death_note)

    await state.finish()
