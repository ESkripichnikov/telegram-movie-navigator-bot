from abc import ABCMeta, abstractmethod
from constants import months, directors_number, actors_number


class IDescription(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_description(data) -> None:
        pass

    @staticmethod
    @abstractmethod
    def add_title() -> None:
        pass

    @staticmethod
    @abstractmethod
    def add_vote_average() -> None:
        pass

    @staticmethod
    @abstractmethod
    def add_release_date() -> None:
        pass

    @staticmethod
    @abstractmethod
    def add_runtime() -> None:
        pass

    @staticmethod
    @abstractmethod
    def add_genres() -> None:
        pass

    @staticmethod
    @abstractmethod
    def add_production_countries() -> None:
        pass

    @staticmethod
    @abstractmethod
    def add_directors() -> None:
        pass

    @staticmethod
    @abstractmethod
    def add_actors() -> None:
        pass

    @staticmethod
    @abstractmethod
    def add_overview() -> None:
        pass


class Description(IDescription):
    def __init__(self, data) -> None:
        self._description = str()
        self._data = data

    @property
    def get_description(self) -> str:
        return self._description

    def add_title(self):
        self._description += f"*{self._data['title']}*\n{self._data['original_title']}\n\n"
        return self

    def add_vote_average(self):
        self._description += f"⭐ {self._data['vote_average']}"
        return self

    def add_release_date(self):
        release_date = get_release_date(self._data)
        self._description += f"📅 {release_date} "
        return self

    def add_runtime(self):
        runtime = get_runtime(self._data)
        self._description += f"🕑 {runtime}\n"
        return self

    def add_genres(self):
        genres = get_genres(self._data)
        self._description += f"🎞️ {genres}\n"
        return self

    def add_production_countries(self):
        production_countries = get_countries(self._data)
        self._description += f"🌍 {production_countries}\n\n"
        return self

    def add_directors(self):
        directors = get_directors(self._data)
        self._description += f"🎥 Режиссер: {directors}\n"
        return self

    def add_actors(self):
        actors = get_actors(self._data)
        self._description += f"🎭 В главных ролях: {actors}\n\n"
        return self

    def add_overview(self):
        self._description += f"{self._data['overview']}"
        return self


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


def get_directors(data):
    directors = list()
    for man in data["credits"]["crew"]:
        if len(directors) < directors_number and man["job"] == "Director":
            directors.append(man["name"])
    return ', '.join(directors)


def get_actors(data):
    actors = list()
    for man in data["credits"]["cast"]:
        if len(actors) < actors_number and man["known_for_department"] == "Acting":
            actors.append(man["name"])
    return ', '.join(actors)
