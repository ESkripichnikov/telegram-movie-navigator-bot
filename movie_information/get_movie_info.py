import requests
from constants import movies_to_display, trailer_links
from exceptions import NoMoviesError
from movie_information.movie_description_builder import Description


def pages(section, tmdb_token):
    """
    Generator of pages with movies
    """
    link = f'https://api.themoviedb.org/3/movie/{section}?api_key={tmdb_token}&language=ru-RU' + '&page={page}'
    for i in range(1, 101):
        yield requests.get(link.format(page=str(i))).json()["results"]


def get_possible_movies(movie_name, tmdb_token):
    """
    Returns the list of all possible movies, that could be implied
    """
    r = requests.get(
        f'https://api.themoviedb.org/3/search/movie?api_key={tmdb_token}&language=ru-RU&query={movie_name}&page=1'
        f'&include_adult=false'
    )
    data = r.json()
    if not data["results"]:
        raise NoMoviesError
    results = {}
    for movie in data["results"]:
        if len(results) < movies_to_display:
            results[movie["id"]] = movie["title"]
    return results


def get_movie(movie_id, tmdb_token):
    """
    Returns information about the selected movie
    """
    r = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_token}&language=ru-RU&append_to_response=credits'
    )
    data = r.json()

    movie_description = Description(data)
    movie_description.add_title()
    movie_description.add_vote_average()
    movie_description.add_release_date()
    movie_description.add_runtime()
    movie_description.add_genres()
    movie_description.add_production_countries()
    movie_description.add_directors()
    movie_description.add_actors()
    movie_description.add_overview()

    return movie_description.get_description


def get_imdb_id(movie_id, tmdb_token):
    r = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_token}')
    data = r.json()
    return data["imdb_id"]


def get_trailer(movie_id, tmdb_token):
    """
    Returns the trailer link
    """
    r = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={tmdb_token}&language=ru-RU')
    data = r.json()
    if data["results"]:
        if data["results"][0]["site"] == "YouTube":
            return trailer_links["Youtube"].format(data["results"][0]["key"])
        elif data["results"][0]["site"] == "Vimeo":
            return trailer_links["Vimeo"].format(data["results"][0]["key"])
    return None


def get_movies_section(section, tmdb_token):
    """
    Returns the list of movies depending on section (popular, top_rated or upcoming)
    """
    r = requests.get(f'https://api.themoviedb.org/3/movie/{section}/?api_key={tmdb_token}&language=ru-RU')
    data = r.json()
    if not data["results"]:
        raise NoMoviesError
    results = {}
    for movie in data["results"]:
        if len(results) < 10:
            results[movie["id"]] = movie["title"]
    return results


def get_movies_genre(genre_id, section, tmdb_token):
    """
    Returns the list of movies by genre depending on section (popular, top_rated or upcoming)
    """
    results = {}
    for page in pages(section, tmdb_token):
        if not page and not results:
            raise NoMoviesError
        elif len(results) >= movies_to_display or (not page and results):
            return results

        for movie in page:
            if int(genre_id) in movie["genre_ids"]:
                results[movie["id"]] = movie["title"]
    return results
