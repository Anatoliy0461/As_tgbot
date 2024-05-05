# Здесь собираем админку
from aiogram import Bot, Router, F, types
from aiogram.filters import Command, Filter
import aiosqlite

admin_private_router = Router()

admin_ids = [399456313]


class IsAdmin(Filter):
    async def __call__(self, obj: types.Message) -> bool:
        return obj.from_user.id in admin_ids


admin_kb = [
    [
        types.InlineKeyboardButton(
            text='Рассылка', callback_data='admin_newsletter'),
        types.InlineKeyboardButton(
            text='Статистика', callback_data='admin_statistic')
    ]
]
admin_kb = types.InlineKeyboardMarkup(inline_keyboard=admin_kb)


@admin_private_router.message(Command('admin'), IsAdmin())
async def admin_command(message: types.Message) -> None:
    await message.answer('Добро пожаловать в Админ-панель!',
                         reply_markup=admin_kb)


async def get_user_count():
    connect = await aiosqlite.connect('db1')
    cursor = await connect.cursor()
    user_count = await cursor.execute('SELECT COUNT(*) FROM users')
    user_count = await user_count.fetchone()  # .fetchall() выведет
    # список кортежей, где каждый кортеж
    # представляет одну строку
    # из таблицы "users"
    await cursor.close()
    await connect.close()
    return user_count[0]


@admin_private_router.callback_query(F.data == 'admin_statistic', IsAdmin())
async def admin_statistic(call: types.CallbackQuery):
    user_count = await get_user_count()
    await call.message.edit_text('Статистика\n\n'
                                 f'Количество пользователей: {user_count}')


@admin_private_router.callback_query(F.data == 'admin_newsletter', IsAdmin())
async def admin_newsletter(call: types.CallbackQuery):
    await call.message.edit_text('Рассылка\nВведите сообщение, '
                                 'которое будет отправлено пользователям')
