# ./custom_sprites/items_sprites.py:
import pygame
from custom_funcs import add_SELF_to_groups


class BasicItem(pygame.sprite.Sprite):
    def __init__(self, game_groups_dict: dict, initial_groups: list):
        super().__init__()
        self.game_groups_dict = game_groups_dict
        self.initial_groups_names = initial_groups

        add_SELF_to_groups(self, game_groups_dict, initial_groups)

        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        if self.__class__ == BasicItem:
            self.image.set_alpha(0)

        # Базовые параметры
        self.name = "An_Item"

    def player_takes_item(self, player):
        self.game_groups_dict["player_kit_group"].add(self)
        self.set_displaying(False)

    def follow_player(self, player: pygame.sprite.Sprite):
        self.rect.center = (
            player.rect.x,
            player.rect.y
        )

    def update(self, **kwargs):
        if self == kwargs['player'].active_slot:
            print(self.name, kwargs["player"].active_slot.name, kwargs["player"].active_slot_index)
            self.set_displaying(True)

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
        return new_instance

    def set_displaying(self, bool_value: bool):
        if bool_value:
            if self._is_object_displaying() == False:
                self.game_groups_dict["displaying_objects_group"].add(self)
        else:
            self.game_groups_dict["displaying_objects_group"].remove(self)

    def _is_object_displaying(self):
        return self in self.game_groups_dict["displaying_objects_group"]


class Gun(BasicItem):
    def __init__(self, game_groups_dict: dict, initial_groups: list):
        super().__init__(game_groups_dict, initial_groups)
        self.name = "A_Gun"

        self.damage = 10        # Урон от оружия
        self.fire_rate = 1000   # Скорострельность
        self.magazine = 30      # Размер обоймы

    def shoot(self):
        print(f"{self.name} fires, dealing {self.damage} damage!")


class Pistol(BasicItem):
    def __init__(self, game_groups_dict: dict, initial_groups: list):
        super().__init__(game_groups_dict, initial_groups)
        self.image = pygame.Surface((30, 10))
        self.gun_color = (0, 128, 255)
        self.image.fill(self.gun_color)
        self.rect = self.image.get_rect()

        self.name = "Pistol"

    def shoot(self):
        print(f"{self.name} fires, dealing {self.damage} damage!")


class SplashGun(BasicItem):
    def __init__(self, game_groups_dict: dict, initial_groups: list):
        super().__init__(game_groups_dict, initial_groups)
        self.image = pygame.Surface((30, 10))
        self.gun_color = (128, 128, 255)
        self.image.fill(self.gun_color)
        self.rect = self.image.get_rect()

        self.name = "SplashGun"


guns_settings_dict = {
    "pistol": [10,]
}
