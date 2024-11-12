# ./custom_funcs.py
import pygame
import game_constants

forbidden_events = {}
delayed_events = {}

# ======================================================== FORBIDDEN


def get_forbidden_events():
    return forbidden_events


def get_forbidden_event(id: int):
    if id in forbidden_events:
        return forbidden_events[id]
    else:
        return False


def remove_forbidden_event(id: int):
    forbidden_events.pop(id, 0)


def activate_with_temp_forbid(id: int, delay: int, function, **kwargs):
    '''
    Привязывает функцию к указанному ID с задержкой на повторный вызов, временно блокируя 
    выполнение функции по этому ID, если она уже вызвана.

    - Если ID ещё не используется в forbidden_events, функция будет выполнена сразу, 
      а затем вызов будет заблокирован на указанное время `delay`. Иными словами, при 
      вызове Этой функции с указанием другой функции, указанная функция будет выполняться 
      не чаще, чем 1 раз за `delay` 

    - Если попытаться привязать другую функцию к уже занятому ID, будет вызвана ошибка, 
      предотвращая случайное переприсвоение ID другой функции.
    '''
    if id not in forbidden_events:
        forbidden_events[id] = function
        function(**kwargs)
        pygame.time.set_timer(pygame.USEREVENT + id, delay, loops=1)
    else:
        if forbidden_events[id] != function:
            raise ValueError(
                f"Невозможно привязать функцию {function} к id {id}, "
                f"так как id занят функцией {forbidden_events[id]}"
            )

# ======================================================== DELAYED


def get_delayed_events():
    return delayed_events


def get_delayed_event(id: int):
    if id in delayed_events:
        return delayed_events[id]
    else:
        return False


def remove_delayed_event(id: int):
    delayed_events.pop(id, 0)


def delayed_activating(id: int, delay: int, function, **kwargs):
    '''
    Позволяет вызвать указанную функцию с указанной задержкой по указанному айди. 
    Если попытаться привязать к одному айди две разные функции, произойдет вызов ошибки. 
    Если повторно установить задержку одной и той же функции с одним и тем же айди, 
    функция будет вызвана через обновленное значение задержки (без учета прошедшего
    времени с момента предыдущей задержки функции)
    '''
    if id not in delayed_events:
        delayed_events[id] = (function, kwargs)
        pygame.time.set_timer(pygame.USEREVENT + id, delay, loops=1)
    else:
        if delayed_events[id][0] != function:
            raise ValueError(
                f"Невозможно привязать функцию {function} к id {id}, "
                f"так как id занят функцией {delayed_events[id]}"
            )
        else:
            pygame.time.set_timer(pygame.USEREVENT + id, delay, loops=1)


# ======================================================== KEY PRESSED


KEYS_DICT = game_constants.KEYS_DICT


def key_pressed(keys_pressed: list, *args) -> bool:
    return all(keys_pressed[KEYS_DICT[key]] for key in args)


def any_key_pressed(keys_pressed: list, *args) -> bool:
    return any(keys_pressed[KEYS_DICT[key]] for key in args)
