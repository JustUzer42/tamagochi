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
