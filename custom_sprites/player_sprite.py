# ./custom_sprites/player_sprite.py:
import pygame
import game_constants
import custom_sprites.guns_sprites as guns_sprites
import custom_funcs
from custom_funcs import key_pressed, any_key_pressed


class Player(pygame.sprite.Sprite):
    def __init__(self, initial_groups):
        super().__init__()
        for group in initial_groups:
            group.add(self, layer=10)

        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()

        self.stamina = 100
        self.movement_speed = 200  # Скорость движения игрока в пикселах в секунду
        self.damage_multiplier = 1
        self.speed_multiplier = 1
        self.hp_multiplier = 1

        self.inventory = [None, None]  # Для ближнего и дальнего боя
        self.equipment = [None, None]  # Для шлема и ботинок

        # Список предметов, которые купил или иным образом заполучил игрок.
        # Если их нет в инвентаре, то при их наличии в списке игрок сможет бесплатно
        # получить в инвентарь предмет. Если предмета нет в списке, то для того чтобы
        # заполучить предмет в инвентарь, нужно его разблокировать, например, купив.
        self.unlocked_items = [guns_sprites.Pistol]
        self.sprint_event_id = game_constants.CUSTOM_EVENTS_IDS['sprint_event']
        self.add_stamina_event_id = game_constants.CUSTOM_EVENTS_IDS['add_stamina_event']
        self._flags = {
            "can_restore_stamina_by_time": True,
            "can_shoot": True,
        }

    def _change_flag(self, flag: str, *bool):
        if bool:
            self._flags[flag] = bool
        else:
            self._flags[flag] = not self._flags[flag]

    def _get_flag(self, flag_name):
        return self._flags[flag_name]

    def add_to_inventory(self, item):
        pass

    def spend_stamina(self, value):
        if self.stamina - value >= 0:
            self.stamina -= value

            if self._get_flag("can_restore_stamina_by_time"):
                self._change_flag("can_restore_stamina_by_time", False)
                custom_funcs.delayed_activating(
                    id=self.add_stamina_event_id, delay=2000, function=self._change_flag, flag="can_restore_stamina_by_time", bool=True)

    def restore_stamina_by_time(self):
        if self._get_flag("can_restore_stamina_by_time"):
            custom_funcs.activate_with_temp_forbid(
                id=self.add_stamina_event_id, delay=125, function=self.add_stamina, value=4)

    def add_stamina(self, value):
        if self.stamina + value <= 100:
            self.stamina += value

    def update(self, keys_pressed):
        print(self.stamina)
        if self.stamina < 100:
            self.restore_stamina_by_time()

        K_P = keys_pressed

        # Вычисляем движения по осям X и Y
        move_x = 0
        move_y = 0

        if key_pressed(K_P, "A"):  # Нажата клавиша 'A' (влево)
            move_x = -self.movement_speed
        if key_pressed(K_P, "D"):  # Нажата клавиша 'D' (вправо)
            move_x = self.movement_speed
        if key_pressed(K_P, "W"):  # Нажата клавиша 'W' (вверх)
            move_y = -self.movement_speed
        if key_pressed(K_P, "S"):  # Нажата клавиша 'S' (вниз)
            move_y = self.movement_speed

        if key_pressed(K_P, "L_SHIFT"):
            move_x = move_x * 1.5
            move_y = move_y * 1.5

        if key_pressed(K_P, "L_SHIFT") and any_key_pressed(K_P, "W", "S", "A", "D"):
            custom_funcs.activate_with_temp_forbid(id=self.sprint_event_id, delay=100,
                                                   function=self.spend_stamina, value=4)

        # Если движение происходит по диагонали, нормализуем скорость
        if move_x != 0 and move_y != 0:
            slowdown_ratio = 1.3
            move_x = move_x / slowdown_ratio
            move_y = move_y / slowdown_ratio

        # Обновляем позицию
        self.rect.x += move_x / game_constants.FPS_LIMIT
        self.rect.y += move_y / game_constants.FPS_LIMIT
