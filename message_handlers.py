from aiogram import types, Dispatcher
import keyboards
from constants import help_text


async def send_help(message: types.Message):
    # the main info about the bot (what it can do) with all commands, their descriptions and starting menu
    await message.answer(help_text, reply_markup=keyboards.start_keyboard())


async def send_top(message: types.Message):
    command = message.get_command()

    if command == "/popular":
        reply_markup = keyboards.trending_keyboard(start='0')
    elif command == "/top_rated":
        reply_markup = keyboards.top_rated_keyboard(start='0')
    else:
        reply_markup = keyboards.upcoming_keyboard(start='0')

    await message.answer("Выбери подходящий вариант", reply_markup=reply_markup)


async def movie_query(message: types.Message):
    movie_name = message.text
    try:
        markup = keyboards.movie_keyboard(source='1', movie_name=movie_name)
        await message.answer("Выберете интересующий вас фильм", reply_markup=markup)
    except Exception:
        await message.answer("Проверьте название введённого фильма")


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(send_help, commands=['help', 'start'])
    dispatcher.register_message_handler(send_top, commands=['popular', 'top_rated', 'upcoming'])
    dispatcher.register_message_handler(movie_query, content_types=types.ContentTypes.TEXT)
