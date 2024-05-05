# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from Handlers.admin_private import admin_private_router
from Handlers.user_private import user_private_router
import asyncio
import nest_asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import os
import aiosqlite

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())                        # Находим .env


dp = Dispatcher()
dp.include_routers(user_private_router, admin_private_router)
nest_asyncio.apply()
bot = Bot(token=os.getenv('TOKEN'))             # Подставляем значение TOKEN из .env


@dp.message(Command('start'))
async def start_command(message: types.Message) -> None:
    kb = [
        [types.InlineKeyboardButton(text="Обо мне", callback_data='about_me')],

        [
            types.InlineKeyboardButton(text="Имя", callback_data='name'),
            types.InlineKeyboardButton(
                text="Портфолио", url='https://github.com/Anatoliy0461/Malon')
        ],
        [
            types.InlineKeyboardButton(text="О тебе", callback_data='about_you')
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=kb, resize_keyboard=True)
    await message.answer('Привет! это мой бот-визитка', reply_markup=keyboard)

    async def get_user_count():
        connect = await aiosqlite.connect('db1')
        cursor = await connect.cursor()
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                full_name TEXT,
                username TEXT
            )
        ''')
    await get_user_count()
    # await add_user(user_id, full_name, username)

    async def add_user(user_id, full_name, username):
        # Соединяемся с db3, если нет - создаем
        connect = await aiosqlite.connect('db1')
        cursor = await connect.cursor()
        await cursor.execute('''INSERT INTO users (user_id, full_name, username) 
                             VALUES (?, ?, ?)''',
                             (user_id, full_name, username))
        await connect.commit()
        await cursor.close()
        await connect.close()
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username

    await add_user(user_id, full_name, username)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
