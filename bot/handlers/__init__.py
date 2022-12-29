from .admin import register_admin_handlers
from .start import register_start_handlers
from .user import register_user_handlers
from aiogram import Dispatcher


def register_all_handlers(dp: Dispatcher):
    register_start_handlers(dp)
    register_user_handlers(dp)
    register_admin_handlers(dp)
