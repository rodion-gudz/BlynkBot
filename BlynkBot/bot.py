import re

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.utils import executor

from BlynkBot.db import db
from BlynkBot.main import *

bot = Bot(token=bot_token, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def get_user(email):
    async with aiohttp.ClientSession() as session:
        await session.post(f"{blynk_url}/admin/login",
                           data={"email": admin_email,
                                 "password": admin_password})
        data = await session.get(f"{blynk_url}/admin/users/{email}-Blynk")
        if data.status == 404:
            return False
        js = await data.json()
        js['energy'] = energy
        await session.put(f"{blynk_url}/admin/users/{email}-Blynk",
                          json=js)
        return True


@dp.message_handler(commands=["start"])
async def start(message: Message):
    await message.answer(f"<b>Приветствую вас, {message.from_user.mention}</b> \n"
                         f"<b>Для пополнения энергии введите ваш email</b>")
    await db.add_user(message.from_user.id)


@dp.message_handler()
async def echo(message: Message):
    if await db.check_user(message.from_user.id):
        await message.answer("<b>Вы уже увеличили количество энергии!</b>")
        return
    if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', message.text):
        await message.answer("<b>Пожалуйста введите верный email</b>")
        return
    user = await get_user(message.text)
    if not user:
        await message.answer(f"<b>Пользователь <code>{message.text}</code> не обнаружен!</b>")
        return
    await message.answer(f"<b>Энергия успешно пополнена до <code>{energy}</code></b>")
    db_user = await db.get_user(message.from_user.id)
    await db.add_email(db_user, message.text.strip())


def main():
    executor.start_polling(dp)
