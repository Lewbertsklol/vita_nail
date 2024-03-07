from aiogram import Router
from aiogram.types import Message
import requests


router = Router()


@router.message()
async def start_handler(message: Message):
    response = requests.get(headers='')
    pass
