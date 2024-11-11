# ./custom_sprites/guns_sprites.py:
import pygame


class BasicGun(pygame.sprite.Sprite):
    def __init__(self, initial_groups: list):
        super().__init__()
        for group in initial_groups:
            group.add(self, layer=9)

        # Базовые параметры
        self.damage = 10        # Урон от оружия
        self.fire_rate = 1000   # Скорострельность
        self.magazine = 30      # Размер обоймы
        self.name = "A_Gun"     # Название оружия

    def shoot(self):
        print(f"{self.name} fires, dealing {self.damage} damage!")

    def player_takes_gun(self):
        pass

    def follow_player(self):
        pass


class Pistol(BasicGun):
    def __init__(self, initial_groups):
        super().__init__(initial_groups)
        self.image = pygame.Surface((30, 10))
        self.gun_color = (0, 128, 255)
        self.image.fill(self.gun_color)
        self.rect = self.image.get_rect()

        self.name = "Pistol"


class SplashGun(BasicGun):
    def __init__(self, initial_groups):
        super().__init__(initial_groups)
        self.image = pygame.Surface((30, 10))
        self.gun_color = (128, 128, 255)
        self.image.fill(self.gun_color)
        self.rect = self.image.get_rect()

        self.name = "SplashGun"


guns_settings_dict = {
    "pistol": [10,]
}
