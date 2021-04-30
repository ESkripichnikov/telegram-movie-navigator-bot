import requests


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
        if len(results) < 10:
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

    movie_info = dict()
    movie_info["title"] = data["title"]
    movie_info["original_title"] = data["original_title"]
    movie_info["release_date"] = data["release_date"]
    movie_info["runtime"] = data["runtime"]
    movie_info["vote_average"] = data["vote_average"]
    movie_info["overview"] = data["overview"]
    movie_info["imdb_id"] = data["imdb_id"]

    movie_info["genres"] = []
    for genre in data["genres"]:
        movie_info["genres"].append(genre['name'])

    movie_info["production_countries"] = []
    for country in data["production_countries"]:
        movie_info["production_countries"].append(country['name'])

    movie_info["cast"] = []
    for man in data["credits"]["cast"]:
        if len(movie_info["cast"]) < 5 and man["known_for_department"] == "Acting":
            movie_info["cast"].append(man["name"])

    movie_info["director"] = []
    for man in data["credits"]["crew"]:
        if len(movie_info["director"]) < 2 and man["job"] == "Director":
            movie_info["director"].append(man["name"])
    return movie_info


def display_movie_info(movie_id, tmdb_token):
    """
    Converts movie information to readable form
    """
    movie_info = get_movie(movie_id, tmdb_token)
    title = movie_info['title']
    original_title = movie_info['original_title']
    vote_average = movie_info['vote_average']

    tmp = movie_info['release_date'].split('-')
    months = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября",
              "Октября", "Ноября", "Декабря"]
    release_date = str(int(tmp[2])) + ' ' + months[int(tmp[1]) - 1] + ' ' + tmp[0]

    tmp = movie_info['runtime']
    if tmp // 60 < 10:
        hours = "0" + str(tmp // 60)
    else:
        hours = str(tmp // 60)
    if tmp % 60 < 10:
        minutes = "0" + str(tmp % 60)
    else:
        minutes = str(tmp % 60)
    runtime = str(tmp) + " мин. / " + hours + ':' + minutes

    genres = ', '.join(movie_info['genres']).title()

    production_countries = ', '.join(movie_info['production_countries'])

    director = ', '.join(movie_info['director'])

    cast = ', '.join(movie_info['cast'])

    overview = movie_info['overview']

    return f"*{title}*\n{original_title}\n\n" \
           f"⭐ {vote_average} 📅 {release_date} 🕑 {runtime}\n" \
           f"🎞️ {genres}\n" \
           f"🌍 {production_countries}\n\n" \
           f"🎥 Режиссер: {director}\n" \
           f"🎭 В главных ролях: {cast}\n\n" \
           f"{overview}"


def backdrop_path(movie_id, tmdb_token):
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


def trailer(movie_id, tmdb_token):
    """
    Returns the trailer link
    """
    r = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={tmdb_token}&language=ru-RU'
    )
    data = r.json()
    if data["results"]:
        if data["results"][0]["site"] == "YouTube":
            return f'https://www.youtube.com/watch?v={data["results"][0]["key"]}'
        elif data["results"][0]["site"] == "Vimeo":
            return f'https://vimeo.com/{data["results"][0]["key"]}'
    return None


def get_trending(tmdb_token):
    """
    Returns the list of trending movies
    """
    r = requests.get(f'https://api.themoviedb.org/3/trending/movie/week?api_key={tmdb_token}&language=ru-RU')
    data = r.json()
    if not data["results"]:
        raise Exception
    results = {}
    for movie in data["results"]:
        if len(results) < 10:
            results[movie["id"]] = movie["title"]
    return results


def get_trending_genre(genre_id, tmdb_token):
    """
    Returns the list of trending movies by genre
    """
    results = {}
    page = 1
    while len(results) < 10 and page < 100:
        r = requests.get(
            f'https://api.themoviedb.org/3/trending/movie/week?api_key={tmdb_token}&language=ru-RU&page={page}'
        )
        data = r.json()
        if not data["results"] and not results:
            raise Exception
        elif not data["results"] and results:
            return results
        for movie in data["results"]:
            for genre in movie["genre_ids"]:
                if genre == int(genre_id):
                    results[movie["id"]] = movie["title"]
        page += 1
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
            break
    return results


def get_top_rated_genre(genre_id, tmdb_token):
    """
    Returns the list of top rated movies by genre
    """
    results = {}
    page = 1
    while len(results) < 10 and page < 100:
        r = requests.get(
            f'https://api.themoviedb.org/3/movie/top_rated?api_key={tmdb_token}&language=ru-RU&page={page}'
        )
        data = r.json()
        if not data["results"] and not results:
            raise Exception
        elif not data["results"] and results:
            return results
        for movie in data["results"]:
            for genre in movie["genre_ids"]:
                if genre == int(genre_id):
                    results[movie["id"]] = movie["title"]
                    break
        page += 1
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


def get_upcoming_genre(genre_id, tmdb_token):
    """
    Returns the list of upcoming movies by genre
    """
    results = {}
    page = 1
    while len(results) < 10 and page < 100:
        r = requests.get(
            f'https://api.themoviedb.org/3/movie/upcoming?api_key={tmdb_token}&language=ru-RU&page={page}&region=RU'
        )
        data = r.json()
        if not data["results"] and not results:
            raise Exception
        elif not data["results"] and results:
            return results
        for movie in data["results"]:
            for genre in movie["genre_ids"]:
                if genre == int(genre_id):
                    results[movie["id"]] = movie["title"]
                    break
        page += 1
    return results
