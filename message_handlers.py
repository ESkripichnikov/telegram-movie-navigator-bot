from aiogram import types, Dispatcher
import keyboards
from callback_data import Source
from constants import help_text


async def send_help(message: types.Message):
    # the main info about the bot (what it can do) with all commands, their descriptions and starting menu
    await message.answer(help_text, reply_markup=keyboards.create_starting_keyboard())


async def send_top(message: types.Message):
    command = message.get_command()

    if command == "/popular":
        reply_markup = keyboards.create_popular_keyboard()
    elif command == "/top_rated":
        reply_markup = keyboards.create_top_rated_keyboard()
    else:
        reply_markup = keyboards.create_upcoming_keyboard()

    await message.answer("Выбери подходящий вариант", reply_markup=reply_markup)


async def movie_query(message: types.Message):
    movie_name = message.text
    try:
        markup = keyboards.create_movies_keyboard(source=Source.movie_request.value, movie_name=movie_name)
        await message.answer("Выберете интересующий вас фильм", reply_markup=markup)
    except Exception:
        await message.answer("Проверьте название введённого фильма")


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(send_help, commands=['help', 'start'])
    dispatcher.register_message_handler(send_top, commands=['popular', 'top_rated', 'upcoming'])
    dispatcher.register_message_handler(movie_query, content_types=types.ContentTypes.TEXT)
