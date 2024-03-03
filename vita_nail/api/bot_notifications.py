from datetime import datetime
import os

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums.parse_mode import ParseMode
from .models import Window


TOKEN = os.environ['BOT_TOKEN']
MY_CHAT_ID = os.environ['MY_CHAT_ID']
VIOLA_CHAT_ID = os.environ['VIOLA_CHAT_ID']


def create_message(window: Window) -> str:
    return f'Записался клиент:\n'\
        f'{window.date}\n'\
        f'{window.user.phone}\n'\
        f'{window.user}\n'\



async def send_notification_by_tgbot(
    window: Window
) -> None:
    session = AiohttpSession()
    bot = Bot(TOKEN, session=session)
    message = create_message(window)
    # await bot.send_message(MY_CHAT_ID, message, parse_mode=ParseMode.HTML)
    # await bot.send_message(VIOLA_CHAT_ID, message)  #! для Виолетты
    await session.close()
