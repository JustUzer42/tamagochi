"""Модуль с интерфейсом и реализацией класса игры"""

from abc import ABC, abstractmethod
from typing import Any

from .clicker import AbstractClicker
from .exceptions import NotEnoughMoney, TamagochiIsGone
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс для логики игры"""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """
        Абстрактный метод инициализации класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды"""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства"""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств
        """
        raise NotImplementedError


class SimpleGame(AbstractGame):
    """Реализация игры с полной логикой"""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ) -> None:
        self._tamagochi = tamagochi
        self._clicker = clicker
        self._all_food = list(all_food)
        self._all_medicine = list(all_medicine)
        self._food: list[Food] = []
        self._medicine: list[Medicine] = []

    def work(self) -> int:
        if not self._tamagochi.is_alive():
            raise TamagochiIsGone("Питомец умер, нельзя работать")
        income = self._clicker.income_per_click
        self._tamagochi.add_coins(income)
        return income

    def buy_food(self) -> None:
        if not self._tamagochi.is_alive():
            raise TamagochiIsGone("Питомец умер, нельзя покупать еду")
        print("\nДоступная еда:")
        for i, food in enumerate(self._all_food):
            print(f"  {i + 1}. {food}")
        try:
            choice = int(input("Выберите еду (номер): ")) - 1
            if 0 <= choice < len(self._all_food):
                food = self._all_food[choice]
                if self._tamagochi.status['coins'] >= food.price:
                    self._tamagochi.add_coins(-food.price)
                    self._food.append(food)
                    print(f"Куплено: {food.name}")
                else:
                    raise NotEnoughMoney(f"Недостаточно монет для покупки {food.name}")
            else:
                print("Неверный номер")
        except ValueError as e:
            if isinstance(e, (TamagochiIsGone, NotEnoughMoney)):
                print(e)
            else:
                print("Неверный ввод")

    def buy_medicine(self) -> None:
        if not self._tamagochi.is_alive():
            raise TamagochiIsGone("Питомец умер, нельзя покупать лекарства")
        print("\nДоступные лекарства:")
        for i, med in enumerate(self._all_medicine):
            print(f"  {i + 1}. {med}")
        try:
            choice = int(input("Выберите лекарство (номер): ")) - 1
            if 0 <= choice < len(self._all_medicine):
                med = self._all_medicine[choice]
                if self._tamagochi.status['coins'] >= med.price:
                    self._tamagochi.add_coins(-med.price)
                    self._medicine.append(med)
                    print(f"Куплено: {med.name}")
                else:
                    raise NotEnoughMoney(f"Недостаточно монет для покупки {med.name}")
            else:
                print("Неверный номер")
        except ValueError as e:
            if isinstance(e, (TamagochiIsGone, NotEnoughMoney)):
                print(e)
            else:
                print("Неверный ввод")

    def feed_tamagochi(self) -> None:
        if not self._tamagochi.is_alive():
            raise TamagochiIsGone("Питомец умер, нельзя кормить")
        if not self._food:
            print("У вас нет еды! Купите еду в магазине.")
            return
        print("\nВаша еда:")
        for i, food in enumerate(self._food):
            print(f"  {i + 1}. {food}")
        try:
            choice = int(input("Выберите еду (номер): ")) - 1
            if 0 <= choice < len(self._food):
                food = self._food.pop(choice)
                self._tamagochi.feed(food)
                print(f"Питомец съел: {food.name}")
            else:
                print("Неверный номер")
        except ValueError as e:
            if isinstance(e, TamagochiIsGone):
                print(e)
            else:
                print("Неверный ввод")

    def heal_tamagochi(self) -> None:
        if not self._tamagochi.is_alive():
            raise TamagochiIsGone("Питомец умер, нельзя лечить")
        available = [m for m in self._medicine if not m.is_empty()]
        if not available:
            print("У вас нет лекарств!")
            return
        print("\nВаши лекарства:")
        for i, med in enumerate(self._medicine):
            print(f"  {i + 1}. {med}")
        try:
            choice = int(input("Выберите лекарство (номер): ")) - 1
            if 0 <= choice < len(self._medicine):
                med = self._medicine[choice]
                if med.is_empty():
                    print("Лекарство закончилось!")
                    return
                self._tamagochi.heal(med)
                print(f"Питомец вылечился: {med.name}")
            else:
                print("Неверный номер")
        except ValueError as e:
            if isinstance(e, TamagochiIsGone):
                print(e)
            else:
                print("Неверный ввод")

    def rest_tamagochi(self) -> None:
        if not self._tamagochi.is_alive():
            raise TamagochiIsGone("Питомец умер, нельзя отдыхать")
        self._tamagochi.rest()

    def play_with_tamagochi(self) -> None:
        if not self._tamagochi.is_alive():
            raise TamagochiIsGone("Питомец умер, нельзя играть")
        self._tamagochi.play()

    def get_status(self) -> dict[str, Any]:
        return self._tamagochi.status

    @property
    def food(self) -> list[Food]:
        return self._food

    @property
    def medicine(self) -> list[Medicine]:
        return self._medicine

    @property
    def tamagochi(self) -> AbstractTamagochi:
        return self._tamagochi
