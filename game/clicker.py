"""Модуль с интерфейсом и реализацией кликера."""

import random

from abc import ABC, abstractmethod


class AbstractClicker(ABC):
    """Интерфейс для кликера."""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации."""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет."""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик."""
        raise NotImplementedError


class SimpleRandomClicker(AbstractClicker):
    """Кликер, который зарабатывает случайное количество монет за клик."""

    def __init__(
        self,
        income_per_click: int,
        max_income_per_click: int
    ) -> None:
        """Инициализация кликера.

        :param income_per_click: минимальное количество монет за клик
        :param max_income_per_click: максимальное количество монет за клик
        """
        self._income_per_click = income_per_click
        self._max_income_per_click = max_income_per_click
        self._coins = 0

    def click(self) -> None:
        """Заработать случайное количество монет."""
        earned = random.randint(
            self._income_per_click, self._max_income_per_click
        )
        self._coins += earned

    @property
    def income_per_click(self) -> int:
        """Количество монет за клик (базовое значение).

        :return: базовое количество монет за клик
        """
        return self._income_per_click
