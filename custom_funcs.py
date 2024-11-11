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


def delayed_activating(id: int, delay: int, function, *args):
    if id not in delayed_events:
        delayed_events[id] = (function, args)
        pygame.time.set_timer(pygame.USEREVENT + id, delay, loops=1)
    else:
        if delayed_events[id][0] != function:
            raise ValueError(
                f"Невозможно привязать функцию {function} к id {id}, "
                f"так как id занят функцией {delayed_events[id]}"
            )


# ======================================================== KEY PRESSED


KEYS_DICT = game_constants.KEYS_DICT


def key_pressed(keys_pressed: list, *args) -> bool:
    return all(keys_pressed[KEYS_DICT[key]] for key in args)
