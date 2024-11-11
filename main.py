# ./main.py
import pygame
import sys
import game_constants
import custom_funcs

import custom_sprites.player_sprite as player_sprite
import custom_sprites.guns_sprites as guns_sprites


class Game:
    def __init__(self):
        pygame.init()
        # Настройка отображения окна приложения
        self.__apply_screen_settings()

        # Каждый спрайт должен быть добавлен в эту группу для отрисовки спрайтов
        # в правильном порядке. По умолчанию ставить layer=10 или менять при необходимости
        # Пример: self.all_sprites.add(self.player, layer=10)
        self.all_sprites = pygame.sprite.LayeredUpdates()

        # Соответствующие спрайты должны быть добавлены в соответствующие группы для обработки коллизий
        self.player_kit = pygame.sprite.LayeredUpdates()
        self.map_kit = pygame.sprite.LayeredUpdates()

        # Инициализация ключевых спрайтов или групп спрайтов
        self.__init_fps_display()
        self.__init_player()
        self.__add_guns_into_the_map()

    def __apply_screen_settings(self):
        self.screen_width = game_constants.SCREEN_WIDTH
        self.screen_height = game_constants.SCREEN_HEIGHT
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.fps_limit = game_constants.FPS_LIMIT

    def __init_fps_display(self):
        self.fps_label = pygame.font.SysFont("Times New Roman", 24)

    def __init_player(self):
        self.player = player_sprite.Player(initial_groups=[self.all_sprites,
                                                           self.map_kit, self.player_kit])
        self.player.rect.center = (self.screen_width // 2,
                                   self.screen_height // 2)
        # ...

    def __add_guns_into_the_map(self):
        self.pistol = guns_sprites.Pistol(initial_groups=[self.all_sprites,
                                                          self.map_kit])
        self.pistol.rect.center = (
            self.screen_width // 2, self.screen_height // 2)

    def draw_fps(self):
        fps_text = self.fps_label.render(
            f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))

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
                elif event_id in custom_funcs.get_delayed_event():
                    args = custom_funcs.get_delayed_event[event_id][1]
                    custom_funcs.get_delayed_event[event_id][0](*args)
                    custom_funcs.remove_delayed_event(event_id)

    def update(self):
        self.all_sprites.update(pygame.key.get_pressed())

    def render(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        self.draw_fps()
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
