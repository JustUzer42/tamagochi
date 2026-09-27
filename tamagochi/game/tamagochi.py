"""Модуль с интерфейсом и реализациями класса тамагочи"""

from abc import ABC, abstractmethod

from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи"""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи"""
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
    """Реализация тамагочи с полной логикой состояний"""

    def __init__(self) -> None:
        self._hp: int = 100
        self._hunger: int = 0
        self._energy: int = 100
        self._coins: int = 0
        self._is_sick: bool = False

    def feed(self, food: Food) -> None:
        self._hunger = max(0, self._hunger - food.satiety)
        self._energy = max(0, self._energy - 2)

    def play(self) -> None:
        self._hunger = min(100, self._hunger + 5)
        self._hp = min(100, self._hp + 2)
        self._energy = max(0, self._energy - 15)

    def rest(self) -> None:
        if self._is_sick:
            self._energy = min(100, self._energy + 10)
        else:
            self._energy = min(100, self._energy + 20)
        self._hunger = min(100, self._hunger + 3)

    def heal(self, medicine: Medicine) -> None:
        if medicine.is_empty():
            raise ValueError("Лекарство закончилось")
        self._hp = min(100, self._hp + medicine.heal_hp)
        self._is_sick = False
        medicine.uses += 1

    @property
    def status(self) -> dict[str, int]:
        return {
            'hunger': self._hunger,
            'hp': self._hp,
            'energy': self._energy,
            'coins': self._coins,
        }

    def is_alive(self) -> bool:
        return self._hp > 0

    def is_sick(self) -> bool:
        return self._is_sick

    def update(self) -> None:
        self._hunger = min(100, self._hunger + 5)
        self._energy = max(0, self._energy - 3)

        if self._is_sick:
            self._hp -= 5

        if self._hunger >= 50:
            self._hp -= 5

        self._hp = max(0, self._hp)

    def add_coins(self, amount: int) -> None:
        self._coins += amount
