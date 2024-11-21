# ./main.py
import pygame
import sys
import game_constants
import custom_funcs

import custom_sprites.player_sprite as player_sprite
import custom_sprites.items_sprites as items_sprites
import custom_sprites.enemy_sprites as enemy_sprites
import custom_sprites.ui_sprites as ui_sprites


class Game:
    def __init__(self):
        pygame.init()
        # Настройка отображения окна приложения
        self.__apply_screen_settings()

        # Каждый спрайт должен быть добавлен в эту группу для отрисовки спрайтов
        # в правильном порядке. По умолчанию ставить layer=10 или менять при необходимости
        # Пример: self.all_sprites_group.add(self.player, layer=10)
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

        self.game_groups_dict = {
            "all_sprites_group": self.all_sprites_group,
            "item_sprites_group": self.item_sprites_group,
            "player_kit_group": self.player_kit_group,
            "map_kit_group": self.map_kit_group,
            "displaying_objects_group": self.displaying_objects_group,
            "bullets_group": self.bullets_group,
            "units_group": self.units_group,
            "interactive_objects_group": self.interactive_objects_group,
            "menus_group": self.menus_group,
        }

        # Инициализация ключевых спрайтов или групп спрайтов
        self.__init_fonts()
        self.__init_player()
        self.__add_guns_into_the_map()
        self.__init_enemy()
        self.__init_interactive_objects()

    def __apply_screen_settings(self):
        self.screen_width = game_constants.SCREEN_WIDTH
        self.screen_height = game_constants.SCREEN_HEIGHT
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.fps_limit = game_constants.FPS_LIMIT

    def __init_fonts(self):
        self.fps_label = pygame.font.SysFont("Times New Roman", 24)

    def __init_player(self):
        self.player = player_sprite.Player(game_groups_dict=self.game_groups_dict,
                                           initial_groups=["displaying_objects_group",
                                                           "all_sprites_group",
                                                           "map_kit_group",
                                                           "player_kit_group",
                                                           "units_group"])
        self.player.rect.center = (self.screen_width // 2,
                                   self.screen_height // 2)
        # ...

    def __init_enemy(self):
        self.skeleton = enemy_sprites.Skeleton(game_groups_dict=self.game_groups_dict,
                                               initial_groups=["displaying_objects_group",
                                                               "all_sprites_group",
                                                               "map_kit_group",
                                                               "units_group"])

    def __add_guns_into_the_map(self):
        self.pistol = items_sprites.Pistol(game_groups_dict=self.game_groups_dict,
                                           initial_groups=["displaying_objects_group",
                                                           "all_sprites_group",
                                                           "map_kit_group",
                                                           "item_sprites_group"])
        self.pistol.set_owner(self.player)
        self.pistol.rect.center = (
            self.screen_width // 2, self.screen_height // 2)

    def __init_interactive_objects(self):
        self.upgrader = ui_sprites.Upgrader(
            game_groups_dict=self.game_groups_dict)

    def draw_fps(self):
        fps_text = self.fps_label.render(
            f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))

    def draw_ammo_count(self):
        player_active_item = self.player.active_slot
        if isinstance(player_active_item, items_sprites.Gun):
            if player_active_item._get_flag("is_reloading_now") == False:
                text = f"{
                    player_active_item.shots_left} / {player_active_item.ammo}"
            else:
                text = "Reloading"
            ammo_text = self.fps_label.render(text, True, (255, 255, 255))
            self.screen.blit(
                ammo_text, (self.screen_width - (len(text) * 15), self.screen_height - 50))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type >= pygame.USEREVENT:
                event_id = event.type - pygame.USEREVENT
                # Обработка событий с ограничением по количеству вызовов за `time` секунд
                if event_id in custom_funcs.get_forbidden_events():
                    custom_funcs.remove_forbidden_event(event_id)

                # Обработка событий с отложенным вызовом
                elif event_id in custom_funcs.get_delayed_events():
                    kwargs = custom_funcs.get_delayed_event(event_id)[1]
                    custom_funcs.get_delayed_event(event_id)[0](**kwargs)
                    custom_funcs.remove_delayed_event(event_id)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.process_mouse(
                    button_id=event.button, pressed_unpressed=True)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.player.process_mouse(
                    button_id=event.button, pressed_unpressed=False)

    def update(self):
        self.all_sprites_group.update(
            keys_pressed=pygame.key.get_pressed(),
            player=self.player)

        # for l in self.game_groups_dict["displaying_objects_group"].layers():
        #     f = self.game_groups_dict["displaying_objects_group"].get_sprites_from_layer(l)
        #     for s in f:
        #         try:
        #             print(s.name, end= ' ')
        #         except Exception:
        #             pass
        #         print(s, l)

    def render(self):
        self.screen.fill((0, 0, 0))
        self.displaying_objects_group.draw(self.screen)
        self.draw_fps()
        self.draw_ammo_count()
        pygame.display.flip()
        self.clock.tick(self.fps_limit)

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()


if __name__ == "__main__":
    game = Game()
    game.run()
