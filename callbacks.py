from aiogram import types, Dispatcher
import keyboards
from callback_data import menu_cd
from config import tmdb_token
from get_movie_info import convert_movie_info


async def display_start_menu(call: types.CallbackQuery, **kwargs):
    try:
        markup = keyboards.start_keyboard()
        await call.message.edit_text("Выберете подходящий вариант")
        await call.message.edit_reply_markup(markup)
    except Exception:
        await call.answer("Что-то пошло не так, попробуйте позже")


async def list_top(call: types.CallbackQuery, source, start, **kwargs):
    if source == '2':
        try:
            markup = keyboards.trending_keyboard(start)
            await call.message.edit_text("Выберете интересующий вас фильм")
            await call.message.edit_reply_markup(markup)
        except Exception:
            await call.answer("Что-то пошло не так, попробуйте позже")
    elif source == '3':
        try:
            markup = keyboards.top_rated_keyboard(start)
            await call.message.edit_text("Выберете интересующий вас фильм")
            await call.message.edit_reply_markup(markup)
        except Exception:
            await call.answer("Что-то пошло не так, попробуйте позже")
    elif source == '4':
        try:
            markup = keyboards.upcoming_keyboard(start)
            await call.message.edit_text("Выберете интересующий вас фильм")
            await call.message.edit_reply_markup(markup)
        except Exception:
            await call.answer("Что-то пошло не так, попробуйте позже")


async def list_genres(call: types.CallbackQuery, source, start, **kwargs):
    try:
        markup = keyboards.genre_keyboard(source, start)
        await call.message.edit_text("Выберете интересующий вас жанр")
        await call.message.edit_reply_markup(markup)
    except Exception:
        await call.answer("Что-то пошло не так, попробуйте позже")


async def list_possible_movies(call: types.CallbackQuery, source, **kwargs):
    try:
        markup = keyboards.movie_keyboard(source=source, **kwargs)
        await call.message.edit_text("Выберете интересующий вас фильм")
        await call.message.edit_reply_markup(markup)
    except Exception:
        await call.answer("Что-то пошло не так, попробуйте позже")


async def display_movie_info(call: types.CallbackQuery, movie_id, **kwargs):
    try:
        movie_info = convert_movie_info(movie_id, tmdb_token)
        markup = keyboards.movie_links_keyboard(movie_id, **kwargs)
        await call.message.edit_text(movie_info, parse_mode='Markdown')
        await call.message.edit_reply_markup(markup)
    except Exception:
        await call.answer("Что-то пошло не так, попробуйте позже")


async def navigate(call: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level")
    source = callback_data.get("source")
    movie_name = callback_data.get("movie_name")
    genre_id = callback_data.get("genre_id")
    movie_id = callback_data.get("movie_id")
    start = callback_data.get("start")

    levels = {
        "0": display_start_menu,
        "1": list_top,
        "2": list_genres,
        "3": list_possible_movies,
        "4": display_movie_info
    }

    current_level_function = levels[current_level]

    await current_level_function(
        call,
        source=source,
        movie_name=movie_name,
        genre_id=genre_id,
        movie_id=movie_id,
        start=start
    )


def register_callbacks(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(navigate, menu_cd.filter())
