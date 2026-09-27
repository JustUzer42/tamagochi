"""Модуль с интерфейсом и реализацией кликера"""

from abc import ABC, abstractmethod

import random


class AbstractClicker(ABC):
    """Интерфейс для кликера"""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации"""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет"""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик"""
        raise NotImplementedError


class SimpleRandomClicker(AbstractClicker):
    """Реализация кликера со случайным доходом"""

    def __init__(self, min_income: int, max_income: int) -> None:
        self._min_income = min_income
        self._max_income = max_income

    @property
    def income_per_click(self) -> int:
        return random.randint(self._min_income, self._max_income)

    def click(self) -> None:
        pass
