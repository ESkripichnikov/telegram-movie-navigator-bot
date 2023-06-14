# Telegram MovieNavigatorBot #

## Bot Description ##

MovieNavigatorBot can provide a lot of useful information about any movie and help with finding the most popular, top-rated, and newest movies of any genre.

In other words, this bot has the following functionality:
1. Upon user request, it provides basic information about a movie, including the movie title, rating, release date, duration, genre list, production country, director, main actors, and movie description. Additionally, it includes links to the movie's pages on IMDB and TMDB, as well as a trailer link.
2. With the help of an interactive menu triggered by the commands /start or /help, users can discover new movies. The search can be performed in the following categories:
- Popular movies and popular movies by various genres (also triggered by the command /popular)
- Top-rated movies and top-rated movies by various genres (also triggered by the command /popular)
- Upcoming releases and upcoming releases by various genres (also triggered by the command /upcoming)

The main feature of this bot is its interactive menu, allowing users to navigate back from any point (e.g., to choose another movie or genre) without unnecessary additional commands, significantly enhancing the user experience.

## Bot's Internal Structure ##

MovieNavigatorBot utilizes [The Movie Database API](https://developers.themoviedb.org/3/getting-started/introduction).

The bot is divided into the following modules:
- main.py - bot initialization and launch
- message_handlers.py - contains main handlers for user requests
- movie_information
  - get_movie_info.py - describes the interaction with The Movie Database API (request creation and processing)
  - movie_description_builder.py - contains a class that constructs the movie description text
- keyboards
  - keyboards.py - contains all the necessary keyboards
  - keyboard_builder.py - describes the class that constructs keyboards
- callbacks
  - callbacks.py - describes the entire navigation through the bot's menu
  - callback_data.py - contains callback data required for navigation through the bot's menu
- constants.py - contains all the main constants used by the bot, including all necessary text.
- exceptions.py - describes the necessary custom exceptions.
