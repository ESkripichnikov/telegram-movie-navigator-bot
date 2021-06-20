from enum import Enum
from aiogram.utils.callback_data import CallbackData


class Source(Enum):
    movie_request = "movie_request"
    trending = "trending"
    top_rated = "top_rated"
    upcoming = "upcoming"


class Start(Enum):
    start_menu = "start_menu"
    other = "start_menu"


menu_cd = CallbackData("show_menu", "level", "source", "movie_name", "genre_id", "movie_id", "start")


def make_callback_data(level, source='0', movie_name='0', genre_id='0', movie_id='0', start=Start.other.value):
    return menu_cd.new(
        level=level,
        source=source,
        movie_name=movie_name,
        genre_id=genre_id,
        movie_id=movie_id,
        start=start
    )
