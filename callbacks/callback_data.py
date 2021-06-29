from enum import Enum
from aiogram.utils.callback_data import CallbackData
from constants import empty


class Source(Enum):
    movie_request = "movie_request"
    popular = "popular"
    top_rated = "top_rated"
    upcoming = "upcoming"


class Start(Enum):
    start_menu = "start_menu"
    other = "other"


class Level(Enum):
    start_menu = "display_start_menu"
    section_menu = "list_top"
    genre_menu = "list_genres"
    movies_list = "list_possible_movies"
    movie_info = "display_movie_info"


menu_cd = CallbackData("show_menu", "level", "source", "movie_name", "genre_id", "movie_id", "start")


def make_callback_data(level, source=empty, movie_name=empty,
                       genre_id=empty, movie_id=empty, start=Start.other.value):
    return menu_cd.new(
        level=level,
        source=source,
        movie_name=movie_name,
        genre_id=genre_id,
        movie_id=movie_id,
        start=start
    )
