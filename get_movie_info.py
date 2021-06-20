import requests

actors_number = 5  # how many actors to display
directors_number = 2  # how many directors to display
months = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня",
          "Июля", "Августа", "Сентября", "Октября", "Ноября", "Декабря"]
movies_to_display = 10  # how many movies to display
links = {
    "Youtube": 'https://www.youtube.com/watch?v={}',
    "Vimeo": 'https://vimeo.com/{}'
}


def get_genres(data):
    genres = list()
    for genre in data["genres"]:
        genres.append(genre['name'])
    return ', '.join(genres).title()


def get_countries(data):
    countries = list()
    for country in data["production_countries"]:
        countries.append(country['name'])
    return ', '.join(countries)


def get_actors(data):
    actors = list()
    for man in data["credits"]["cast"]:
        if len(actors) < actors_number and man["known_for_department"] == "Acting":
            actors.append(man["name"])
    return ', '.join(actors)


def get_directors(data):
    directors = list()
    for man in data["credits"]["crew"]:
        if len(directors) < directors_number and man["job"] == "Director":
            directors.append(man["name"])
    return ', '.join(directors)


def get_release_date(data):
    tmp = data['release_date'].split('-')
    release_date = str(int(tmp[2])) + ' ' + months[int(tmp[1]) - 1] + ' ' + tmp[0]
    return release_date


def get_runtime(data):
    tmp = data['runtime']
    if tmp // 60 < 10:
        hours = "0" + str(tmp // 60)
    else:
        hours = str(tmp // 60)
    if tmp % 60 < 10:
        minutes = "0" + str(tmp % 60)
    else:
        minutes = str(tmp % 60)
    runtime = str(tmp) + " мин. / " + hours + ':' + minutes
    return runtime


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
        raise Exception
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

    title = data["title"]
    original_title = data["original_title"]
    release_date = get_release_date(data)
    runtime = get_runtime(data)
    vote_average = data["vote_average"]
    overview = data["overview"]
    genres = get_genres(data)
    production_countries = get_countries(data)
    actors = get_actors(data)
    directors = get_directors(data)

    return f"*{title}*\n{original_title}\n\n" \
           f"⭐ {vote_average} 📅 {release_date} 🕑 {runtime}\n" \
           f"🎞️ {genres}\n" \
           f"🌍 {production_countries}\n\n" \
           f"🎥 Режиссер: {directors}\n" \
           f"🎭 В главных ролях: {actors}\n\n" \
           f"{overview}"


def get_backdrop_path(movie_id, tmdb_token):
    """
    Returns the backdrop path
    """
    r = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_token}'
    )
    data = r.json()
    if data["backdrop_path"]:
        return f'https://image.tmdb.org/t/p/original/{data["backdrop_path"]}'
    return None


def get_imdb_id(movie_id, tmdb_token):
    r = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_token}&language=ru-RU&append_to_response=credits'
    )
    data = r.json()
    return data["imdb_id"]


def get_trailer(movie_id, tmdb_token):
    """
    Returns the trailer link
    """
    r = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={tmdb_token}&language=ru-RU'
    )
    data = r.json()
    if data["results"]:
        if data["results"][0]["site"] == "YouTube":
            return links["Youtube"].format(data["results"][0]["key"])
        elif data["results"][0]["site"] == "Vimeo":
            return links["Vimeo"].format(data["results"][0]["key"])
    return None


def get_popular(tmdb_token):
    """
    Returns the list of popular movies
    """
    r = requests.get(f'https://api.themoviedb.org/3/movie/popular/?api_key={tmdb_token}&language=ru-RU')
    data = r.json()
    if not data["results"]:
        raise Exception
    results = {}
    for movie in data["results"]:
        if len(results) < 10:
            results[movie["id"]] = movie["title"]
    return results


def get_top_rated(tmdb_token):
    """
    Returns the list of top rated movies
    """
    r = requests.get(f'https://api.themoviedb.org/3/movie/top_rated?api_key={tmdb_token}&language=ru-RU')
    data = r.json()
    if not data["results"]:
        raise Exception
    results = {}
    for movie in data["results"]:
        if len(results) < 10:
            results[movie["id"]] = movie["title"]
    return results


def get_upcoming(tmdb_token):
    """
    Returns the list of upcoming movies
    """
    r = requests.get(
        f'https://api.themoviedb.org/3/movie/upcoming?api_key={tmdb_token}&language=ru-RU&page=1&region=RU'
    )
    data = r.json()
    if not data["results"]:
        raise Exception
    results = {}
    for movie in data["results"]:
        if len(results) < 10:
            results[movie["id"]] = movie["title"]
    return results


def get_movies_genre(genre_id, section, tmdb_token):
    results = {}
    for page in pages(section, tmdb_token):
        if not page and not results:
            raise Exception  # расписать exception
        elif len(results) >= movies_to_display or (not page and results):
            return results

        for movie in page:
            if int(genre_id) in movie["genre_ids"]:
                results[movie["id"]] = movie["title"]
    return results
