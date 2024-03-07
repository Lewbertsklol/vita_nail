from enum import Enum
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

class Commands(Enum):
    START = '/start'
    NEW_ADMIN = 'Создать нового администратора'
    ACCEPT = 'Подтвердить'
    DECLINE = 'Отклонить'
    
    
inline_new_admin_keyboard = InlineKeyboardBuilder().add(
    InlineKeyboardButton(
        text=Commands.NEW_ADMIN.value,
        url='http://127.0.0.1:8000/api/v1/admins'
    )
)
