import pygame
import custom_funcs
import game_constants
import random

from custom_funcs import add_SELF_to_groups


class HpBar(pygame.sprite.Sprite):
    def __init__(self, game_groups_dict: dict, owner: pygame.sprite.Sprite):
        super().__init__()
        self.game_groups_dict = game_groups_dict
        self.initial_groups = ["all_sprites_group",
                               "map_kit_group",
                               "displaying_objects_group"]
        add_SELF_to_groups(self, self.game_groups_dict,
                           self.initial_groups, 12)

        self.owner = owner
        self.image = pygame.Surface((40, 10))
        self.image.fill((128, 64, 64))
        pygame.draw.rect(self.image, (255, 64, 64), (2, 2, 36, 6))
        self.rect = self.image.get_rect()

    def update(self, **kwargs):
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
