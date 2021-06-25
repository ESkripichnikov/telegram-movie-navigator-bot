from abc import ABCMeta, abstractmethod
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from callback_data import make_callback_data, Source, Level
from constants import all_genres, movie_links
from get_movie_info import get_possible_movies, get_movies_section, get_movies_genre, get_imdb_id, get_trailer
from config import tmdb_token


class IKeyboard(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_keyboard() -> None:
        pass

    @staticmethod
    @abstractmethod
    def add_popular_buttons(start) -> None:
        pass

    @staticmethod
    @abstractmethod
    def add_top_rated_buttons(start) -> None:
        pass

    @staticmethod
    @abstractmethod
    def add_upcoming_buttons(start) -> None:
        pass

    @staticmethod
    @abstractmethod
    def add_genres_buttons(start, source) -> None:
        pass

    @staticmethod
    @abstractmethod
    def add_movies_buttons(source, **kwargs) -> None:
        pass

    @staticmethod
    @abstractmethod
    def add_movie_links_buttons(movie_id) -> None:
        pass

    @staticmethod
    @abstractmethod
    def add_back_button(start, place_to_return) -> None:
        pass


class Keyboard(IKeyboard):
    def __init__(self, row_width=1) -> None:
        self._keyboard = InlineKeyboardMarkup(row_width=row_width)

    @property
    def get_keyboard(self) -> InlineKeyboardMarkup:
        return self._keyboard

    def add_popular_buttons(self, start):
        btn_popular = InlineKeyboardButton(
            text="Самые популярные фильмы",
            callback_data=make_callback_data(
                level=Level.movies_list.value,
                source=Source.popular.value,
                start=start
            )
        )
        btn_popular_genre = InlineKeyboardButton(
            text="Самые популярные фильмы по жанрам",
            callback_data=make_callback_data(
                level=Level.genre_menu.value,
                source=Source.popular.value,
                start=start
            )
        )
        self._keyboard.add(btn_popular, btn_popular_genre)
        return self

    def add_top_rated_buttons(self, start):
        btn_top_rated = InlineKeyboardButton(
            text="Самые рейтинговые фильмы",
            callback_data=make_callback_data(
                level=Level.movies_list.value,
                source=Source.top_rated.value,
                start=start
            )
        )
        btn_top_rated_genre = InlineKeyboardButton(
            text="Самые рейтинговые фильмы по жанрам",
            callback_data=make_callback_data(
                level=Level.genre_menu.value,
                source=Source.popular.value,
                start=start
            )
        )
        self._keyboard.add(btn_top_rated, btn_top_rated_genre)
        return self

    def add_upcoming_buttons(self, start):
        btn_upcoming = InlineKeyboardButton(
            text="Премьеры",
            callback_data=make_callback_data(
                level=Level.movies_list.value,
                source=Source.upcoming.value,
                start=start
            )
        )
        btn_upcoming_genre = InlineKeyboardButton(
            text="Премьеры по жанрам",
            callback_data=make_callback_data(
                level=Level.genre_menu.value,
                source=Source.upcoming.value,
                start=start
            )
        )
        self._keyboard.add(btn_upcoming, btn_upcoming_genre)
        return self

    def add_genres_buttons(self, start, source):
        for genre in all_genres:
            callback_data = make_callback_data(
                level=Level.movies_list.value,
                source=source,
                genre_id=genre["id"],
                start=start
            )
            btn = InlineKeyboardButton(text=genre["name"].title(), callback_data=callback_data)
            self._keyboard.add(btn)
        return self

    def add_movies_buttons(self, source, **kwargs):
        movies_list = get_movies_list(source, kwargs["genre_id"], kwargs["movie_name"])
        for movie_id, movie_name in movies_list.items():
            kwargs["movie_id"] = movie_id
            kwargs["level"] = Level.movie_info.value
            btn = InlineKeyboardButton(
                text=movie_name,
                callback_data=make_callback_data(
                    source=source,
                    **kwargs
                )
            )
            self._keyboard.add(btn)
        return self

    def add_movie_links_buttons(self, movie_id):
        imdb_id = get_imdb_id(movie_id, tmdb_token)
        url_imdb = movie_links["IMDB"].format(imdb_id)
        url_tmdb = movie_links["TMDB"].format(movie_id)
        btn_imdb = InlineKeyboardButton(text="IMDb", url=url_imdb)
        btn_tmdb = InlineKeyboardButton(text="TMDb", url=url_tmdb)
        self._keyboard.add(btn_imdb, btn_tmdb)

        trailer_link = get_trailer(movie_id, tmdb_token)
        if trailer_link:
            btn_trailer = InlineKeyboardButton(text="Смотреть трейлер", url=trailer_link)
            self._keyboard.row(btn_trailer)
        return self

    def add_back_button(self, place_to_return, **kwargs):
        if place_to_return == Level.movies_list.value:
            text = "🔙 Вернуться к выбору фильма"
        elif place_to_return == Level.genre_menu.value:
            text = "🔙 Вернуться к выбору жанра"
        else:
            text = "🔙 Назад"

        kwargs["level"] = place_to_return
        btn_back = InlineKeyboardButton(
            text=text,
            callback_data=make_callback_data(**kwargs)
        )
        self._keyboard.add(btn_back)
        return self


def get_movies_list(source, genre_id, movie_name):
    if source == Source.movie_request.value:
        results = get_possible_movies(movie_name, tmdb_token)
    elif source == Source.popular.value and genre_id != '-1':
        results = get_movies_genre(genre_id, 'popular', tmdb_token)
    elif source == Source.popular.value and genre_id == '-1':
        results = get_movies_section('popular', tmdb_token)
    elif source == Source.top_rated.value and genre_id != '-1':
        results = get_movies_genre(genre_id, 'top_rated', tmdb_token)
    elif source == Source.top_rated.value and genre_id == '-1':
        results = get_movies_section('top_rated', tmdb_token)
    elif source == Source.upcoming.value and genre_id != '-1':
        results = get_movies_genre(genre_id, 'upcoming', tmdb_token)
    else:
        results = get_movies_section('upcoming', tmdb_token)
    return results
