import pygame
import custom_funcs as cf
import game_constants as gc
import random

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
    def __init__(self, game_groups_dict: dict, initial_groups: list):
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
        self.rect.x = 100
        self.rect.y = 100

        self.speed = 200
        self.max_hp = 100
        self.hp_multiplier = 1
        self.hp = self.max_hp * self.hp_multiplier
        self.hp_bar = HpBar(game_groups_dict=self.game_groups_dict, owner=self)

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

# =============================================================== HP

    def take_damage(self, value):
        self.hp = max(0, self.hp - value)

    def add_hp(self, value):
        self.hp = min(self.max_hp * self.hp_multiplier, self.hp + value)

    def update_hp(self):
        if self.hp < 1:
            self.kill()
            self.hp_bar.kill()

# =============================================================== COLLISIONS

    def update(self, **kwargs):
        player = kwargs['player']
        self.update_hp()


class Skeleton(BasicEnemy):
    def __init__(self, game_groups_dict: dict, initial_groups: list):
        super().__init__(game_groups_dict=game_groups_dict, initial_groups=initial_groups)
