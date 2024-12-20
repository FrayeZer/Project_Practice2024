import pygame
import pygame.locals
import game_constants as gc
import custom_funcs as cf


class GameProcess():
    def __init__(self, game):
        self.game = game

    def change_level_to(self, level_id):
        self.game.level.kill_current_level_sprites()
        self.game.level.id = level_id
        self.game.level.wave = 1
        self.game.level.update_json()
        self.game.level.add_level_sprites()
        if level_id != 0:
            self.teleport_player((430, 400))
        else:
            self.teleport_player((430, 130))
        self.game.level.add_map_image()

    def teleport_player(self, pos):
        self.game.player.rect.x = pos[0]
        self.game.player.rect.y = pos[1]


class Level():
    def __init__(self, game):
        self.game = game
        self.id = 0
        self.wave = 1
        self.wave_count = 1
        self.enemy_left = 1
        self.any_level_group = pygame.sprite.Group()
        self.enemies = None
        self.initialised_sprites = None
        self.json = None
        self.is_level_ended = False

    def add_map_image(self):
        self.map_image_sprite = pygame.sprite.Sprite()
        self.map_image_sprite.image = pygame.image.load(
            f"levels/level{self.id}/map_image.png")
        self.map_image_sprite.rect = self.map_image_sprite.image.get_rect()
        self.map_image_sprite.rect.x = 0
        self.map_image_sprite.rect.y = 0
        groups = ["all_sprites_group",
                  "map_kit_group",
                  "displaying_objects_group",
                  "any_level_group"]
        cf.add_SELF_to_groups(object=self.map_image_sprite,
                              game_groups_dict=self.game.game_groups_dict,
                              including_groups=groups,
                              layer=0)

    def kill_current_level_sprites(self):
        for sprite in self.any_level_group:
            sprite.kill()
        for sprite in self.game.game_groups_dict["bullets_group"]:
            sprite.kill()

    def add_level_sprites(self):
        initial_groups = ["displaying_objects_group",
                          "all_sprites_group",
                          "map_kit_group",
                          "units_group",
                          "any_level_group"]

        self.initialised_sprites = [self.game.unit_types[unit](game=self.game, game_groups_dict=self.game.game_groups_dict, initial_groups=initial_groups, start_pos=start_pos)
                                    for unit in self.json[f"wave_{self.wave}"]["units"] for start_pos in self.json[f"wave_{self.wave}"]["units"][unit]]
        self.enemies = [sprite for sprite in self.initialised_sprites if sprite
                        not in self.game.game_groups_dict["interactive_objects_group"]]
        # print(self.enemies)

    def update_json(self):
        self.json = cf.read_json(f"levels/level{self.id}/level{self.id}.json")
        self.wave_count = int(self.json["wave_count"])

    def count_enemies(self):
        enemy_left = 0
        for unit in self.enemies:
            if unit._is_object_displaying():
                enemy_left += 1
        self.enemy_left = enemy_left

    def next_wave(self):
        if self.wave + 1 <= self.wave_count:
            self.wave += 1
            self.add_level_sprites()
        else:
            if self.is_level_ended == False:
                self.end()

    def end(self):
        print(123)
        self.is_level_ended = True
        self.game.unit_types["ExitDoor"](game=self.game,
                                         game_groups_dict=self.game.game_groups_dict,
                                         initial_groups=None, start_pos=None)

    def set_level_ended(self, bool_value: bool):
        if self.is_level_ended != bool_value:
            self.is_level_ended = bool_value

    def update(self):
        self.count_enemies()
        if self.enemy_left < 1:
            if self.id != 0:
                self.next_wave()
        # self.set_level_ended(False)
