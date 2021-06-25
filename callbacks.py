from aiogram import types, Dispatcher
import keyboards
from callback_data import menu_cd, Source, Level
from config import tmdb_token
from get_movie_info import get_movie
from exceptions import NoMoviesError


async def display_start_menu(call: types.CallbackQuery, **kwargs):
    try:
        markup = keyboards.create_starting_keyboard()
        await call.message.edit_text("Выберете подходящий вариант")
        await call.message.edit_reply_markup(markup)
    except NoMoviesError:
        await call.answer("Что-то пошло не так, попробуйте позже")


async def list_top(call: types.CallbackQuery, source, **kwargs):
    if source == Source.popular.value:
        markup = keyboards.create_popular_keyboard()
    elif source == Source.top_rated.value:
        markup = keyboards.create_top_rated_keyboard()
    else:
        markup = keyboards.create_upcoming_keyboard()

    try:
        await call.message.edit_text("Выберете интересующий вас фильм")
        await call.message.edit_reply_markup(markup)
    except NoMoviesError:
        await call.answer("Что-то пошло не так, попробуйте позже")


async def list_genres(call: types.CallbackQuery, source, start, **kwargs):
    try:
        markup = keyboards.create_genre_keyboard(source, start)
        await call.message.edit_text("Выберете интересующий вас жанр")
        await call.message.edit_reply_markup(markup)
    except NoMoviesError:
        await call.answer("Что-то пошло не так, попробуйте позже")


async def list_possible_movies(call: types.CallbackQuery, source, **kwargs):
    try:
        markup = keyboards.create_movies_keyboard(source=source, **kwargs)
        await call.message.edit_text("Выберете интересующий вас фильм")
        await call.message.edit_reply_markup(markup)
    except NoMoviesError:
        await call.answer("Что-то пошло не так, попробуйте позже")


async def display_movie_info(call: types.CallbackQuery, movie_id, **kwargs):
    try:
        movie_info = get_movie(movie_id, tmdb_token)
        markup = keyboards.create_movie_links_keyboard(movie_id, **kwargs)
        await call.message.edit_text(movie_info, parse_mode='Markdown')
        await call.message.edit_reply_markup(markup)
    except NoMoviesError:
        await call.answer("Что-то пошло не так, попробуйте позже")


async def navigate(call: types.CallbackQuery, callback_data: dict):
    levels = {
        Level.start_menu.value: display_start_menu,
        Level.section_menu.value: list_top,
        Level.genre_menu.value: list_genres,
        Level.movies_list.value: list_possible_movies,
        Level.movie_info.value: display_movie_info
    }

    current_level_function = levels[callback_data["level"]]
    callback_data.pop('@')
    await current_level_function(
        call,
        **callback_data
    )


def register_callbacks(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(navigate, menu_cd.filter())
