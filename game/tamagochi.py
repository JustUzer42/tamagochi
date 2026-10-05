"""Модуль с интерфейсом и реализациями класса тамагочи."""

from abc import ABC, abstractmethod

import random

from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи."""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли тамагочи

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи

        :return: True если тамагочи болеет, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи.
        Должен использоваться после каждого взаимодействия с тамагочи
        """
        raise NotImplementedError


class SimpleTamagochi(AbstractTamagochi):
    """Реализация тамагочи с базовой логикой состояния."""

    def __init__(self, name: str = "Тамагочи") -> None:
        """Инициализация тамагочи.

        :param name: имя питомца
        """
        self._name = name
        self._hunger: int = 50  # 0 - не голоден, 100 - сильно голоден
        self._hp: int = 100  # здоровье
        self._energy: int = 100  # энергия
        self._is_sick: bool = False
        self._coins: int = 100  # стартовый баланс монет

    @property
    def coins(self) -> int:
        """Текущий баланс монет.

        :return: количество монет
        """
        return self._coins

    @coins.setter
    def coins(self, value: int) -> None:
        """Установить баланс монет.

        :param value: новое количество монет
        """
        self._coins = value

    def feed(self, food: Food) -> None:
        """Кормить тамагочи.

        Уменьшает голод на величину насыщения еды.
        Уменьшает энергию.

        :param food: объект еды для кормления
        """
        self._hunger = max(0, self._hunger - food.satiety)
        self._energy = max(0, self._energy - 5)

    def play(self) -> None:
        """Поиграть с тамагочи.

        Увеличивает голод и уменьшает энергию.
        """
        self._hunger = min(100, self._hunger + 10)
        self._energy = max(0, self._energy - 15)

    def rest(self) -> None:
        """Отдохнуть.

        Восстанавливает энергию. Если болен — восстановление менее эффективно.
        """
        if self._is_sick:
            self._energy = min(100, self._energy + 20)
        else:
            self._energy = min(100, self._energy + 40)
        self._hunger = min(100, self._hunger + 5)

    def heal(self, medicine: Medicine) -> None:
        """Вылечить тамагочи.

        Восстанавливает здоровье, снимает болезнь.
        Увеличивает счётчик использований лекарства.

        :param medicine: лекарство для лечения
        """
        if medicine.is_empty():
            raise ValueError("Лекарство закончилось")
        self._hp = min(100, self._hp + medicine.heal_hp)
        self._is_sick = False
        medicine.uses += 1

    @property
    def status(self) -> dict[str, int]:
        """Текущее состояние тамагочи.

        :return: словарь с ключами 'hunger', 'hp', 'energy'
        """
        return {
            "hunger": self._hunger,
            "hp": self._hp,
            "energy": self._energy,
        }

    def is_alive(self) -> bool:
        """Проверка, жив ли тамагочи.

        :return: True если здоровье > 0
        """
        return self._hp > 0

    def is_sick(self) -> bool:
        """Проверка, болен ли тамагочи.

        :return: True если болен
        """
        return self._is_sick

    def update(self) -> None:
        """Обновление состояния тамагочи.

        Увеличивает голод, уменьшает здоровье при сильном голоде,
        случайный шанс заболеть, уменьшает энергию.
        """
        # Голод увеличивается со временем
        self._hunger = min(100, self._hunger + 5)

        # При сильном голоде здоровье уменьшается
        if self._hunger >= 90:
            self._hp -= 10

        # Случайный шанс заболеть (10%)
        if not self._is_sick and random.random() < 0.1:
            self._is_sick = True
            self._hp -= 5
            self._energy -= 10

        # Если болен — здоровье уменьшается
        if self._is_sick:
            self._hp -= 3

        # Энергия уменьшается со временем
        self._energy = max(0, self._energy - 3)
