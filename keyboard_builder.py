from abc import ABCMeta, abstractmethod
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from callback_data import make_callback_data, Source, Start


class IKeyboard(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_keyboard() -> None:
        pass

    @staticmethod
    @abstractmethod
    def add_popular_buttons() -> None:
        pass

    @staticmethod
    @abstractmethod
    def add_top_rated_buttons() -> None:
        pass

    @staticmethod
    @abstractmethod
    def add_upcoming_buttons() -> None:
        pass

    @staticmethod
    @abstractmethod
    def add_back_button() -> None:
        pass


class Keyboard(IKeyboard):
    def __init__(self, current_level, start) -> None:
        self._keyboard = InlineKeyboardMarkup(row_width=1)
        self._current_level = current_level
        self._start = start

    @property
    def get_keyboard(self) -> InlineKeyboardMarkup:
        return self._keyboard

    def add_popular_buttons(self):
        btn_trending = InlineKeyboardButton(
            text="Самые популярные фильмы",
            callback_data=make_callback_data(
                level=self._current_level + 3,
                source=Source.trending.value,
                start=self._start
            )
        )
        btn_trending_genre = InlineKeyboardButton(
            text="Самые популярные фильмы по жанрам",
            callback_data=make_callback_data(
                level=self._current_level + 2,
                source=Source.trending.value,
                start=self._start
            )
        )
        self._keyboard.add(btn_trending, btn_trending_genre)
        return self

    def add_top_rated_buttons(self):
        btn_top_rated = InlineKeyboardButton(
            text="Самые рейтинговые фильмы",
            callback_data=make_callback_data(
                level=self._current_level + 3,
                source=Source.top_rated.value,
                start=self._start
            )
        )
        btn_top_rated_genre = InlineKeyboardButton(
            text="Самые рейтинговые фильмы по жанрам",
            callback_data=make_callback_data(
                level=self._current_level + 2,
                source=Source.trending.value,
                start=self._start
            )
        )
        self._keyboard.add(btn_top_rated, btn_top_rated_genre)
        return self

    def add_upcoming_buttons(self):
        btn_upcoming = InlineKeyboardButton(
            text="Премьеры",
            callback_data=make_callback_data(
                level=self._current_level + 3,
                source=Source.upcoming.value,
                start=self._start
            )
        )
        btn_upcoming_genre = InlineKeyboardButton(
            text="Премьеры по жанрам",
            callback_data=make_callback_data(
                level=self._current_level + 2,
                source=Source.upcoming.value,
                start=self._start
            )
        )
        self._keyboard.add(btn_upcoming, btn_upcoming_genre)
        return self

    def add_back_button(self):
        btn_back = InlineKeyboardButton(
            text="🔙 Назад",
            callback_data=make_callback_data(level=self._current_level)
        )
        self._keyboard.add(btn_back)
        return self
