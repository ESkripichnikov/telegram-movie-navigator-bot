import requests
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from callback_data import make_callback_data, Source, Start
from config import tmdb_token
from get_movie_info import get_possible_movies, get_movies_section, \
    get_movies_genre, get_imdb_id, get_trailer


def create_starting_keyboard():
    """
    Generate the keyboard with trending, top rated and upcoming movies
    """
    current_level = 0
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_trending = InlineKeyboardButton(
        text="Самые популярные фильмы",
        callback_data=make_callback_data(
            level=current_level + 3,
            source=Source.trending.value,
            start=Start.start_menu.value
        )
    )
    btn_trending_genre = InlineKeyboardButton(
        text="Самые популярные фильмы по жанрам",
        callback_data=make_callback_data(
            level=current_level + 2,
            source=Source.trending.value,
            start=Start.start_menu.value
        )
    )
    btn_top_rated = InlineKeyboardButton(
        text="Самые рейтинговые фильмы",
        callback_data=make_callback_data(
            level=current_level + 3,
            source=Source.top_rated.value,
            start=Start.start_menu.value
        )
    )
    btn_top_rated_genre = InlineKeyboardButton(
        text="Самые рейтинговые фильмы по жанрам",
        callback_data=make_callback_data(
            level=current_level + 2,
            source=Source.trending.value,
            start=Start.start_menu.value
        )
    )
    btn_upcoming = InlineKeyboardButton(
        text="Премьеры",
        callback_data=make_callback_data(
            level=current_level + 3,
            source=Source.upcoming.value,
            start=Start.start_menu.value
        )
    )
    btn_upcoming_genre = InlineKeyboardButton(
        text="Премьеры по жанрам",
        callback_data=make_callback_data(
            level=current_level + 2,
            source=Source.upcoming.value,
            start=Start.start_menu.value
        )
    )
    keyboard.add(btn_trending, btn_trending_genre, btn_top_rated, btn_top_rated_genre,
                 btn_upcoming, btn_upcoming_genre)
    return keyboard


def create_trending_keyboard(start):
    """
    Generate the keyboard with trending buttons
    """
    current_level = 1
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_trending = InlineKeyboardButton(
        text="Самые популярные фильмы",
        callback_data=make_callback_data(
            level=current_level + 2,
            source=Source.trending.value,
            start=start
        )
    )
    btn_trending_genre = InlineKeyboardButton(
        text="Самые популярные фильмы по жанрам",
        callback_data=make_callback_data(
            level=current_level + 1,
            source=Source.trending.value,
            start=start
        )
    )
    keyboard.add(btn_trending, btn_trending_genre)

    if start == "start_menu":
        btn_back = InlineKeyboardButton(
            text="🔙 Назад",
            callback_data=make_callback_data(level=current_level - 1)
        )
        keyboard.add(btn_back)
    return keyboard


def create_top_rated_keyboard(start):
    """
    Generate the keyboard with top rated buttons
    """
    current_level = 1
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_top_rated = InlineKeyboardButton(
        text="Самые рейтинговые фильмы",
        callback_data=make_callback_data(
            level=current_level + 2,
            source=Source.top_rated.value,
            start=start
        )
    )
    btn_top_rated_genre = InlineKeyboardButton(
        text="Самые рейтинговые фильмы по жанрам",
        callback_data=make_callback_data(
            level=current_level + 1,
            source=Source.top_rated.value,
            start=start
        )
    )
    keyboard.add(btn_top_rated, btn_top_rated_genre)

    if start == Start.start_menu.value:
        btn_back = InlineKeyboardButton(
            text="🔙 Назад",
            callback_data=make_callback_data(level=current_level - 1)
        )
        keyboard.add(btn_back)
    return keyboard


def create_upcoming_keyboard(start):
    """
    Generate the keyboard with upcoming movies
    """
    current_level = 1
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_upcoming = InlineKeyboardButton(
        text="Премьеры",
        callback_data=make_callback_data(
            level=current_level + 2,
            source=Source.upcoming.value,
            start=start
        )
    )
    btn_upcoming_genre = InlineKeyboardButton(
        text="Премьеры по жанрам",
        callback_data=make_callback_data(
            level=current_level + 1,
            source=Source.upcoming.value,
            start=start
        )
    )
    keyboard.add(btn_upcoming, btn_upcoming_genre)

    if start == Start.start_menu.value:
        btn_back = InlineKeyboardButton(
            text="🔙 Назад",
            callback_data=make_callback_data(level=current_level - 1)
        )
        keyboard.add(btn_back)
    return keyboard


def create_genre_keyboard(source, start):
    """
    Generate the keyboard with different genres
    """
    current_level = 2
    keyboard = InlineKeyboardMarkup(row_width=1)
    r = requests.get(f'https://api.themoviedb.org/3/genre/movie/list?api_key={tmdb_token}&language=ru-RU')
    all_genres = r.json()["genres"]
    for genre in all_genres:
        callback_data = make_callback_data(
            level=current_level + 1,
            source=source,
            genre_id=genre["id"],
            start=start
        )
        btn = InlineKeyboardButton(text=genre["name"].title(), callback_data=callback_data)
        keyboard.add(btn)

    if start == Start.start_menu.value:
        btn_back = InlineKeyboardButton(
            text="🔙 Назад",
            callback_data=make_callback_data(
                level=current_level - 2,
                source=source,
                start=start
            )
        )
    else:
        btn_back = InlineKeyboardButton(
            text="🔙 Назад",
            callback_data=make_callback_data(
                level=current_level - 1,
                source=source,
                start=start
            )
        )
    keyboard.add(btn_back)
    return keyboard


def create_movies_keyboard(source, **kwargs):
    """
    Generate the keyboard with all possible movies, that could be implied
    """
    current_level = 3
    if source == Source.movie_request.value:
        results = get_possible_movies(kwargs.get("movie_name"), tmdb_token)
    elif source == Source.trending.value:
        if kwargs.get("genre_id") == '0':
            results = get_movies_section('popular', tmdb_token)
        else:
            results = get_movies_genre(kwargs.get("genre_id"), 'popular', tmdb_token)
    elif source == Source.top_rated.value:
        if kwargs.get("genre_id") == '0':
            results = get_movies_section('top_rated', tmdb_token)
        else:
            results = get_movies_genre(kwargs.get("genre_id"), 'top_rated', tmdb_token)
    else:
        if kwargs.get("genre_id") == '0':
            results = get_movies_section('upcoming', tmdb_token)
        else:
            results = get_movies_genre(kwargs.get("genre_id"), 'upcoming', tmdb_token)

    keyboard = InlineKeyboardMarkup(row_width=1)
    for movie_id, movie in results.items():
        kwargs["movie_id"] = movie_id
        callback_data = make_callback_data(level=current_level + 1, source=source, **kwargs)
        btn = InlineKeyboardButton(movie, callback_data=callback_data)
        keyboard.add(btn)

    if kwargs.get("movie_name") != '0':
        # in this case should be no "back" button
        return keyboard

    if kwargs.get("genre_id") == '0':
        text = "🔙 Назад"
        if kwargs.get("start") == '0':
            callback_data = make_callback_data(level=current_level - 2,
                                               source=source,
                                               **kwargs)
        else:
            callback_data = make_callback_data(level=current_level - 3)
    else:
        text = "🔙 Вернуться к выбору жанра"
        callback_data = make_callback_data(level=current_level - 1,
                                           source=source,
                                           **kwargs)

    btn_back = InlineKeyboardButton(text=text, callback_data=callback_data)
    keyboard.row(btn_back)
    return keyboard


def create_movie_links_keyboard(movie_id, **kwargs):
    """
    Generate the keyboard with links to the movie on tmdb, imdb and its trailer
    """
    current_level = 4
    keyboard = InlineKeyboardMarkup(row_width=2)
    imdb_id = get_imdb_id(movie_id, tmdb_token)
    url_imdb = f'https://www.imdb.com/title/{imdb_id}'
    url_tmdb = f'https://www.themoviedb.org/movie/{movie_id}'
    btn_imdb = InlineKeyboardButton(text="IMDb", url=url_imdb)
    btn_tmdb = InlineKeyboardButton(text="TMDb", url=url_tmdb)
    keyboard.add(btn_imdb, btn_tmdb)

    trailer_link = get_trailer(movie_id, tmdb_token)
    if trailer_link:
        btn_trailer = InlineKeyboardButton(text="Смотреть трейлер", url=trailer_link)
        keyboard.row(btn_trailer)

    callback_data = make_callback_data(level=current_level - 1, **kwargs)
    btn_back = InlineKeyboardButton(text="🔙 Вернуться к выбору фильма", callback_data=callback_data)
    keyboard.add(btn_back)
    return keyboard
