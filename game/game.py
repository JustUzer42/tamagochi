"""Модуль с интерфейсом и реализацией класса игры."""

import copy
from abc import ABC, abstractmethod
from typing import Any

from .clicker import AbstractClicker
from .exceptions import (
    InvalidChoice,
    NoFoodAvailable,
    NoFoodInInventory,
    NoMedicineAvailable,
    NoMedicineInInventory,
    NotEnoughMoney,
    TamagochiIsGone,
)
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс для логики игры."""

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа"

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды."""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства."""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи."""
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
    """Реализация игры с управлением тамагочи, кликером и ресурсами."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ) -> None:
        """Инициализация игры.

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды в магазине
        :param all_medicine: все доступные варианты лекарств в магазине
        """
        self._tamagochi = tamagochi
        self._clicker = clicker
        self._shop_food: list[Food] = list(all_food)
        self._shop_medicine: list[Medicine] = list(all_medicine)
        self._inventory_food: list[Food] = []
        self._inventory_medicine: list[Medicine] = []
        self._coins: int = 100

    @property
    def tamagochi(self) -> AbstractTamagochi:
        """Экземпляр тамагочи.

        :return: экземпляр SimpleTamagochi
        """
        return self._tamagochi

    @property
    def coins(self) -> int:
        """Текущий баланс монет.

        :return: количество монет
        """
        return self._coins

    @property
    def food(self) -> list[Food]:
        """Сумка с купленной едой.

        :return: список купленных объектов еды
        """
        return self._inventory_food

    @property
    def medicine(self) -> list[Medicine]:
        """Сумка с купленными лекарствами.

        :return: список купленных объектов лекарств
        """
        return self._inventory_medicine

    def _ensure_alive(self) -> None:
        """Проверить, жив ли тамагочи.

        :raises TamagochiIsGone: если тамагочи мёртв
        """
        if not self._tamagochi.is_alive():
            raise TamagochiIsGone()

    def work(self) -> int:
        """Пойти на работу — использовать кликер для заработка монет.

        :return: количество заработанных монет
        :raises TamagochiIsGone: если тамагочи мёртв
        """
        self._ensure_alive()
        self._clicker.click()
        earned = self._clicker.last_earned
        self._coins += earned
        self._tamagochi.update()
        return earned

    def buy_food(self) -> None:
        """Купить еду в магазине.

        Показывает доступную еду и предлагает выбрать.
        При покупке списывает монеты и добавляет еду в инвентарь.
        """
        if not self._shop_food:
            raise NoFoodAvailable()

        print("\n--- Доступная еда ---")
        for i, food in enumerate(self._shop_food, 1):
            name = food.name
            sat = food.satiety
            pr = food.price
            print(f"{i}. {name} - насыщ.: {sat}, цена: {pr}")

        try:
            choice = int(input("Выберите еду для покупки (номер): ")) - 1
        except ValueError:
            raise InvalidChoice()

        if choice < 0 or choice >= len(self._shop_food):
            raise InvalidChoice()

        food = self._shop_food[choice]

        if self._coins < food.price:
            raise NotEnoughMoney(
                f"Недостаточно монет для покупки "
                f"{food.name} (нужно {food.price})"
            )

        self._coins -= food.price
        self._inventory_food.append(copy.deepcopy(food))
        print(f"Куплено: {food.name}!")

    def buy_medicine(self) -> None:
        """Купить лекарство в магазине.

        Показывает доступные лекарства и предлагает выбрать.
        При покупке списывает монеты и добавляет лекарство в инвентарь.
        """
        if not self._shop_medicine:
            raise NoMedicineAvailable()

        print("\n--- Доступные лекарства ---")
        for i, med in enumerate(self._shop_medicine, 1):
            name = med.name
            heal = med.heal_hp
            pr = med.price
            uses = med.number_of_uses
            print(f"{i}. {name} - лечит: {heal} HP, "
                  f"цена: {pr}, исп.: {uses}")

        try:
            choice = int(input("Выберите лекарство для покупки (номер): ")) - 1
        except ValueError:
            raise InvalidChoice()

        if choice < 0 or choice >= len(self._shop_medicine):
            raise InvalidChoice()

        med = self._shop_medicine[choice]

        if self._coins < med.price:
            raise NotEnoughMoney(
                f"Недостаточно монет для покупки "
                f"{med.name} (нужно {med.price})"
            )

        self._coins -= med.price
        self._inventory_medicine.append(copy.deepcopy(med))
        print(f"Куплено: {med.name}!")

    def feed_tamagochi(self) -> None:
        """Покормить тамагочи.

        Показывает еду в инвентаре и предлагает выбрать.
        При кормлении вызывает tamagochi.feed().

        :raises TamagochiIsGone: если тамагочи мёртв
        """
        self._ensure_alive()

        if not self._inventory_food:
            raise NoFoodInInventory()

        print("\n--- Ваша еда ---")
        for i, food in enumerate(self._inventory_food, 1):
            print(f"{i}. {food.name} - насыщение: {food.satiety}")

        try:
            choice = int(input("Выберите еду для кормления (номер): ")) - 1
        except ValueError:
            raise InvalidChoice()

        if choice < 0 or choice >= len(self._inventory_food):
            raise InvalidChoice()

        food = self._inventory_food.pop(choice)
        self._tamagochi.feed(food)
        self._tamagochi.update()
        print(f"Покормили: {food.name}!")

    def heal_tamagochi(self) -> None:
        """Вылечить тамагочи.

        Показывает лекарства в инвентаре и предлагает выбрать.
        При лечении вызывает tamagochi.heal().

        :raises TamagochiIsGone: если тамагочи мёртв
        """
        self._ensure_alive()

        if not self._inventory_medicine:
            raise NoMedicineInInventory()

        # Фильтруем пустые лекарства
        available = [m for m in self._inventory_medicine if not m.is_empty()]
        if not available:
            print("Нет лекарств с оставшимися использованиями!")
            return

        print("\n--- Ваши лекарства ---")
        for i, med in enumerate(self._inventory_medicine, 1):
            if med.is_empty():
                status = "закончилось"
            else:
                left = med.number_of_uses - med.uses
                status = f"осталось: {left}"
            print(f"{i}. {med.name} - лечит: {med.heal_hp} HP ({status})")

        try:
            choice = int(input("Выберите лекарство для лечения (номер): ")) - 1
        except ValueError:
            raise InvalidChoice()

        if choice < 0 or choice >= len(self._inventory_medicine):
            raise InvalidChoice()

        med = self._inventory_medicine[choice]
        if med.is_empty():
            print("Это лекарство закончилось!")
            return

        self._tamagochi.heal(med)
        self._tamagochi.update()
        print(f"Вылечили: {med.name}!")

    def rest_tamagochi(self) -> None:
        """Отдохнуть с тамагочи.

        Вызывает tamagochi.rest() для восстановления энергии.

        :raises TamagochiIsGone: если тамагочи мёртв
        """
        self._ensure_alive()
        self._tamagochi.rest()
        self._tamagochi.update()

    def play_with_tamagochi(self) -> None:
        """Поиграть с тамагочи.

        Вызывает tamagochi.play().

        :raises TamagochiIsGone: если тамагочи мёртв
        """
        self._ensure_alive()
        self._tamagochi.play()
        self._tamagochi.update()

    def get_status(self) -> dict[str, Any]:
        """Получить полный статус игры.

        :return: словарь с ключами 'hunger', 'hp', 'energy', 'coins'
        """
        status = self._tamagochi.status
        status["coins"] = self._coins
        return status
