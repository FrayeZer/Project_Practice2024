# ./main.py
import pygame
import sys

import pygame.image
import game_constants as gc
import custom_funcs as cf

import custom_sprites.player_sprite as player_sprite
import custom_sprites.items_sprites as items_sprites
import custom_sprites.enemy_sprites as enemy_sprites
import custom_sprites.ui_sprites as ui_sprites

from ingame_processes import GameProcess, Level

IMG_MAIN_MENU = pygame.image.load("textures/main_menu_screen.png")
IMG_UI = pygame.image.load("textures/UI.png")


class Game:
    def __init__(self):
        pygame.init()
        # game, main_menu, pause_menu, lose_screen
        self.window = "main_menu"

        # Внутригровые процессы
        self.unit_types = {"Skeleton": enemy_sprites.Skeleton,
                           "Buyer": ui_sprites.Buyer,
                           "EnterDoor": ui_sprites.EnterDoor,
                           "ExitDoor": ui_sprites.ExitDoor,
                           "Upgrader": ui_sprites.Upgrader}
        self.level = Level(self)
        self.level.id = 0  # 0 - Safe зона; 1, 2, ..., n - айди
        self.levels_completed = 1
        self.game_process = GameProcess(self)

        # Настройка отображения окна приложения
        self.__apply_screen_settings()

        # Каждый спрайт должен быть добавлен в эту группу для отрисовки спрайтов
        # в правильном порядке. По умолчанию ставить layer=10 или менять при необходимости
        # Пример: self.displaying_objects_group.add(self.player, layer=10)
        self.all_sprites_group = pygame.sprite.Group()
        self.item_sprites_group = pygame.sprite.Group()
        self.displaying_objects_group = pygame.sprite.LayeredUpdates()

        # Соответствующие спрайты должны быть добавлены в соответствующие группы для обработки коллизий
        self.player_kit_group = pygame.sprite.Group()
        self.map_kit_group = pygame.sprite.Group()
        self.bullets_group = pygame.sprite.Group()
        self.units_group = pygame.sprite.Group()
        self.interactive_objects_group = pygame.sprite.Group()
        self.menus_group = pygame.sprite.Group()
        self.barriers_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()

        self.game_groups_dict = {
            "player_group": self.player_group,
            "all_sprites_group": self.all_sprites_group,
            "item_sprites_group": self.item_sprites_group,
            "player_kit_group": self.player_kit_group,
            "map_kit_group": self.map_kit_group,
            "displaying_objects_group": self.displaying_objects_group,
            "bullets_group": self.bullets_group,
            "units_group": self.units_group,
            "interactive_objects_group": self.interactive_objects_group,
            "menus_group": self.menus_group,
            "any_level_group": self.level.any_level_group,
            "barriers_group": self.barriers_group,
        }

        # Инициализация ключевых спрайтов или групп спрайтов
        self.__init_fonts()
        self.__init_player()
        self.__init_walls()
        self.__init_ui()
        # self.__add_guns_into_the_map()
        # self.__init_enemy()
        # self.__init_interactive_objects()

        first_gun = items_sprites.Pistol(game_groups_dict=self.game_groups_dict,
                                         initial_groups=["displaying_objects_group",
                                                         "all_sprites_group",
                                                         "map_kit_group",
                                                         "player_kit_group",
                                                         "item_sprites_group",
                                                         "any_level_group"])
        first_gun.set_owner(self.player)
        self.player.add_to_inventory(first_gun)

        self.game_process.change_level_to(0)

        # self.__draw_background()

    def __apply_screen_settings(self):
        self.screen_width = gc.SCREEN_WIDTH
        self.screen_height = gc.SCREEN_HEIGHT
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.fps_limit = gc.FPS_LIMIT

    # def __draw_background(self):
    #     self.screen.blit()

    def __init_fonts(self):
        self.fps_label = pygame.font.SysFont("Monocraft", 12)
        self.ammo_label = pygame.font.SysFont("Monocraft", 24)

    def __init_player(self):
        self.player = player_sprite.Player(game_groups_dict=self.game_groups_dict,
                                           initial_groups=["player_group",
                                                           "displaying_objects_group",
                                                           "all_sprites_group",
                                                           "map_kit_group",
                                                           "player_kit_group",
                                                           "units_group",],
                                           game=self)
        self.player.rect.center = (self.screen_width // 2,
                                   self.screen_height // 2)

    def __init_walls(self):
        self.top_wall = items_sprites.Barrier(game_groups_dict=self.game_groups_dict,
                                              size=(820, 20), pos=(40, 75))
        self.left_wall = items_sprites.Barrier(game_groups_dict=self.game_groups_dict,
                                               size=(20, 420), pos=(25, 85))
        self.bottom_wall = items_sprites.Barrier(game_groups_dict=self.game_groups_dict,
                                                 size=(820, 20), pos=(40, 505))
        self.right_wall = items_sprites.Barrier(game_groups_dict=self.game_groups_dict,
                                                size=(20, 420), pos=(860, 85))

    def __init_ui(self):

        self.wooden_bg_bar = ui_sprites.WoodenBgBar(game=self,
                                                    game_groups_dict=self.game_groups_dict,
                                                    initial_groups=["displaying_objects_group",
                                                                    "all_sprites_group",
                                                                    "menus_group"],
                                                    start_pos=[])

        self.pause_button = ui_sprites.PauseButton(game=self,
                                                    game_groups_dict=self.game_groups_dict,
                                                    initial_groups=["displaying_objects_group",
                                                                    "all_sprites_group",
                                                                    "menus_group"],
                                                    start_pos=[])
        self.player_hp_bar_bg = ui_sprites.PlayerHpBarBg(game=self,
                                                    game_groups_dict=self.game_groups_dict,
                                                    initial_groups=["displaying_objects_group",
                                                                    "all_sprites_group",
                                                                    "menus_group"],
                                                    start_pos=[])
        self.player_hp_bar = ui_sprites.PlayerHpBar(game=self,
                                                    game_groups_dict=self.game_groups_dict,
                                                    initial_groups=["displaying_objects_group",
                                                                    "all_sprites_group",
                                                                    "menus_group"],
                                                    start_pos=[])


# ========================================================== GAME


    def get_next_level_id(self):
        return self.level.id + self.levels_completed

    def get_level_id(self):
        return self.level.id

    def change_level(self, level_id: int):
        self.game_process.change_level_to(level_id)

    def create_level(self, level):
        pass


# ========================================================== UPDATE


    def draw_fps(self):
        fps_text = self.fps_label.render(
            f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))

    def draw_ammo_count(self):
        player_active_item = self.player.active_slot
        if isinstance(player_active_item, items_sprites.Gun):
            if player_active_item._get_flag("is_reloading_now") == False:
                text = f"{
                    player_active_item.shots_left}/{player_active_item.ammo}"
            else:
                text = "Reloading"
            ammo_text = self.ammo_label.render(text, True, (255, 255, 255))
            self.screen.blit(
                ammo_text, (self.screen_width - (len(text) * 20), self.screen_height - 50))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type >= pygame.USEREVENT:
                event_id = event.type - pygame.USEREVENT
                # Обработка событий с ограничением по количеству вызовов за `time` секунд
                if event_id in cf.get_forbidden_events():
                    cf.remove_forbidden_event(event_id)

                # Обработка событий с отложенным вызовом
                elif event_id in cf.get_delayed_events():
                    kwargs = cf.get_delayed_event(event_id)[1]
                    cf.get_delayed_event(event_id)[0](**kwargs)
                    cf.remove_delayed_event(event_id)

                # if event_id == gc.CUSTOM_EVENTS_IDS["level_started_event"]:
                #     self.change_level(self.get_next_level_id())
                #     print(f"level {self.level.id} started")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.process_mouse(
                    button_id=event.button, pressed_unpressed=True)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.player.process_mouse(
                    button_id=event.button, pressed_unpressed=False)

    def update(self) -> None:
        self.all_sprites_group.update(
            keys_pressed=pygame.key.get_pressed(),
            player=self.player,
            game=self)
        self.level.update()

    def render(self) -> None:
        self.screen.fill((0, 0, 0))
        self.displaying_objects_group.draw(self.screen)
        # self.draw_fps()
        self.draw_menu(self.window)
        pygame.display.flip()
        self.clock.tick(self.fps_limit)

    def draw_menu(self, window) -> None:
        if window == "game":
            self.draw_ammo_count()
        if window == "main_menu":
            self.screen.blit(IMG_MAIN_MENU, (0, 0))
        if window == "lose_screen":
            pass

    def process_menu(self):
        if self.window == "main_menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.window = "game"
        elif self.window == "game":
            pass

    def run(self):
        while True:
            if self.window == "game":
                self.update()
                self.handle_events()
            self.render()
            self.process_menu()


if __name__ == "__main__":
    game = Game()
    game.run()
