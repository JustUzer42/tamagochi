"""Пакет game для проекта Тамагочи-кликер."""

from game.clicker import AbstractClicker, SimpleRandomClicker
from game.tamagochi import AbstractTamagochi, SimpleTamagochi
from game.game import AbstractGame, SimpleGame
from game.models import Food, Medicine
from game.exceptions import TamagochiIsGone, NotEnoughMoney

__all__ = [
    "AbstractClicker",
    "SimpleRandomClicker",
    "AbstractTamagochi",
    "SimpleTamagochi",
    "AbstractGame",
    "SimpleGame",
    "Food",
    "Medicine",
    "TamagochiIsGone",
    "NotEnoughMoney",
]
