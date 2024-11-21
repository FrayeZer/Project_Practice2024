import pygame
import game_constants as gc
import custom_funcs as cf

from custom_funcs import add_SELF_to_groups


class Ui(pygame.sprite.Sprite):
    def __init__(self, game_groups_dict):
        super().__init__()
        self.name = "Ui"
        self.game_groups_dict = game_groups_dict

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


class Upgrader(Ui):
    def __init__(self, game_groups_dict):
        super().__init__(game_groups_dict)
        self.name = "Upgrader"
        self.game_groups_dict = game_groups_dict
        self.init_groups = ["all_sprites_group",
                            "map_kit_group",
                            "displaying_objects_group",
                            "interactive_objects_group",
                            "zero_level_group"]
        add_SELF_to_groups(self, self.game_groups_dict,
                           self.init_groups, layer=13)

        self.image = pygame.Surface((40, 80))
        self.image.fill((128, 0, 128))
        self.rect = self.image.get_rect()

        self.rect.x = 50
        self.rect.y = gc.SCREEN_HEIGHT / 2 - self.image.get_height() / 2

    def open(self, **kwargs):
        player = kwargs["player"]
        print("Открытие апгрейдера")

    def close(self, **kwargs):
        player = kwargs["player"]
        print("Закрытие апгрейдера")


class UpgraderMenu(Ui):
    def __init__(self, game_groups_dict):
        super().__init__(game_groups_dict)
        self.name = "UpgraderMenu"
        self.init_groups = ["all_sprites_group",
                            "displaying_objects_group",
                            "menus_group",
                            "zero_level_group"]
        add_SELF_to_groups(self, self.game_groups_dict,
                           self.init_groups, layer=14)


class Buyer(Ui):
    def __init__(self, game_groups_dict):
        super().__init__(game_groups_dict)
        self.name = "Buyer"
        self.game_groups_dict = game_groups_dict
        self.init_groups = ["all_sprites_group",
                            "map_kit_group",
                            "displaying_objects_group",
                            "interactive_objects_group",
                            "zero_level_group"]
        add_SELF_to_groups(self, self.game_groups_dict,
                           self.init_groups, layer=13)

        self.image = pygame.Surface((40, 80))
        self.image.fill((128, 64, 128))
        self.rect = self.image.get_rect()

        self.rect.x = gc.SCREEN_WIDTH - 50 - self.image.get_width()
        self.rect.y = gc.SCREEN_HEIGHT / 2 - self.image.get_height() / 2

    def open(self, **kwargs):
        player = kwargs["player"]
        print("Открытие скупщика")

    def close(self, **kwargs):
        player = kwargs["player"]
        print("Закрытие скупщика")


class Door(Ui):
    def __init__(self, game_groups_dict):
        super().__init__(game_groups_dict)
        self.name = "Door"
        self.game_groups_dict = game_groups_dict
        self.init_groups = ["all_sprites_group",
                            "map_kit_group",
                            "displaying_objects_group",
                            "interactive_objects_group",
                            "zero_level_group"]
        add_SELF_to_groups(self, self.game_groups_dict,
                           self.init_groups, layer=13)

        self.image = pygame.Surface((80, 20))
        self.image.fill((255, 64, 64))
        self.rect = self.image.get_rect()

        self.rect.x = gc.SCREEN_WIDTH / 2 - self.image.get_width() / 2
        self.rect.y = 40

    def open(self, **kwargs):
        player = kwargs["player"]
        cf.delayed_activating(id=gc.CUSTOM_EVENTS_IDS["open_door_event"],
                              delay=1000,
                              function=player._change_flag,
                              flag="can_move",
                              bool_value=True)
        pygame.time.set_timer(pygame.USEREVENT + gc.CUSTOM_EVENTS_IDS["level_started_event"],
                              millis=1,
                              loops=1)

    def close(self, **kwargs):
        player = kwargs["player"]
        print("Закрытие ДВЕРИ!")
