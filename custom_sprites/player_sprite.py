import pygame
import game_constants as gc
import custom_sprites.items_sprites as items_sprites
import custom_funcs as cf
import custom_sprites.ui_sprites as ui_sprites
from custom_funcs import key_pressed, any_key_pressed, add_SELF_to_groups


class Player(pygame.sprite.Sprite):
    '''Основной класс игрока'''

    def __init__(self, game_groups_dict: dict, initial_groups: list, game):
        '''game_groups_dict - словарь всех групп игры
           initial_groups - начальные группы, в которые игрок будет добавлен'''
        super().__init__()
        self.game = game
        self.game_groups_dict = game_groups_dict
        self.initial_groups_names = initial_groups
        self.displaying_layer = 10
        add_SELF_to_groups(self, game_groups_dict,
                           initial_groups, layer=self.displaying_layer)
        image = pygame.image.load("textures/player.png")
        self.image = image
        self.rect = self.image.get_rect()

        # Инициализация статистик игрока
        self.speed_multiplier = 1  # Множитель скорости
        self.hp_multiplier = 1  # Множитель максимального уровня здоровья

        self.stamina = 100
        self.max_hp = 100
        self.hp = self.max_hp * self.hp_multiplier
        # Скорость движения игрока в пикселах в секунду
        self.movement_speed = 200 * self.speed_multiplier
        self.damage_multiplier = 10  # Множитель наносимого урона

        # Инициализация инвентаря игрока (дублируется несколько предметов)
        basic_item = items_sprites.BasicItem(game_groups_dict=self.game_groups_dict,
                                             initial_groups=["all_sprites_group",
                                                             "player_kit_group"])
        basic_item.set_owner(self)

        self.inventory = ui_sprites.Inventory(game=self.game, game_groups_dict=self.game_groups_dict,
                                              initial_items=[basic_item.deepcopy() for _ in range(4)])
        self.equipment = [basic_item.deepcopy()
                          for _ in range(2)]  # Для шлема и ботинок

        self.active_slot_index = 0
        self.active_slot = self.inventory.items[self.active_slot_index]

        # Список предметов, которые игрок может получить
        # только объекты из следующего списка классов можно (не принудительно) получить в инвентарь
        self.unlocked_items = [items_sprites.Pistol]
        self.sprint_event_id = gc.CUSTOM_EVENTS_IDS['sprint_event']
        self.add_stamina_event_id = gc.CUSTOM_EVENTS_IDS['add_stamina_event']
        self.restore_stamina_by_time_event_id = gc.CUSTOM_EVENTS_IDS[
            "restore_stamina_by_time_event"]
        self._flags = {
            "can_restore_stamina_by_time": True,
            "can_shoot": True,
            "can_move": True,
            "can_move_up": True,
            "can_move_down": True,
            "can_move_left": True,
            "can_move_right": True,
        }
        self._status = {
            "moving": False,
            "sprint": False,
            "idle": True,
            "attack": False,
        }

        self._opened_menus = {
            "Upgrader": False,
            "Buyer": False,
        }

        self.level_id = 0
        self.TEST_VALUE = 0
        self.balance = 0

# =============================================================== FLAGS

    def _is_object_displaying(self) -> bool:
        return self in self.game_groups_dict["displaying_objects_group"]

    def _change_flag(self, flag: str, bool_value):
        '''Меняет флаг в словаре _flags.
           Устанавливает флаг в указанное значение'''
        self._flags[flag] = bool_value

    def _get_flag(self, flag_name):
        '''Возвращает текущее значение флага по имени из словаря _flags.'''
        return self._flags[flag_name]

    def _is_menu_opened(self, menu):
        return self._opened_menus[menu]

    def _set_menu_opened(self, menu, flag):
        self._opened_menus[menu] = flag

# =============================================================== STATUSES

    def _set_player_status(self, status_name: str, value: bool):
        '''Меняет статус игрока в словаре _status, если текущий статус отличается от нового.'''
        if not self._status[status_name] == value:
            self._status[status_name] = value

    def status_idle(self):
        '''Функция для обработки статуса игрока "idle" (неактивен).'''
        if self._status["idle"]:
            if self._status["moving"]:
                cf.INTERRUPT_ERROR(1)
            pass
        else:
            pass

    def status_moving(self):
        '''Функция для обработки статуса игрока "moving" (движется).'''
        if self._status["moving"]:
            pass
        else:
            pass

    def status_sprint(self):
        '''Функция для обработки статуса игрока "sprint" (спринт).'''
        if self._status["sprint"]:
            pass
        else:
            pass

    def status_attack(self):
        '''Функция для обработки статуса игрока "attack" (атакует).'''
        if self._status["attack"]:
            pass
        else:
            pass

# =============================================================== HP

    def take_damage(self, value):
        self.hp = max(0, self.hp - value)

    def add_hp(self, value):
        self.hp = min(self.max_hp * self.hp_multiplier, self.hp + value)


# =============================================================== STAMINA


    def spend_stamina(self, value):
        '''Потратить стамину игрока. 
           Если достаточно стамины, уменьшает значение.
           Запускает восстановление стамины через 2000 мс.'''
        cf.delayed_activating(
            id=self.add_stamina_event_id,
            delay=2000,
            function=self._change_flag,
            flag="can_restore_stamina_by_time",
            bool_value=True)

        if self.stamina - value >= 0:
            self.stamina -= value
            if self._get_flag("can_restore_stamina_by_time"):
                self._change_flag("can_restore_stamina_by_time", False)

    def restore_stamina_by_time(self):
        '''Функция для восстановления стамины игрока со временем.'''
        if self._get_flag("can_restore_stamina_by_time"):
            cf.activate_with_temp_forbid(
                id=self.restore_stamina_by_time_event_id,
                delay=125,
                function=self.add_stamina,
                value=4)

    def add_stamina(self, value):
        '''Добавляет стамину, не превышая максимального значения 100.'''
        self.stamina = min(100, self.stamina + value)

    def get_stamina(self):
        return self.stamina


# =============================================================== ITEMS & INVENTORY

    def take_item(self):
        '''Подобрать предмет, если он находится в группе item_sprites_group и еще не в экипировке игрока.'''
        first_collided_gun = pygame.sprite.spritecollideany(
            self, self.game_groups_dict["item_sprites_group"])

        # Проверяет, является ли объект объектом класса BasicItem
        # и есть ли он у игрока в экипировке
        if isinstance(first_collided_gun, items_sprites.BasicItem) and \
                not first_collided_gun in self.game_groups_dict["player_kit_group"]:
            self.game_groups_dict["player_kit_group"].add(first_collided_gun)
            copy_of_item = first_collided_gun.deepcopy()
            self.add_to_inventory(copy_of_item)
            first_collided_gun.kill()

    def _inventory_free_space(self):
        '''Возвращает количество свободных слотов в инвентаре (где есть предметы типа BasicItem).'''
        count = 0
        for item in self.inventory.items:
            if item.__class__ == items_sprites.BasicItem:
                count += 1
        return count

    def _is_item_unlocked(self, item):
        '''Проверяет, разблокирован ли предмет в списке unlocked_items.'''
        flag = False
        for iter_item in self.unlocked_items:
            if iter_item == item.__class__:
                flag = True
                break
        return flag

    def _can_take_item(self, item):
        '''Проверяет, можно ли взять предмет (разблокирован ли он и есть ли свободное место в инвентаре).'''
        return self._is_item_unlocked(item) and \
            self._inventory_free_space() > 0

    def add_to_inventory(self, item):
        '''Добавляет предмет в инвентарь в первый свободный слот (где есть объект класса BasicItem).'''
        if self._can_take_item(item):
            for i, cell in enumerate(self.inventory.items):
                if cell.__class__ == items_sprites.BasicItem:
                    cell.kill()
                    self.inventory.items[i] = item
                    self.inventory.items[i].player_takes_item(player=self)
                    break

    def replace_inventory_cell(self, index: int, item):
        '''Принудительно заменяет конкретный элемент инвентаря на новый, убивая старый.'''
        if not isinstance(item, items_sprites.BasicItem):
            cf.INTERRUPT_ERROR(2)
        self.inventory.items[index].kill()
        self.inventory.items[index] = item.deepcopy()

    def change_active_slot(self, new_active_slot_index):
        '''Изменяет активный слот инвентаря на новый. Отключает рендеринг старого активного 
        предмета и включает рендеринг нового.'''
        if not self.active_slot == self.inventory.items[new_active_slot_index]:
            self.active_slot_index = new_active_slot_index
            self.active_slot.set_displaying(False)
            self.active_slot = self.inventory.items[self.active_slot_index]
            self.active_slot.set_displaying(True,
                                            self.active_slot.displaying_layer)
            self.inventory.update()


# =============================================================== MENUS

    def open_menu(self):
        interactive_collisions = pygame.sprite.spritecollide(
            self, self.game_groups_dict["interactive_objects_group"], dokill=0)
        for obj in interactive_collisions:
            if obj._is_object_displaying():
                if obj.name == "Door":
                    obj.open(player=self, game=self.game)
                    self._change_flag("can_move", False)
                elif self._is_menu_opened(obj.name) == False:
                    cf.activate_with_temp_forbid(
                        id=11, delay=1000, function=obj.open, player=self, game=self.game)
                    # self._set_menu_opened(obj.name, True)
                    # self._change_flag("can_move", False)

    def close_menu(self):
        interactive_collisions = pygame.sprite.spritecollide(
            self, self.game_groups_dict["interactive_objects_group"], dokill=0)
        for obj in interactive_collisions:
            if not "Door" in obj.name and \
                    self._is_menu_opened(obj.name) == True:
                obj.close(player=self)
                self._set_menu_opened(obj.name, False)
                self._change_flag("can_move", True)

# =============================================================== UPDATE

    def update_stamina(self):
        '''Обновляет состояние стамины игрока, восстанавливая её со временем, если это необходимо.'''
        if self.get_stamina() < 100:
            self.restore_stamina_by_time()

    def update_hp(self):
        if self.hp < 1:
            print("YOU DEAD")
            self.game.window = "lose_screen"

    def process_mouse(self, button_id: int, pressed_unpressed: bool):
        if button_id == 1:  # ЛКМ
            self.active_slot.left_mouse_click_action(pressed_unpressed)
        elif button_id == 2:  # СКМ
            print(pygame.mouse.get_pos())
        elif button_id == 3:  # ПКМ
            pass

    def process_keystrokes(self, K_P: list):
        '''Обрабатывает нажатие клавиш.'''
        if any_key_pressed(K_P, "W", "A", "S", "D"):
            if self._get_flag("can_move"):
                self._set_player_status("idle", False)
                self._set_player_status("moving", True)
        else:
            self._set_player_status("idle", True)
            self._set_player_status("moving", False)

        if key_pressed(K_P, "F"):
            self.take_item()
            self.open_menu()

        if key_pressed(K_P, "ESC"):
            self.close_menu()

        if key_pressed(K_P, "L_SHIFT") and any_key_pressed(K_P, "W", "A", "S", "D"):
            if self.get_stamina() >= 4:
                self._set_player_status("sprint", True)
                cf.activate_with_temp_forbid(
                    id=self.sprint_event_id,
                    delay=100,
                    function=self.spend_stamina,
                    value=4)
        else:
            self._set_player_status("sprint", False)

        if key_pressed(K_P, "1"):
            self.change_active_slot(0)

        if key_pressed(K_P, "2"):
            self.change_active_slot(1)

        if key_pressed(K_P, "3"):
            self.change_active_slot(2)

        if key_pressed(K_P, "4"):
            self.change_active_slot(3)

    def update_position(self, K_P: list):
        '''Обновляет позицию игрока в зависимости от нажатых клавиш для перемещения.'''
        move_x = 0
        move_y = 0

        if key_pressed(K_P, "A"):
            if self._get_flag("can_move_left"):
                move_x = -self.movement_speed
        if key_pressed(K_P, "D"):
            if self._get_flag("can_move_right"):
                move_x = self.movement_speed
        if key_pressed(K_P, "W"):
            if self._get_flag("can_move_up"):
                move_y = -self.movement_speed
        if key_pressed(K_P, "S"):
            if self._get_flag("can_move_down"):
                move_y = self.movement_speed

        if self.get_stamina() >= 4:
            if key_pressed(K_P, "L_SHIFT") and any_key_pressed(K_P, "W", "S", "A", "D"):
                move_x *= 1.5
                move_y *= 1.5

        # Нормализуем движение при движении по диагонали
        if move_x != 0 and move_y != 0:
            slowdown_ratio = 1.3
            move_x /= slowdown_ratio
            move_y /= slowdown_ratio

        if self._get_flag("can_move"):
            self.rect.x += move_x / gc.FPS_LIMIT
            self.rect.y += move_y / gc.FPS_LIMIT

    def check_collisions(self):
        self._change_flag("can_move_up",    True)
        self._change_flag("can_move_down",  True)
        self._change_flag("can_move_left",  True)
        self._change_flag("can_move_right", True)
        collisions = pygame.sprite.spritecollide(
            self,
            self.game_groups_dict["barriers_group"],
            dokill=False)
        if collisions:
            for barrier in collisions:
                barrier.process(self)
                if barrier.colliding_top():
                    self._change_flag("can_move_down",  False)
                elif barrier.colliding_left():
                    self._change_flag("can_move_right", False)
                elif barrier.colliding_bottom():
                    self._change_flag("can_move_up",    False)
                else:
                    self._change_flag("can_move_left",  False)

    def update(self, **kwargs):
        '''Обновляет состояние игрока каждый кадр'''
        K_P = kwargs["keys_pressed"]
        self.update_stamina()
        self.update_hp()
        self.process_keystrokes(K_P)
        self.check_collisions()
        self.update_position(K_P)

        self.change_active_slot(self.active_slot_index)
        self.active_slot.follow_player(player=self)
        self.active_slot.update(player=self)

        self.status_idle()
        self.status_moving()
        self.status_sprint()
        self.status_attack()

        # self.TEST_VALUE += 1
        # if self.TEST_VALUE > 60:
        #     self.TEST_VALUE = 0
        #     print(self.get_stamina())
        #     print(f"0000 {cf.get_forbidden_events()} \n===={
        #           cf.get_delayed_events()}")
        #     print(self._get_flag("can_restore_stamina_by_time"))
        #     print()

        # for i in self.inventory.items:
        #     print(i.name, end=', ')
        # print()
