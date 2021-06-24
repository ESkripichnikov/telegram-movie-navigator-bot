from callback_data import Start, Source, Level
from keyboard_builder import Keyboard


def create_starting_keyboard():
    """
    Generate the keyboard with trending, top rated and upcoming movies
    """
    keyboard = Keyboard()
    keyboard.add_popular_buttons(Start.start_menu.value)
    keyboard.add_top_rated_buttons(Start.start_menu.value)
    keyboard.add_upcoming_buttons(Start.start_menu.value)
    return keyboard.get_keyboard


def create_popular_keyboard():
    """
    Generate the keyboard with trending buttons
    """
    keyboard = Keyboard()
    keyboard.add_popular_buttons(Start.other.value)
    return keyboard.get_keyboard


def create_top_rated_keyboard():
    """
    Generate the keyboard with top rated buttons
    """
    keyboard = Keyboard()
    keyboard.add_top_rated_buttons(Start.other.value)
    return keyboard.get_keyboard


def create_upcoming_keyboard():
    """
    Generate the keyboard with upcoming movies
    """
    keyboard = Keyboard()
    keyboard.add_upcoming_buttons(Start.other.value)
    return keyboard.get_keyboard


def create_genre_keyboard(source, start):
    """
    Generate the keyboard with different genres
    """
    keyboard = Keyboard()
    keyboard.add_genres_buttons(start, source)

    if start == Start.start_menu.value:
        place_to_return = Level.start_menu.value
    else:
        place_to_return = Level.section_menu.value

    keyboard.add_back_button(
        place_to_return=place_to_return,
        start=start,
        source=source
    )
    return keyboard.get_keyboard


def create_movies_keyboard(source, **kwargs):
    """
    Generate the keyboard with all possible movies, that could be implied
    """
    keyboard = Keyboard()
    keyboard.add_movies_buttons(source, **kwargs)

    if source == Source.movie_request.value:
        return keyboard.get_keyboard
    elif kwargs["genre_id"] == '-1' and kwargs["start"] == Start.other.value:
        place_to_return = Level.section_menu.value
    elif kwargs["genre_id"] == '-1' and kwargs["start"] == Start.start_menu.value:
        place_to_return = Level.start_menu.value
    else:
        place_to_return = Level.genre_menu.value

    keyboard.add_back_button(
        place_to_return=place_to_return,
        source=source,
        **kwargs
    )
    return keyboard.get_keyboard


def create_movie_links_keyboard(movie_id, **kwargs):
    """
    Generate the keyboard with links to the movie on tmdb, imdb and its trailer
    """
    keyboard = Keyboard(row_width=2)
    keyboard.add_movie_links_buttons(movie_id)
    keyboard.add_back_button(place_to_return=Level.movies_list.value, **kwargs)
    return keyboard.get_keyboard
