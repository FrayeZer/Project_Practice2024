import pygame
import game_constants


class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()

        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)

        self.movement_speed = 200  # Скорость движения игрока в пикселах в секунду

    def update(self, keys_pressed):
        keys = keys_pressed

        # Вычисляем движения по осям X и Y
        move_x = 0
        move_y = 0

        if keys[pygame.K_a]:  # Нажата клавиша 'A' (влево)
            move_x = -self.movement_speed
        if keys[pygame.K_d]:  # Нажата клавиша 'D' (вправо)
            move_x = self.movement_speed
        if keys[pygame.K_w]:  # Нажата клавиша 'W' (вверх)
            move_y = -self.movement_speed
        if keys[pygame.K_s]:  # Нажата клавиша 'S' (вниз)
            move_y = self.movement_speed

        if keys[pygame.K_LSHIFT]:
            move_x = move_x * 1.5
            move_y = move_y * 1.5

        # Если движение происходит по диагонали, нормализуем скорость
        if move_x != 0 and move_y != 0:
            # Нормализуем движение по диагонали
            slowdown_ratio = 1.3
            move_x = move_x / slowdown_ratio
            move_y = move_y / slowdown_ratio

        # Обновляем позицию
        self.rect.x += move_x / game_constants.FPS_LIMIT
        self.rect.y += move_y / game_constants.FPS_LIMIT
