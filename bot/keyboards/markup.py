from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_main_menu = ["manage users", "manage admins", "profile"]
genders = ["male", "female", "other"]
user_menu = ["profile"]
manage_admins_menu = ["add", "main menu"]
profile_menu = ["update", "main menu"]


def create_markup(texts):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for text in texts:
        markup.add(KeyboardButton(text=text))

    return markup
