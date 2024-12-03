import pygame
import custom_funcs as cf
import game_constants as gc
import random
import math
import time

from custom_funcs import add_SELF_to_groups


class HpBar(pygame.sprite.Sprite):
    def __init__(self, game_groups_dict: dict, owner: pygame.sprite.Sprite):
        super().__init__()
        self.game_groups_dict = game_groups_dict
        self.initial_groups = ["all_sprites_group",
                               "map_kit_group",
                               "displaying_objects_group"]
        self.layer = 12
        add_SELF_to_groups(self, self.game_groups_dict,
                           self.initial_groups,
                           self.layer)

        self.owner = owner
        self.image = pygame.Surface((40, 10))
        self.image.fill((128, 64, 64))
        pygame.draw.rect(self.image, (255, 64, 64), (2, 2, 36, 6))
        self.rect = self.image.get_rect()

    def _is_object_displaying(self):
        return self in self.game_groups_dict["displaying_objects_group"]

    def set_displaying(self, bool_value: bool, *layer: int):
        if bool_value:
            if not layer or len(layer) > 1:
                cf.INTERRUPT_ERROR(3)
            if self._is_object_displaying() == False:
                self.game_groups_dict["displaying_objects_group"].add(
                    self, layer=layer[0])
        else:
            self.game_groups_dict["displaying_objects_group"].remove(self)

    def update(self, **kwargs):
        self.set_displaying(self.owner._is_object_displaying(), self.layer)
        self.rect.x = self.owner.rect.centerx - self.owner.image.get_width() / 2
        self.rect.y = self.owner.rect.y - 20
        self.image.fill((128, 64, 64))
        pygame.draw.rect(self.image, (255, 64, 64), (2, 2, 36 *
                                                     self.owner.hp / (self.owner.max_hp * self.owner.hp_multiplier), 6))


class BasicEnemy(pygame.sprite.Sprite):
    def __init__(self, game_groups_dict: dict, initial_groups: list, start_pos=[100, 100]):
        super().__init__()
        self.game_groups_dict = game_groups_dict
        self.initial_groups_names = initial_groups
        self.displaying_layer = 9
        add_SELF_to_groups(self, game_groups_dict,
                           initial_groups,
                           layer=self.displaying_layer)

        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]

        self.speed = 150
        self.max_hp = 100
        self.hp_multiplier = 1
        self.hp = self.max_hp * self.hp_multiplier
        self.hp_bar = HpBar(game_groups_dict=self.game_groups_dict, owner=self)

        self._status = {
            "moving": True,
            "attack": False,
            "escaping": False,
            "random_movement": False,
        }

        self.timers = {
            "escape_timer": 0,
            "escape_duration": 0,
            "random_movement_timer": 0,
            "random_movement_duration": 0
        }

    def _is_object_displaying(self):
        return self in self.game_groups_dict["displaying_objects_group"]

    def set_displaying(self, bool_value: bool, *layer: int):
        if bool_value:
            if not layer or len(layer) > 1:
                cf.INTERRUPT_ERROR(3)
            if self._is_object_displaying() == False:
                self.game_groups_dict["displaying_objects_group"].add(
                    self, layer=layer[0])
        else:
            self.game_groups_dict["displaying_objects_group"].remove(self)
# =============================================================== STATUSES

    def status_moving(self):
        '''Функция для обработки статуса игрока "moving" (движется).'''
        if self._status["moving"]:
            pass
        else:
            pass

    def status_attack(self):
        '''Функция для обработки статуса игрока "attack" (атакует).'''
        if self._status["attack"]:
            pass
        else:
            pass
# =============================================================== HP

    def take_damage(self, value):
        self.hp = max(0, self.hp - value)

    def add_hp(self, value):
        self.hp = min(self.max_hp * self.hp_multiplier, self.hp + value)

    def update_hp(self):
        if self.hp < 1:
            self.kill()
            self.hp_bar.kill()

        self.status_moving()
        self.status_attack()

# =============================================================== COLLISIONS

    def update(self, **kwargs):
        player = kwargs['player']
        self.update_hp()
        self.follow_player(player)

# =============================================================== FAKE AI

    def random_movement(self):
        pass

    def follow_player(self, player):
        """Обновляет позицию монстра, чтобы он следовал за игроком."""
        current_time = time.time()

        # Получаем позиции
        player_x, player_y = player.rect.center
        monster_x, monster_y = self.rect.center

        # Вычисляем разницу в координатах
        diff_x = player_x - monster_x
        diff_y = player_y - monster_y

        # Вычисляем расстояние до игрока
        distance = math.sqrt(diff_x**2 + diff_y**2)

        # --- Убегание ---
        if distance < 50 and not self._status["escaping"]:
            self._status["escaping"] = True
            self.timers["escape_duration"] = random.uniform(0.5, 1.2)
            self.timers["escape_timer"] = current_time

        if self._status["escaping"]:
            if current_time - self.timers["escape_timer"] < self.timers["escape_duration"]:
                # Убегаем от игрока
                norm_x = -diff_x / (distance + 1)
                norm_y = -diff_y / (distance + 1)
                move_speed = self.speed / 2 * random.uniform(0.2, 2)
            else:
                # Завершаем режим убегания
                self._status["escaping"] = False
                norm_x = diff_x / (distance + 1)
                norm_y = diff_y / (distance + 1)
                move_speed = self.speed
        else:
            # Нормальное преследование
            norm_x = diff_x / (distance + 1)
            norm_y = diff_y / (distance + 1)
            move_speed = self.speed

        # --- Случайное поведение ---
        if not self._status["escaping"]:
            # Проверяем, можно ли активировать случайное движение
            if current_time - self.timers["random_movement_timer"] > 0.5:
                self.timers["random_movement_timer"] = current_time
                if random.random() < 0.3:
                    self._status["random_movement"] = True
                    self.timers["random_movement_duration"] = random.uniform(
                        0.5, 1.5)

                    # Генерируем фиксированное отклонение
                    self.random_offset_x = random.uniform(-2, 2)
                    self.random_offset_y = random.uniform(-2, 2)
                    self.random_speed_multiplier = random.uniform(
                        0.75, 1.5)
                else:
                    self.random_offset_x = 0
                    self.random_offset_y = 0
                    self.random_speed_multiplier = random.uniform(0.75, 1.5)

                if distance > 200:
                    self.random_offset_x = 0
                    self.random_offset_y = 0
                    self.random_speed_multiplier = random.uniform(0.75, 1.5)

            # Если случайное движение активно
            if self._status["random_movement"]:
                if current_time - self.timers["random_movement_timer"] < self.timers["random_movement_duration"]:
                    # Добавляем зафиксированные отклонения
                    norm_x += self.random_offset_x
                    norm_y += self.random_offset_y

                    # Нормализуем вектор
                    magnitude = math.sqrt(norm_x**2 + norm_y**2)
                    norm_x /= magnitude
                    norm_y /= magnitude

                    # Используем фиксированный множитель скорости
                    move_speed *= self.random_speed_multiplier
                else:
                    # Завершаем случайное движение
                    self._status["random_movement"] = False

        # Вычисляем движение
        move_x = norm_x * move_speed / gc.FPS_LIMIT
        move_y = norm_y * move_speed / gc.FPS_LIMIT

        # Обновляем позицию монстра
        self.rect.x += move_x
        self.rect.y += move_y


class Skeleton(BasicEnemy):
    def __init__(self, game_groups_dict: dict, initial_groups: list, start_pos=[100, 100]):
        super().__init__(game_groups_dict=game_groups_dict,
                         initial_groups=initial_groups, start_pos=start_pos)

    def update(self, **kwargs):
        return super().update(**kwargs)
