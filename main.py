import logging
from message_handlers import register_handlers
from aiogram import Bot, Dispatcher, executor, types
import keyboards as kb
from callback_data import menu_cd
from config import bot_token, tmdb_token
from get_movie_info import display_movie_info


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=bot_token)
dispatcher = Dispatcher(bot)

register_handlers(dispatcher)


async def start_menu(call: types.CallbackQuery, **kwargs):
    try:
        markup = kb.start_keyboard()
        await call.message.edit_text("Выберете подходящий вариант")
        await call.message.edit_reply_markup(markup)
    except Exception:
        await call.answer("Что-то пошло не так, попробуйте позже")


async def list_top(call: types.CallbackQuery, source, start, **kwargs):
    if source == '2':
        try:
            markup = kb.trending_keyboard(start)
            await call.message.edit_text("Выберете интересующий вас фильм")
            await call.message.edit_reply_markup(markup)
        except Exception:
            await call.answer("Что-то пошло не так, попробуйте позже")
    elif source == '3':
        try:
            markup = kb.top_rated_keyboard(start)
            await call.message.edit_text("Выберете интересующий вас фильм")
            await call.message.edit_reply_markup(markup)
        except Exception:
            await call.answer("Что-то пошло не так, попробуйте позже")
    elif source == '4':
        try:
            markup = kb.upcoming_keyboard(start)
            await call.message.edit_text("Выберете интересующий вас фильм")
            await call.message.edit_reply_markup(markup)
        except Exception:
            await call.answer("Что-то пошло не так, попробуйте позже")


async def list_genres(call: types.CallbackQuery, source, start, **kwargs):
    try:
        markup = kb.genre_keyboard(source, start)
        await call.message.edit_text("Выберете интересующий вас жанр")
        await call.message.edit_reply_markup(markup)
    except Exception:
        await call.answer("Что-то пошло не так, попробуйте позже")


async def list_possible_movies(call: types.CallbackQuery, source, **kwargs):
    try:
        markup = kb.movie_keyboard(source=source, **kwargs)
        await call.message.edit_text("Выберете интересующий вас фильм")
        await call.message.edit_reply_markup(markup)
    except Exception:
        await call.answer("Что-то пошло не так, попробуйте позже")


async def movie_info(call: types.CallbackQuery, movie_id, **kwargs):
    try:
        movie_info = display_movie_info(movie_id, tmdb_token)
        markup = kb.movie_links_keyboard(movie_id, **kwargs)
        await call.message.edit_text(movie_info, parse_mode='Markdown')
        await call.message.edit_reply_markup(markup)
    except Exception:
        await call.answer("Что-то пошло не так, попробуйте позже")


@dispatcher.callback_query_handler(menu_cd.filter())
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
    executor.start_polling(dispatcher, skip_updates=True)
