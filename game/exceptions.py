"""Модуль с исключениями"""


class TamagochiIsGone(Exception):
    """Ошибка при смерти тамагочи"""

    def __init__(self, message: str = "Тамагочи умер!"):
        self.message = message
        super().__init__(self.message)


class NotEnoughMoney(Exception):
    """Ошибка когда не хватает монет для покупки"""

    def __init__(self, message: str = "Недостаточно монет для покупки"):
        self.message = message
        super().__init__(self.message)


class InvalidChoice(Exception):
    """Ошибка неверного выбора"""

    def __init__(self, message: str = "Неверный выбор!"):
        self.message = message
        super().__init__(self.message)


class NoFoodAvailable(Exception):
    """Ошибка когда еда недоступна для покупки"""

    def __init__(self, message: str = "Еда недоступна для покупки."):
        self.message = message
        super().__init__(self.message)


class NoMedicineAvailable(Exception):
    """Ошибка когда лекарства недоступны для покупки"""

    def __init__(self, message: str = "Лекарства недоступны для покупки."):
        self.message = message
        super().__init__(self.message)


class NoFoodInInventory(Exception):
    """Ошибка когда нет еды в инвентаре"""

    def __init__(self, message: str = "В инвентаре нет еды! Купите еду в магазине."):
        self.message = message
        super().__init__(self.message)


class NoMedicineInInventory(Exception):
    """Ошибка когда нет лекарств в инвентаре"""

    def __init__(self, message: str = "В инвентаре нет лекарств! Купите лекарства в магазине."):
        self.message = message
        super().__init__(self.message)
