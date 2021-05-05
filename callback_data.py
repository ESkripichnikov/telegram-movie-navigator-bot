from aiogram.utils.callback_data import CallbackData

menu_cd = CallbackData("show_menu", "level", "source", "movie_name", "genre_id", "movie_id", "start")
# source = 1 if it called from movie request
#        = 2 if it called from trending
#        = 3 if it called from top_rated
#        = 4 if it called from upcoming
# start  = 1 if it called from start menu
#        = 0 if it called from somewhere else


def make_callback_data(level, source='0', movie_name='0', genre_id='0', movie_id='0', start='0'):
    return menu_cd.new(level=level,
                       source=source, movie_name=movie_name, genre_id=genre_id, movie_id=movie_id, start=start)