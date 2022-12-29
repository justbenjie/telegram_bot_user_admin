from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from authorization import check_if_user_is_admin, check_if_user_exists
from states.user import User
from aiogram.dispatcher import FSMContext
from keyboards.markup import admin_main_menu, user_menu, create_markup


async def start_message(message: types.Message, state: FSMContext):

    await state.finish()

    admin = check_if_user_is_admin(message.from_user.id)
    user = check_if_user_exists(message.from_user.id)

    if admin:
        await message.answer(
            f"Admin menu",
            reply_markup=create_markup(admin_main_menu),
        )
    elif user:
        await message.answer(f"User menu", reply_markup=create_markup(user_menu))
    else:
        await User.name.set()
        await message.answer("Your name: ", reply_markup=types.ReplyKeyboardRemove())


def register_start_handlers(dp: Dispatcher):

    dp.register_message_handler(start_message, Text(equals="main menu"), state="*")
    dp.register_message_handler(start_message, commands="start", state="*")
