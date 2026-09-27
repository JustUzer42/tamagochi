"""Тесты на логику"""

import pytest
from unittest.mock import patch
from io import StringIO

from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi
from game.clicker import SimpleRandomClicker
from game.game import SimpleGame
from game.exceptions import TamagochiIsGone, NotEnoughMoney


def test_main_import_and_exit():
    """Проверка что main() при вводе '0' корректно завершает работу"""
    import main
    
    with patch('builtins.input', return_value='0'):
        with patch('sys.stdout', new_callable=StringIO):
            # Должна завершиться без исключений
            try:
                main.main()
            except SystemExit:
                pass  # OK
            except Exception as e:
                pytest.fail(f"main() должна завершаться без исключений при вводе '0', но получено: {e}")


def test_game_status():
    """Проверка что можно получить статус игры"""
    tamagochi = SimpleTamagochi()
    clicker = SimpleRandomClicker(10, 20)
    all_food = [Food(name='Бургер', satiety=20, price=40)]
    all_medicine = [Medicine(name='Ибупрофен', price=30, heal_hp=20, number_of_uses=2)]
    
    game = SimpleGame(tamagochi, clicker, all_food, all_medicine)
    status = game.get_status()
    
    assert isinstance(status, dict)
    assert 'hunger' in status
    assert 'hp' in status
    assert 'energy' in status
    assert 'coins' in status


def test_tamagochi_feed_hunger():
    """Проверка что кормление уменьшает голод"""
    tamagochi = SimpleTamagochi()
    food = Food(name='Бургер', satiety=20, price=40)
    
    tamagochi._hunger = 30
    tamagochi.feed(food)
    
    assert tamagochi.status['hunger'] == 10


def test_tamagochi_rest_increases_energy():
    """Проверка что отдых увеличивает энергию"""
    tamagochi = SimpleTamagochi()
    tamagochi._energy = 50
    
    tamagochi.rest()
    
    assert tamagochi.status['energy'] == 70


def test_tamagochi_heal_increases_hp():
    """Проверка что лечение увеличивает HP"""
    tamagochi = SimpleTamagochi()
    tamagochi._hp = 50
    tamagochi._is_sick = True
    
    medicine = Medicine(name='Ибупрофен', price=30, heal_hp=20, number_of_uses=2)
    tamagochi.heal(medicine)
    
    assert tamagochi.status['hp'] == 70
    assert tamagochi.is_sick() == False


def test_tamagochi_play_changes_state():
    """Проверка что игра меняет состояния"""
    tamagochi = SimpleTamagochi()
    initial_status = tamagochi.status.copy()
    
    tamagochi.play()
    
    assert tamagochi.status['hunger'] == initial_status['hunger'] + 5
    assert tamagochi.status['energy'] == initial_status['energy'] - 15


def test_tamagochi_update_progress_or_end():
    """Проверка что update меняет состояния"""
    tamagochi = SimpleTamagochi()
    initial_status = tamagochi.status.copy()
    
    tamagochi.update()
    
    assert tamagochi.status['hunger'] == initial_status['hunger'] + 5
    assert tamagochi.status['energy'] == initial_status['energy'] - 3


def test_work_increases_coins_and_calls_click():
    """Проверка что работа увеличивает монеты"""
    tamagochi = SimpleTamagochi()
    clicker = SimpleRandomClicker(10, 20)
    all_food = []
    all_medicine = []
    
    game = SimpleGame(tamagochi, clicker, all_food, all_medicine)
    income = game.work()
    
    assert 10 <= income <= 20
    assert tamagochi.status['coins'] == income


def test_game_buy_food_adds_inventory():
    """Проверка что покупка еды добавляет её в инвентарь"""
    tamagochi = SimpleTamagochi()
    tamagochi._coins = 100
    clicker = SimpleRandomClicker(10, 20)
    all_food = [Food(name='Бургер', satiety=20, price=40)]
    all_medicine = []
    
    game = SimpleGame(tamagochi, clicker, all_food, all_medicine)
    
    # Симулируем выбор
    with patch('builtins.input', return_value='1'):
        game.buy_food()
    
    assert len(game.food) == 1
    assert game.food[0].name == 'Бургер'


def test_game_feed_removes_selected_item_from_inventory():
    """Проверка что кормление удаляет еду из инвентаря"""
    tamagochi = SimpleTamagochi()
    tamagochi._coins = 100  # Достаточно монет для покупки
    clicker = SimpleRandomClicker(10, 20)
    all_food = [Food(name='Бургер', satiety=20, price=40)]
    all_medicine = []
    
    game = SimpleGame(tamagochi, clicker, all_food, all_medicine)
    
    # Сначала покупаем еду
    with patch('builtins.input', return_value='1'):
        game.buy_food()
    
    assert len(game.food) == 1
    
    # Затем кормим
    with patch('builtins.input', return_value='1'):
        game.feed_tamagochi()
    
    assert len(game.food) == 0


def test_game_buy_medicine_adds_inventory():
    """Проверка что покупка лекарства добавляет его в инвентарь"""
    tamagochi = SimpleTamagochi()
    tamagochi._coins = 100
    clicker = SimpleRandomClicker(10, 20)
    all_food = []
    all_medicine = [Medicine(name='Ибупрофен', price=30, heal_hp=20, number_of_uses=2)]
    
    game = SimpleGame(tamagochi, clicker, all_food, all_medicine)
    
    with patch('builtins.input', return_value='1'):
        game.buy_medicine()
    
    assert len(game.medicine) == 1
    assert game.medicine[0].name == 'Ибупрофен'


def test_game_end_condition_reachable():
    """Проверка что игра может завершиться (питомец умирает)"""
    tamagochi = SimpleTamagochi()
    clicker = SimpleRandomClicker(10, 20)
    all_food = []
    all_medicine = []
    
    game = SimpleGame(tamagochi, clicker, all_food, all_medicine)
    
    # Убиваем питомца
    tamagochi._hp = 0
    
    assert game.tamagochi.is_alive() == False
    
    # Работа должна выбросить исключение
    with pytest.raises(TamagochiIsGone):
        game.work()
