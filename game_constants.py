import pygame

# ./game_constants
#  Размеры экрана
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

# Ограничение фпс
FPS_LIMIT = 60

# Словарь кастомных ивентов
CUSTOM_EVENTS_IDS = {
    "shoot_event": 1,
    "reload_event": 2,
    "sprint_event": 3,
    "add_stamina_event": 4,
    "gun_ends_reloading_event": 5,
    "restore_stamina_by_time_event": 6,
    "open_door_event": 7,
    "level_started_event": 8,
    "return_to_zero_level_event": 9,
    "level_ended_event": 10,
}

# Словарь для чуть более удобной работы с pygame.key
KEYS_DICT = {
    "A": pygame.K_a,
    "B": pygame.K_b,
    "C": pygame.K_c,
    "D": pygame.K_d,
    "E": pygame.K_e,
    "F": pygame.K_f,
    "G": pygame.K_g,
    "H": pygame.K_h,
    "I": pygame.K_i,
    "J": pygame.K_j,
    "K": pygame.K_k,
    "L": pygame.K_l,
    "M": pygame.K_m,
    "N": pygame.K_n,
    "O": pygame.K_o,
    "P": pygame.K_p,
    "Q": pygame.K_q,
    "R": pygame.K_r,
    "S": pygame.K_s,
    "T": pygame.K_t,
    "U": pygame.K_u,
    "V": pygame.K_v,
    "W": pygame.K_w,
    "X": pygame.K_x,
    "Y": pygame.K_y,
    "Z": pygame.K_z,

    "0": pygame.K_0,
    "1": pygame.K_1,
    "2": pygame.K_2,
    "3": pygame.K_3,
    "4": pygame.K_4,
    "5": pygame.K_5,
    "6": pygame.K_6,
    "7": pygame.K_7,
    "8": pygame.K_8,
    "9": pygame.K_9,

    "ESC": pygame.K_ESCAPE,
    "ENTER": pygame.K_RETURN,
    "TAB": pygame.K_TAB,
    "BACKSPACE": pygame.K_BACKSPACE,
    "SPACE": pygame.K_SPACE,
    "CAPSLOCK": pygame.K_CAPSLOCK,
    "L_SHIFT": pygame.K_LSHIFT,
    "L_CTRL": pygame.K_LCTRL,
    "L_ALT": pygame.K_LALT,
    "PAGEUP": pygame.K_PAGEUP,
    "PAGEDOWN": pygame.K_PAGEDOWN,
    "DELETE": pygame.K_DELETE,
    "END": pygame.K_END,
    "UP": pygame.K_UP,
    "DOWN": pygame.K_DOWN,
    "LEFT": pygame.K_LEFT,
    "RIGHT": pygame.K_RIGHT
}
