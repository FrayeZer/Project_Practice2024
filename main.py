import pygame
import sys
import game_constants

import custom_sprites

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
        self.player = custom_sprites.Player(
            self.screen_width, self.screen_height)
        self.all_sprites.add(self.player, layer=10)
        # ...

    def draw_fps(self):
        fps_text = self.fps_label.render(
            f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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
