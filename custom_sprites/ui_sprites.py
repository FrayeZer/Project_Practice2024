import pygame

from custom_funcs import add_SELF_to_groups
import game_constants as gc


class Upgrader(pygame.sprite.Sprite):
    def __init__(self, game_groups_dict):
        super().__init__()
        self.name = "Upgrader"
        self.game_groups_dict = game_groups_dict
        self.init_groups = ["all_sprites_group",
                            "map_kit_group",
                            "displaying_objects_group",
                            "interactive_objects_group"]
        add_SELF_to_groups(self, self.game_groups_dict,
                           self.init_groups, layer=13)

        self.image = pygame.Surface((40, 80))
        self.image.fill((128, 0, 128))
        self.rect = self.image.get_rect()

        self.rect.x = 50
        self.rect.y = gc.SCREEN_HEIGHT / 2 - self.image.get_height() / 2


class UpgraderMenu(pygame.sprite.Sprite):
    def __init__(self, game_groups_dict):
        super().__init__()
        self.name = "UpgraderMenu"
        self.init_groups = ["all_sprites_group",
                            "displaying_objects_group",
                            "menus_group"]
        add_SELF_to_groups(self, self.game_groups_dict,
                           self.init_groups, layer=14)


class Buyer(pygame.sprite.Sprite):
    def __init__(self, game_groups_dict):
        super().__init__()
        self.name = "Upgrader"
        self.game_groups_dict = game_groups_dict
        self.init_groups = ["all_sprites_group",
                            "map_kit_group",
                            "displaying_objects_group",
                            "interactive_objects_group"]
        add_SELF_to_groups(self, self.game_groups_dict,
                           self.init_groups, layer=13)

        self.image = pygame.Surface((40, 80))
        self.image.fill((128, 0, 128))
        self.rect = self.image.get_rect()

        self.rect.x = 50
        self.rect.y = gc.SCREEN_HEIGHT / 2 - self.image.get_height() / 2
