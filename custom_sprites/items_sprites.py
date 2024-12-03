# ./custom_sprites/items_sprites.py:
import pygame
import math
import game_constants
import custom_funcs

from game_constants import CUSTOM_EVENTS_IDS
from custom_funcs import add_SELF_to_groups, cut_image, activate_with_temp_forbid, delayed_activating

IMG_WEAPONS = pygame.image.load("textures/weapons.png")


class Bullet(pygame.sprite.Sprite):
    def __init__(self, gun, target: tuple, game_groups_dict: dict):
        super().__init__()
        self.gun = gun
        self.target = target
        self.game_groups_dict = game_groups_dict
        self.initial_groups_names = ["all_sprites_group",
                                     "item_sprites_group",
                                     "map_kit_group",
                                     "displaying_objects_group",
                                     "bullets_group"]
        self.displaying_layer = 11
        add_SELF_to_groups(self, self.game_groups_dict,
                           self.initial_groups_names, self.displaying_layer)

        self.image = pygame.Surface((10, 5), pygame.SRCALPHA)
        self.image.fill((255, 255, 255))
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = self.gun.rect.centerx + \
            5 * math.sin(-self.gun.image_angle) * \
            (1 if self.gun.image_mirror_x else -1)
        self.rect.y = self.gun.rect.centery + \
            10 * math.cos(-self.gun.image_angle) * \
            (1 if self.gun.image_mirror_x else -1)
        self.speed = self.gun.bullet_speed
        self.speed_x = 0
        self.speed_y = 0

        # Чтобы не было округлений rect.y и rect.x
        self.next_frame_rect_x = self.rect.x
        self.next_frame_rect_y = self.rect.y

        self.rotate()
        self.calc_move_vector()

    def rotate(self):
        self.image = pygame.transform.rotate(
            self.original_image, math.degrees(-self.gun.image_angle))

    def calc_move_vector(self):
        direction_x = self.target[0] - self.rect.centerx
        direction_y = self.target[1] - self.rect.centery
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        self.speed_x = direction_x / distance * self.speed
        self.speed_y = direction_y / distance * self.speed

    def move(self):
        self.next_frame_rect_x += self.speed_x / game_constants.FPS_LIMIT
        self.next_frame_rect_y += self.speed_y / game_constants.FPS_LIMIT

        self.rect.x = self.next_frame_rect_x
        self.rect.y = self.next_frame_rect_y

    def process_collisions(self, **kwargs):
        player = kwargs["player"]
        bullets_group = self.game_groups_dict["bullets_group"]
        units_group = self.game_groups_dict["units_group"]
        first_collided_sprite = pygame.sprite.spritecollideany(
            self, units_group)

        # print(first_collided_sprite, first_collided_sprite != self.gun.owner, first_collided_sprite and first_collided_sprite != self.gun.owner
        #       and first_collided_sprite._is_object_displaying())

        if first_collided_sprite and first_collided_sprite != self.gun.owner \
                and first_collided_sprite._is_object_displaying():
            first_collided_sprite.take_damage(self.gun.damage)
            self.kill()

    def update(self, **kwargs):
        self.process_collisions(**kwargs)
        self.move()


class BasicItem(pygame.sprite.Sprite):
    def __init__(self, game_groups_dict: dict, initial_groups: list):
        super().__init__()
        self.owner = None
        self.game_groups_dict = game_groups_dict
        self.initial_groups_names = initial_groups
        self.displaying_layer = 12
        add_SELF_to_groups(self, game_groups_dict,
                           initial_groups, layer=self.displaying_layer)
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        self.image.fill((255, 255, 255))
        self.original_image = self.image.copy()
        self.image_scale = 1
        self.image_angle = 0
        self.image_mirror_x = False
        self.rect = self.image.get_rect()

        # Базовые параметры
        self.name = "An_Item"
        self._flags = {}

    def _change_flag(self, flag: str, *bool_value):
        '''Меняет флаг в словаре _flags.
           Если передан аргумент bool_value, устанавливает флаг в указанное значение, иначе инвертирует текущий флаг.'''
        if bool_value:
            value = bool_value[0]
            self._flags[flag] = value
        else:
            self._flags[flag] = not self._flags[flag]

    def _get_flag(self, flag_name):
        '''Возвращает текущее значение флага по имени из словаря _flags.'''
        return self._flags[flag_name]

    def left_mouse_click_action(self, pressed_unpressed):
        return

    def right_mouse_click_action(self, pressed_unpressed):
        return

    def mid_mouse_click_action(self, pressed_unpressed):
        return

    def set_displaying(self, bool_value: bool, *layer: int):
        if bool_value:
            if not layer or len(layer) > 1:
                custom_funcs.INTERRUPT_ERROR(3)
            if self._is_object_displaying() == False and \
                    not self.__class__ == BasicItem:
                self.game_groups_dict["displaying_objects_group"].add(
                    self, layer=layer[0])
        else:
            self.game_groups_dict["displaying_objects_group"].remove(self)

    def _is_object_displaying(self):
        return self in self.game_groups_dict["displaying_objects_group"]

    def player_takes_item(self, player):
        self.game_groups_dict["player_kit_group"].add(self)
        self.set_displaying(False)

    def follow_player(self, player: pygame.sprite.Sprite):
        angle = self._get_angle_to_mouse(self.rect.center)

        # Для поворота не вокруг точного центра спрйта,
        # а вокруг некоторой точки между мышкой и спрайтом:
        sin = math.sin(angle)
        cos = math.cos(angle)
        self.rect.center = (
            player.rect.x + 10 + (10 * -cos),
            player.rect.y + 40 + (10 * -sin)
        )

    def _get_angle_to_mouse(self, first_point):
        '''Получает угол между двумя точками'''
        first_point = first_point
        second_point = pygame.mouse.get_pos()

        dx = second_point[0] - first_point[0]  # Разница по оси X
        # Разница по оси Y с учетом высоты спрайта для более корректного отображения
        dy = second_point[1] - first_point[1] + \
            self.image.get_height() // self.image_scale
        angle = math.atan2(dy, dx)  # Вычисление угла в радианах
        self.image_angle = angle
        return angle

    def rotate(self):
        """Поворачивает изображение спрайта на заданный угол и отзеркаливает 
        при необходимости, чтобы спрайт правильно следил за мышью."""
        mouse_pos = pygame.mouse.get_pos()
        angle = self._get_angle_to_mouse(self.rect.center)
        angle_degrees = math.degrees(-angle)  # Переводим в градусы
        if mouse_pos[0] < self.rect.centerx:  # Мышь слева от спрайта
            angle_degrees = -angle_degrees + 180
        self.image = pygame.transform.rotate(
            self.original_image, angle_degrees)
        if mouse_pos[0] < self.rect.centerx:  # Мышь слева от спрайта
            self.image = pygame.transform.flip(self.image, True, False)
            self.image_mirror_x = True
        else:
            self.image_mirror_x = False
        self.rect = self.image.get_rect(center=self.rect.center)

    def deepcopy(self):
        new_instance = self.__class__(
            game_groups_dict=self.game_groups_dict, initial_groups=self.initial_groups_names)
        new_instance.image = self.image.copy()
        new_instance.rect = new_instance.image.get_rect()
        for key, value in self.__dict__.items():
            if key not in ["image", "rect"]:
                if isinstance(value, (list, dict, set)):
                    setattr(new_instance, key, value.copy())
                else:
                    setattr(new_instance, key, value)
        new_instance
        add_SELF_to_groups(new_instance, self.game_groups_dict,
                           self.initial_groups_names, layer=11)
        return new_instance

    def set_owner(self, owner):
        self.owner = owner

    def get_owner(self):
        return self.owner

    def update(self, **kwargs):
        player = kwargs['player']
        if self == player.active_slot:
            self.set_displaying(True, self.displaying_layer)
            self.rotate()


class Gun(BasicItem):
    def __init__(self, game_groups_dict: dict, initial_groups: list):
        super().__init__(game_groups_dict, initial_groups)
        self.game_groups_dict["displaying_objects_group"].change_layer(
            self, 11)
        self.name = "A_Gun"

        self.bullet_speed = 350  # Пикселей в секунду
        self.damage = 10        # Урон от оружия
        self.fire_rate = 1000   # Скорострельность
        self.reload_time = 2000
        self.ammo = 5      # Размер обоймы
        self.shots_left = self.ammo

        self.rect = self.image.get_rect()

        self._flags = {
            "is_gun_shooting_now": False,
            "is_reloading_now": False,
        }

    def left_mouse_click_action(self, pressed_unpressed: bool):
        if pressed_unpressed:
            self._change_flag("is_gun_shooting_now", True)
        else:
            self._change_flag("is_gun_shooting_now", False)

    def try_shoot(self, target_pos):
        if self._can_shoot(1):
            self.shoot(target_pos)
            self.spend_shots(1)
            if self.shots_left == 0:
                self.reload_ammo()

    def shoot(self, target_pos):
        Bullet(gun=self,
               target=target_pos,
               game_groups_dict=self.game_groups_dict)

    def spend_shots(self, count):
        if self._can_shoot(count):
            self.shots_left -= count

    def add_shots(self, count):
        self.shots_left = min(self.ammo, self.shots_left + count)

    def gun_is_fully_reloaded(self):
        self._change_flag("is_reloading_now", False)

    def reload_ammo(self):
        self._change_flag("is_reloading_now", True)
        delayed_activating(id=CUSTOM_EVENTS_IDS["reload_event"],
                           delay=self.reload_time,
                           function=self.add_shots,
                           count=self.ammo)
        delayed_activating(id=CUSTOM_EVENTS_IDS["gun_ends_reloading_event"],
                           delay=self.reload_time,
                           function=self.gun_is_fully_reloaded)

    def _can_shoot(self, count):
        return self.shots_left - count >= 0

    def update(self, **kwargs):
        player = kwargs['player']
        if self == player.active_slot:
            self.set_displaying(True, self.displaying_layer)
            self.rotate()
        if self._get_flag("is_gun_shooting_now"):
            activate_with_temp_forbid(id=CUSTOM_EVENTS_IDS["shoot_event"],
                                      delay=self.fire_rate,
                                      function=self.try_shoot,
                                      target_pos=pygame.mouse.get_pos())


class Pistol(Gun):
    def __init__(self, game_groups_dict: dict, initial_groups: list):
        super().__init__(game_groups_dict, initial_groups)

        self.name = "Pistol"
        self.ammo = 500
        self.shots_left = self.ammo
        self.fire_rate = 100

        self.image = cut_image(IMG_WEAPONS, (0, 118), (12, 10))
        width, height = self.image.get_size()
        self.image_scale = 3
        self.image = pygame.transform.scale(
            self.image, (width * self.image_scale, height * self.image_scale))
        self.original_image = self.image.copy()


class SplashGun(BasicItem):
    def __init__(self, game_groups_dict: dict, initial_groups: list):
        super().__init__(game_groups_dict, initial_groups)
        self.image = pygame.Surface((30, 10))
        self.gun_color = (128, 128, 255)
        self.image.fill(self.gun_color)
        self.rect = self.image.get_rect()

        self.name = "SplashGun"
