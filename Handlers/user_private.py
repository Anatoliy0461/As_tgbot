from aiogram import Bot, Router, F, types
from aiogram.filters import Command
import os

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'))

user_private_router = Router()


@user_private_router.callback_query(F.data == "about_me")
async def about_me_callback(callback: types.CallbackQuery):
    await callback.message.edit_text('Рад, что ты спросил\n'
                                     'Я на самом деле редко говорю о себе, но мама говорит, что я классный')


@user_private_router.callback_query(F.data == 'name')
async def name_callback(callback: types.CallbackQuery):
    # await callback.message.answer(f'Меня зовут {(await Bot.get_me()).username}. '
    bot_info = await bot.get_me()
    await callback.message.answer(f'Меня зовут {bot_info.username}, '

                                  f'А как тебя зовут? Хотя, можешь не отвечать, я не смогу прочитать')


@user_private_router.callback_query(F.data == 'portfolio')
async def portfolio_callback(callback: types.CallbackQuery):
    await callback.message.answer('Я пока что только учусь, и ещё не успел создать ботов, но скоро они здесь будут')


@user_private_router.callback_query(F.data == 'about_you')
async def about_you_callback(callback: types.CallbackQuery):
    await callback.message.answer(f'А тебя зовут {callback.from_user.full_name}!')
