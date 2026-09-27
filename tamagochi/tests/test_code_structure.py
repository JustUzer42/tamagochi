"""Тесты на структуру кода"""

import pytest
import inspect


def test_modules_present():
    """Проверка что все модули существуют"""
    import game.clicker
    import game.game
    import game.tamagochi
    import game.models
    import game.exceptions


def test_models_exist():
    """Проверка что модели существуют"""
    from game import models
    assert hasattr(models, 'Food')
    assert hasattr(models, 'Medicine')


def test_exceptions_exist():
    """Проверка что исключения существуют"""
    from game import exceptions
    assert hasattr(exceptions, 'TamagochiIsGone')
    assert hasattr(exceptions, 'NotEnoughMoney')


def test_abstract_interfaces_shape():
    """Проверка что абстрактные классы имеют нужные методы"""
    from game.clicker import AbstractClicker
    from game.tamagochi import AbstractTamagochi
    from game.game import AbstractGame

    # AbstractClicker должен иметь click и income_per_click
    assert hasattr(AbstractClicker, 'click')
    assert hasattr(AbstractClicker, 'income_per_click')

    # AbstractTamagochi должен иметь нужные методы
    for method in ['feed', 'play', 'rest', 'heal', 'status', 'is_alive', 'is_sick', 'update']:
        assert hasattr(AbstractTamagochi, method), f"AbstractTamagochi должен иметь метод {method}"

    # AbstractGame должен иметь нужные методы
    for method in ['work', 'buy_food', 'buy_medicine', 'feed_tamagochi', 'heal_tamagochi', 'rest_tamagochi', 'play_with_tamagochi', 'get_status']:
        assert hasattr(AbstractGame, method), f"AbstractGame должен иметь метод {method}"


def test_concrete_implementation_exists():
    """Проверка что есть конкретные реализации абстрактных классов"""
    from game.clicker import AbstractClicker
    from game.tamagochi import AbstractTamagochi
    from game.game import AbstractGame

    # Проверяем clicker
    import game.clicker as clicker_module
    clicker_classes = [
        name for name, obj in inspect.getmembers(clicker_module, inspect.isclass)
        if issubclass(obj, AbstractClicker) and obj != AbstractClicker
    ]
    assert len(clicker_classes) > 0, "В game.clicker добавьте класс наследник абстрактного класса AbstractClicker."

    # Проверяем tamagochi
    import game.tamagochi as tamagochi_module
    tamagochi_classes = [
        name for name, obj in inspect.getmembers(tamagochi_module, inspect.isclass)
        if issubclass(obj, AbstractTamagochi) and obj != AbstractTamagochi
    ]
    assert len(tamagochi_classes) > 0, "В game.tamagochi добавьте класс наследник абстрактного класса AbstractTamagochi."

    # Проверяем game
    import game.game as game_module
    game_classes = [
        name for name, obj in inspect.getmembers(game_module, inspect.isclass)
        if issubclass(obj, AbstractGame) and obj != AbstractGame
    ]
    assert len(game_classes) > 0, "В game.game добавьте класс наследник абстрактного класса AbstractGame."


def test_main_symbol_exists():
    """Проверка что в main.py есть функция main"""
    import main
    assert hasattr(main, 'main')
    assert callable(main.main)
