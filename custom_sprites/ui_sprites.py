import pygame
import game_constants as gc
import custom_funcs as cf

from custom_funcs import add_SELF_to_groups
IMG_UI = pygame.image.load("textures/UI.png")


class Ui(pygame.sprite.Sprite):
    def __init__(self, game, game_groups_dict: dict, initial_groups, start_pos):
        self.game = game
        super().__init__()
        self.displaying_layer = 10
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


class Upgrader(Ui):
    def __init__(self, game, game_groups_dict, initial_groups, start_pos):
        self.game = game
        super().__init__(game, game_groups_dict, initial_groups, start_pos)
        self.name = "Upgrader"
        self.game_groups_dict = game_groups_dict
        self.initial_groups = ["all_sprites_group",
                               "map_kit_group",
                               "displaying_objects_group",
                               "interactive_objects_group",
                               "any_level_group"]
        self.displaying_layer = 13
        add_SELF_to_groups(self, self.game_groups_dict,
                           self.initial_groups, layer=self.displaying_layer)

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
    def __init__(self, game, game_groups_dict):
        self.game = game
        super().__init__(game, game_groups_dict)
        self.name = "UpgraderMenu"
        self.initial_groups = ["all_sprites_group",
                               "displaying_objects_group",
                               "menus_group",
                               "any_level_group"]
        self.displaying_layer = 14
        add_SELF_to_groups(self, self.game_groups_dict,
                           self.initial_groups, layer=self.displaying_layer)


class Buyer(Ui):
    def __init__(self, game, game_groups_dict, initial_groups, start_pos: list):
        self.game = game
        super().__init__(game, game_groups_dict, initial_groups, start_pos)
        self.name = "Buyer"
        self.game_groups_dict = game_groups_dict
        self.initial_groups = ["all_sprites_group",
                               "map_kit_group",
                               "displaying_objects_group",
                               "interactive_objects_group",
                               "any_level_group"]
        self.displaying_layer = 13
        add_SELF_to_groups(self, self.game_groups_dict,
                           self.initial_groups, layer=self.displaying_layer)

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
    def __init__(self, game, game_groups_dict, initial_groups, start_pos):
        self.game = game
        super().__init__(game, game_groups_dict, initial_groups, start_pos)

        self.name = "Door"
        self.game_groups_dict = game_groups_dict
        self.initial_groups = ["all_sprites_group",
                               "map_kit_group",
                               "displaying_objects_group",
                               "interactive_objects_group",
                               "any_level_group"]
        self.displaying_layer = 13
        add_SELF_to_groups(self, self.game_groups_dict,
                           self.initial_groups, layer=self.displaying_layer)


class EnterDoor(Door):
    def __init__(self, game, game_groups_dict, initial_groups, start_pos):
        self.game = game
        super().__init__(game, game_groups_dict, initial_groups, start_pos)
        self.image = pygame.Surface((80, 20))
        self.image.fill((255, 64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = gc.SCREEN_WIDTH / 2 - self.image.get_width() / 2
        self.rect.y = 85

    def open(self, **kwargs):
        print("ENTER")
        player = kwargs["player"]
        cf.delayed_activating(id=gc.CUSTOM_EVENTS_IDS["open_door_event"],
                              delay=500,
                              function=player._change_flag,
                              flag="can_move",
                              bool_value=True)
        # pygame.time.set_timer(pygame.USEREVENT + gc.CUSTOM_EVENTS_IDS["level_started_event"],
        #                       millis=1,
        #                       loops=1)
        self.game.change_level(self.game.get_next_level_id())
        print(f"level {self.game.level.id} started")


class ExitDoor(Door):
    def __init__(self, game, game_groups_dict, initial_groups, start_pos):
        self.game = game
        super().__init__(game, game_groups_dict, initial_groups, start_pos)
        self.image = pygame.Surface((80, 20))
        self.image.fill((255, 64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = gc.SCREEN_WIDTH / 2 - self.image.get_width() / 2
        self.rect.y = 500

    def open(self, **kwargs):
        print("EXIT")
        player = kwargs["player"]
        game = kwargs["game"]
        cf.delayed_activating(id=gc.CUSTOM_EVENTS_IDS["return_to_zero_level_event"],
                              delay=500,
                              function=player._change_flag,
                              flag="can_move",
                              bool_value=True)
        game.change_level(0)
        game.levels_completed += 1
        game.level.set_level_ended(False)


class InventotyCell(Ui):
    def __init__(self, game, game_groups_dict, item, index):
        self.game = game
        start_pos = ()
        initial_groups = ["all_sprites_group",
                          "player_kit_group",
                          "displaying_objects_group",
                          "menus_group"]
        super().__init__(game, game_groups_dict, initial_groups, start_pos)
        self.player = game_groups_dict["player_group"].sprites()[0]
        self.index = index
        self.displaying_layer = 14
        self.game_groups_dict = game_groups_dict
        self.initial_groups = initial_groups
        add_SELF_to_groups(self, self.game_groups_dict,
                           self.initial_groups, layer=self.displaying_layer)

        temp_active_bg_image = cf.cut_image(IMG_UI, (19, 0), (19, 20))
        width, height = temp_active_bg_image.get_size()
        self.active_bg_image = pygame.transform.scale(
            temp_active_bg_image, (width * 3, height * 3))

        temp_passive_bg_image = cf.cut_image(IMG_UI, (0, 0), (19, 20))
        width, height = temp_passive_bg_image.get_size()
        self.passive_bg_image = pygame.transform.scale(
            temp_passive_bg_image, (width * 3, height * 3))

        self.bg = self.passive_bg_image

        self.item = item
        self.item_image = self.item.original_image

        self.image = pygame.Surface((56, 56), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = 340 + 55 * self.index
        self.rect.y = 535

    def update_texture(self):
        self.item = self.player.inventory.items[self.index]
        self.item_image = self.item.original_image

        if self.index == self.player.active_slot_index:
            self.bg = self.active_bg_image
        else:
            self.bg = self.passive_bg_image

        item_width, item_height = self.item_image.get_size()
        self.image.blit(self.bg, (0, 0))
        self.image.blit(
            self.item_image, ((57 - item_width) // 2, item_height // 2))

    # def update(self, *args, **kwargs):
    #     self.player = kwargs["player"]


class Inventory():
    def __init__(self, game, game_groups_dict, initial_items: list):
        self.game = game
        self.items = initial_items
        self.game_groups_dict = game_groups_dict

        self.cells = [InventotyCell(game=self.game,
                                    item=self.items[i],
                                    game_groups_dict=self.game_groups_dict,
                                    index=i)
                      for i in range(4)]

    def update(self):  # Не каждый кадр!
        for cell in self.cells:
            cell.update_texture()


class PlayerHpBarBg(Ui):
    def __init__(self, game, game_groups_dict, initial_groups, start_pos):
        super().__init__(game, game_groups_dict, initial_groups, start_pos)
        self.image = cf.cut_image(
            IMG_UI, (59, 1), (52, 13), scale=3)
        self.rect = self.image.get_rect()
        self.rect.center = (100, 563)
        cf.add_SELF_to_groups(object=self,
                              game_groups_dict=self.game_groups_dict,
                              including_groups=initial_groups,
                              layer=14)


class PlayerHpBar(Ui):
    def __init__(self, game, game_groups_dict, initial_groups, start_pos):
        super().__init__(game, game_groups_dict, initial_groups, start_pos)
        self.image = cf.cut_image(
            IMG_UI, (113, 1), (48, 9), scale=3)
        self.rect = self.image.get_rect()
        self.rect.center = (100, 563)
        cf.add_SELF_to_groups(object=self,
                              game_groups_dict=self.game_groups_dict,
                              including_groups=initial_groups,
                              layer=15)

    def update(self, **kwargs):
        x = 113 + (52 - 52 * (self.game.player.hp / self.game.player.max_hp))
        xx = 52 * (self.game.player.hp / self.game.player.max_hp)
        self.image = cf.cut_image(
            IMG_UI, (x, 1), (xx, 13), scale=3)


class WoodenBgBar(Ui):
    def __init__(self, game, game_groups_dict, initial_groups, start_pos):
        super().__init__(game, game_groups_dict, initial_groups, start_pos)
        self.image = cf.cut_image(
            IMG_UI, (1, 21), (200, 16), scale=4.5)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 527
        cf.add_SELF_to_groups(object=self,
                              game_groups_dict=self.game_groups_dict,
                              including_groups=initial_groups,
                              layer=13)


class PauseButton(Ui):
    def __init__(self, game, game_groups_dict, initial_groups, start_pos):
        super().__init__(game, game_groups_dict, initial_groups, start_pos)
        self.image = cf.cut_image(
            IMG_UI, (39, 1), (18, 18), scale=3)
        self.rect = self.image.get_rect()
        self.rect.x = 15
        self.rect.y = 15
        cf.add_SELF_to_groups(object=self,
                              game_groups_dict=self.game_groups_dict,
                              including_groups=initial_groups,
                              layer=14)
