import os
import requests
from enum import Enum
from typing import NamedTuple


from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from .models import Window


TOKEN = os.environ['BOT_TOKEN']
MY_CHAT_ID = os.environ['MY_CHAT_ID']
VIOLA_CHAT_ID = os.environ['VIOLA_CHAT_ID']


class CommandScheme(NamedTuple):
    text: str
    url: str


class Commands(Enum):
    ACCEPT = CommandScheme('Принять', 'http://127.0.0.1:8000/api/v1/windows/')
    DECLINE = CommandScheme('Отклонить', 'http://127.0.0.1:8000/api/v1/windows/')


inline_accepting_keyboard = InlineKeyboardBuilder().row(
    InlineKeyboardButton(
        text=Commands.ACCEPT.value.text,
        url=Commands.ACCEPT.value.url,
    ),
    InlineKeyboardButton(
        text=Commands.DECLINE.value.text,
        url=Commands.DECLINE.value.url
    )
).as_markup()


def create_message(window: Window) -> str:
    return f'Записался клиент:\n'\
        f'{window.date.strftime('%d.%m.%y на %H:%M')}\n'\
        f'{window.client.phone}\n'\
        f'{window.client.name} {window.client.surname}\n'\



async def send_notification_by_tgbot(
    window: Window
) -> None:
    session = AiohttpSession()
    bot = Bot(TOKEN, session=session)
    message = create_message(window)
    # await bot.send_message(MY_CHAT_ID, message, reply_markup=inline_accepting_keyboard)
    # await bot.send_message(VIOLA_CHAT_ID, message)  #! для Виолетты
    await session.close()
