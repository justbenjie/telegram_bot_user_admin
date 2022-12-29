import enum
from gettext import find
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types.message import ParseMode
from aiogram.dispatcher import FSMContext
from sqlalchemy import select
import re
from states.user import AdminUpdateUser
from api_client.api_requests import api_requests
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.markup import create_markup, admin_main_menu, manage_admins_menu


async def manage_admins(message: types.Message):

    response = api_requests.get(f"/admins/")
    admins = response.json()

    for admin in admins:
        await message.answer(
            text=f"id: {admin['user']['id']}\nname: {admin['user']['name']}\nphone: {admin['user']['phone']}\ngender:{admin['user']['gender']}",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    "delete", callback_data=f"del admin {admin['user']['id']}"
                )
            ),
        )
    await message.answer(
        "You can delete or add admin", reply_markup=create_markup(manage_admins_menu)
    )


async def delete_admin(callback_query: types.CallbackQuery):
    admin_id = callback_query.data.replace("del admin ", "")
    api_requests.delete(f"/admins/{admin_id}")
    await callback_query.answer(
        text=f"admin with id: {admin_id} deleted", show_alert=True
    )


async def add_admin_button(message: types.Message):
    await message.answer("Give users id", reply_markup=types.ReplyKeyboardRemove())


async def add_admin(message: types.Message):

    user_id = message.text.strip()
    try:
        user_id = int(user_id)
    except:
        await message.answer(
            text="Invalid user id, try again", reply_markup=types.ReplyKeyboardRemove()
        )
        return

    response = api_requests.post("/admins/", json={"user_id": user_id})

    if response.status_code == 409:
        await message.answer(
            text=response.json()["detail"],
            reply_markup=create_markup(manage_admins_menu),
        )
        return

    if response.status_code == 201:
        await message.answer(
            text="successfully added", reply_markup=create_markup(manage_admins_menu)
        )


async def manage_users(message: types.Message):

    response = api_requests.get(f"/users/")
    users = response.json()

    for user in users:
        await message.answer(
            text=f"id: {user['id']}\nname: {user['name']}\nphone: {user['phone']}\ngender:{user['gender']}",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("name", callback_data=f"name user {user['id']}"),
                InlineKeyboardButton("phone", callback_data=f"phone user {user['id']}"),
                InlineKeyboardButton(
                    "gender", callback_data=f"gender user {user['id']}"
                ),
                InlineKeyboardButton("delete", callback_data=f"del user {user['id']}"),
            ),
        )


async def delete_user(callback_query: types.CallbackQuery):

    id = callback_query.data.replace("del user ", "")
    api_requests.delete(f"/users/{id}")
    await callback_query.answer(text=f"user with id: {id} deleted", show_alert=True)


async def name_user(callback_query: types.CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        data["id"] = callback_query.data.replace("name user ", "")

    await AdminUpdateUser.name.set()

    await callback_query.answer(text=f"Print Name:", show_alert=True)


async def phone_user(callback_query: types.CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        data["id"] = callback_query.data.replace("phone user ", "")

    await AdminUpdateUser.phone.set()

    await callback_query.answer(text=f"Print phone:", show_alert=True)


async def gender_user(callback_query: types.CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        data["id"] = callback_query.data.replace("gender user ", "")

    await AdminUpdateUser.gender.set()
    await callback_query.answer(text=f"Print gender:", show_alert=True)


async def add_name(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data["name"] = message.text
        dict_data = data.as_dict()

    user = api_requests.get(f"/users/{dict_data['id']}").json()
    user["name"] = dict_data["name"]

    response = api_requests.put(f"/users/{dict_data['id']}", json=user)
    await state.finish()
    await message.answer("Updated!")
    await message.answer("main menu")


async def add_phone(message: types.Message, state: FSMContext):

    phone = message.text.replace(" ", "")
    if not re.match(r"^(\+375|80)(29|25|44|33)(\d{7})$", phone):
        await message.answer("Invalid phone number, try again")
        return

    async with state.proxy() as data:
        data["phone"] = phone
        dict_data = data.as_dict()

    user = api_requests.get(f"/users/{dict_data['id']}").json()
    user["phone"] = dict_data["phone"]

    response = api_requests.put(f"/users/{dict_data['id']}", json=user)
    await state.finish()
    await message.answer("Updated!")
    await message.answer("main menu")


async def add_gender(message: types.Message, state: FSMContext):

    gender = message.text.strip()

    if gender not in ["male", "female", "other"]:
        await message.answer("Options: male, female, other")
        return

    async with state.proxy() as data:
        data["gender"] = gender
        dict_data = data.as_dict()

    user = api_requests.get(f"/users/{dict_data['id']}").json()
    user["gender"] = dict_data["gender"]

    response = api_requests.put(f"/users/{dict_data['id']}", json=user)
    await state.finish()
    await message.answer("Updated!")
    await message.answer("main menu")


def register_admin_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        delete_admin, lambda x: x.data and x.data.startswith("del admin")
    )
    dp.register_message_handler(manage_admins, Text(equals="manage admins"))

    dp.register_callback_query_handler(
        delete_user, lambda x: x.data and x.data.startswith("del user")
    )
    dp.register_callback_query_handler(
        name_user, lambda x: x.data and x.data.startswith("name user"), state="*"
    )
    dp.register_callback_query_handler(
        phone_user, lambda x: x.data and x.data.startswith("phone user"), state="*"
    )
    dp.register_callback_query_handler(
        gender_user, lambda x: x.data and x.data.startswith("gender user"), state="*"
    )
    dp.register_message_handler(manage_users, Text(equals="manage users"))
    dp.register_message_handler(add_admin_button, Text(equals="add"))
    dp.register_message_handler(add_admin)
    dp.register_message_handler(add_name, state=AdminUpdateUser.name)
    dp.register_message_handler(add_phone, state=AdminUpdateUser.phone)
    dp.register_message_handler(add_gender, state=AdminUpdateUser.gender)
