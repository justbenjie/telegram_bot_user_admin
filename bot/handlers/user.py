import enum
from gettext import find
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types.message import ParseMode
from aiogram.dispatcher import FSMContext
from sqlalchemy import select
import re
from api_client.api_requests import api_requests
from authorization import check_if_user_is_admin, check_if_user_exists
from states.user import User
from keyboards.markup import (
    genders,
    user_menu,
    create_markup,
    profile_menu,
    admin_main_menu,
)


async def profile(message: types.Message):

    id = message.from_user.id
    response = api_requests.get(f"/users/{id}")
    user = response.json()

    await message.answer(
        f"id: {user['id']}\nname: {user['name']}\nphone: {user['phone']}\ngender:{user['gender']}",
        reply_markup=create_markup(profile_menu),
    )


async def change_profile(message: types.Message):

    await User.name.set()
    await message.answer("Your name: ", reply_markup=types.ReplyKeyboardRemove())


async def add_name(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data["name"] = message.text

    await User.phone.set()
    await message.answer("Your phone number:")


async def add_phone(message: types.Message, state: FSMContext):

    phone = message.text.replace(" ", "")
    if not re.match(r"^(\+375|80)(29|25|44|33)(\d{7})$", phone):
        await message.answer("Invalid phone number, try again")
        return
    async with state.proxy() as data:
        data["phone"] = message.text

    await User.gender.set()
    await message.answer("Your gender:", reply_markup=create_markup(genders))


async def add_gender(message: types.Message, state: FSMContext):

    id = message.from_user.id

    if message.text not in ["male", "female", "other"]:
        await message.answer("Use the buttons for choosing your gender")
        return

    async with state.proxy() as data:
        data["gender"] = message.text
        dict_data = data.as_dict()

    await state.finish()

    if check_if_user_exists(id):
        response = api_requests.put(f"/users/{id}", json=dict_data)
    else:
        dict_data["id"] = id
        response = api_requests.post("/users/", json=dict_data)

    if check_if_user_is_admin(id):
        markup = admin_main_menu
    else:
        markup = user_menu

    await message.answer("main menu", reply_markup=types.ReplyKeyboardRemove())


async def cancel(message: types.Message, state: FSMContext):

    await state.finish()
    await message.answer("Canceled", reply_markup=types.ReplyKeyboardRemove())


def register_user_handlers(dp: Dispatcher):

    dp.register_message_handler(cancel, commands="cancel", state="*")
    dp.register_message_handler(profile, Text(equals="profile"))
    dp.register_message_handler(change_profile, Text(equals="update"))
    dp.register_message_handler(add_name, state=User.name)
    dp.register_message_handler(add_phone, state=User.phone)
    dp.register_message_handler(add_gender, state=User.gender)
