from config import bot_token, tmdb_token
from get_movie_info import display_movie_info
import logging
from aiogram import Bot, Dispatcher, executor, types
import keyboards as kb
from callback_data import menu_cd


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['help', 'start'])
async def send_help(message: types.Message):
    # the main info about the bot (what it can do) with all commands, their descriptions and starting menu
    await message.answer("КиноНавигатор\n\n"
                         "Я могу быстро найти много полезной информации о любом фильме, "
                         "а также помочь с поиском самых популярных фильмов любого жанра.\n\n"
                         "Для того, чтобы начать, просто отправь мне название интересующего тебя фильма "
                         "(я понимаю не только русский, но и английский язык) или воспользуйся кнопками ниже.\n\n"
                         "Также ты можешь пользоваться следующими командами для поиска различных фильмов:\n"
                         "• Отправь команду /popular для поиска популярных фильмов, в том числе "
                         "среди различных жанров\n"
                         "• Отправь команду /top_rated для поиска самых рейтинговых фильмов, в том числе "
                         "среди различных жанров\n"
                         "• Отправь команду /upcoming для поиска фильмов, которые скоро выйдут в кино, в том числе "
                         "среди различных жанров\n"
                         "• Отправь команду /help, чтобы в любой момент прочитать эту инструкцию ещё раз",
                         reply_markup=kb.start_keyboard())


@dp.message_handler(commands=['popular'])
async def send_top(message: types.Message):
    await message.answer("Выбери подходящий вариант", reply_markup=kb.trending_keyboard(start='0'))


@dp.message_handler(commands=['top_rated'])
async def send_top(message: types.Message):
    await message.answer("Выбери подходящий вариант", reply_markup=kb.top_rated_keyboard(start='0'))


@dp.message_handler(commands=['upcoming'])
async def send_top(message: types.Message):
    await message.answer("Выбери подходящий вариант", reply_markup=kb.upcoming_keyboard(start='0'))


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def movie_query(message: types.Message):
    movie_name = message.text
    try:
        markup = kb.movie_keyboard(source='1', movie_name=movie_name)
        await message.answer("Выберете интересующий вас фильм", reply_markup=markup)
    except:
        await message.answer("Проверьте название введённого фильма")


async def start_menu(call: types.CallbackQuery, **kwargs):
    try:
        markup = kb.start_keyboard()
        await call.message.edit_reply_markup(markup)
    except:
        await call.answer("Что-то пошло не так, попробуйте позже")


async def list_top(call: types.CallbackQuery, source, start, **kwargs):
    if source == '2':
        try:
            markup = kb.trending_keyboard(start)
            await call.message.edit_reply_markup(markup)
        except:
            await call.answer("Что-то пошло не так, попробуйте позже")
    elif source == '3':
        try:
            markup = kb.top_rated_keyboard(start)
            await call.message.edit_reply_markup(markup)
        except:
            await call.answer("Что-то пошло не так, попробуйте позже")
    elif source == '4':
        try:
            markup = kb.upcoming_keyboard(start)
            await call.message.edit_reply_markup(markup)
        except:
            await call.answer("Что-то пошло не так, попробуйте позже")


async def list_genres(call: types.CallbackQuery, source, start, **kwargs):
    try:
        markup = kb.genre_keyboard(source, start)
        await call.message.edit_text("Выберете интересующий вас жанр")
        await call.message.edit_reply_markup(markup)
    except:
        await call.answer("Что-то пошло не так, попробуйте позже")


async def list_possible_movies(call: types.CallbackQuery, source, **kwargs):
    try:
        markup = kb.movie_keyboard(source=source, **kwargs)
        await call.message.edit_text("Выберете интересующий вас фильм")
        await call.message.edit_reply_markup(markup)
    except:
        await call.answer("Что-то пошло не так, попробуйте позже")


async def movie_info(call: types.CallbackQuery, movie_id, **kwargs):
    try:
        movie_info = display_movie_info(movie_id, tmdb_token)
        markup = kb.movie_links_keyboard(movie_id, **kwargs)
        await call.message.edit_text(movie_info, parse_mode='Markdown')
        await call.message.edit_reply_markup(markup)
    except:
        await call.answer("Что-то пошло не так, попробуйте позже")


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level")
    source = callback_data.get("source")
    movie_name = callback_data.get("movie_name")
    genre_id = callback_data.get("genre_id")
    movie_id = callback_data.get("movie_id")
    start = callback_data.get("start")

    levels = {
        "0": start_menu,
        "1": list_top,
        "2": list_genres,
        "3": list_possible_movies,
        "4": movie_info
    }

    current_level_function = levels[current_level]

    await current_level_function(call, source=source, movie_name=movie_name,
                                 genre_id=genre_id, movie_id=movie_id, start=start)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
