import tkinter as tk
import random
from PIL import Image, ImageTk, ImageFilter, ImageEnhance

from entities.player import Player
from entities.enemy import Enemy
from entities.wall import Wall
from entities.bullet import Bullet
from rooms.room import Room



class Game:
    def __init__(self, root):
        self.root = root
        self.int = tk.Canvas(root, width=600, height = 200, bg = "gray")
        self.int.pack()
        self.canvas = tk.Canvas(root, width=600, height=600, bg="black")
        self.canvas.pack()


        img = Image.open("sprites/player.png").resize((200, 200), Image.Resampling.LANCZOS)
        img = img.resize((50, 50), Image.Resampling.NEAREST).resize((30, 30), Image.Resampling.NEAREST)


        self.player_image = ImageTk.PhotoImage(img)

        self.player = Player(self.canvas, 300, 300, self.player_image)
        # Отображение здоровья
        self.health_text = self.int.create_text(300, 25, text=f"Здоровье: {self.player.health}", font=("Arial", 14),fill="black")
        self.room_text = self.int.create_text(300, 50, text=f"Комната: 0", font=("Arial", 14), fill="black")

        self.rooms = {
            0: Room(self.canvas, 0, {"right": 1}),  # В комнате 0 два врага
            1: Room(self.canvas, 1, {"left": 0, "right": 2, "up": 3}, enemies=[(300, 300)]),  # В комнате 1 один враг
            2: Room(self.canvas, 2, {"left": 1}, enemies=[(250, 250), (450, 450), (350, 300)]),  # В комнате 2 три врага
            3: Room(self.canvas, 3, {"down": 1}, enemies=[])  # В комнате 3 нет врагов
        }
        self.current_room = self.rooms[0]  # Начальная комната
        self.load_room(0)

        # Создаём стены
        self.walls = []
        # Создаём врагов
        self.enemies = []
        self.bullets = []


        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)
        self.update_movement()  # Запускаем обновление движения
        self.check_bullet_collision()

    def load_room(self, room_id, entrance_direction=None):
        """Загружает новую комнату и ставит игрока у соответствующей двери"""
        print(f"Переход в комнату {room_id} (вход с {entrance_direction})")

        # Очищаем холст
        self.canvas.delete("all")

        # Загружаем новую комнату
        self.current_room = self.rooms[room_id]
        self.current_room.generate_walls()
        self.current_room.generate_doors()
        self.current_room.spawn_enemies()

        # Определяем позицию игрока у входа
        offset = 100
        if entrance_direction == "right":
            player_x, player_y = 600 - offset, 300 # Левая дверь (сдвиг вправо)
        elif entrance_direction == "left":
            player_x, player_y = 0 + offset, 300   # Правая дверь (сдвиг влево)
        elif entrance_direction == "up":
            player_x, player_y = 300, 0 + offset # Нижняя дверь (сдвиг вверх)
        elif entrance_direction == "down":
            player_x, player_y = 300, 600 - offset # Верхняя дверь (сдвиг вниз)
        else:
            player_x, player_y = 300, 300  # Если нет направления, появляемся в центре

        # Создаём игрока в нужном месте
        self.player.rect = self.canvas.create_rectangle(
            player_x - 10, player_y - 10, player_x + 10, player_y + 10, fill="cyan"
        )

    def key_press(self, event):
        """Обрабатывает нажатие клавиш"""
        key = event.keysym.lower()
        if key in ("w", "a", "s", "d"):
            self.player.keys_pressed.add(key)  # Движение
        elif key in ("up", "down", "left", "right"):
            self.player.attack(key, self.check_attack_collision)  # Атака мечом

    def key_release(self, event):
        key = event.keysym.lower()
        self.player.keys_pressed.discard(key)

    def update_movement(self):
        """Обновляет движение игрока и проверяет столкновения"""
        for key in self.player.keys_pressed:
            if key == "w":
                self.move_player(0, -5)
            elif key == "s":
                self.move_player(0, 5)
            elif key == "a":
                self.move_player(-5, 0)
            elif key == "d":
                self.move_player(5, 0)

        self.check_enemy_collision()  # Проверяем столкновение с врагами
        self.check_bullet_collision()  # Проверяем попадание пули
        self.check_room_transition()  # Проверяем, вошёл ли игрок в дверь

        self.root.after(16, self.update_movement)

    def move_player(self, dx, dy):
        """Двигает игрока, если нет столкновения"""
        if not self.check_collision(dx, dy):  # Если нет столкновения, двигаем
            self.canvas.move(self.player.rect, dx, dy)
            self.player.update_sprite_position()

    def check_room_transition(self):
        """Проверяет, зашёл ли игрок в дверь и меняет комнату"""
        player_coords = self.canvas.coords(self.player.rect)

        for door in self.current_room.doors:
            door_coords = self.canvas.coords(door.rect)
            if not door_coords or len(door_coords) < 4:
                continue  # Пропускаем некорректные двери

            if (player_coords[2] > door_coords[0] and player_coords[0] < door_coords[2] and
                    player_coords[3] > door_coords[1] and player_coords[1] < door_coords[3]):
                self.load_room(door.target_room, door.direction)  # Передаём направление входа
                return

    def check_collision(self, dx, dy):
        """Проверяет, столкнётся ли игрок со стеной или дверью"""
        player_coords = self.canvas.coords(self.player.rect)
        if not player_coords:
            return False  # Если у игрока нет координат, просто пропускаем

        next_x1, next_y1, next_x2, next_y2 = (
            player_coords[0] + dx, player_coords[1] + dy,
            player_coords[2] + dx, player_coords[3] + dy
        )

        # Проверяем стены
        for wall in self.current_room.walls:
            wall_coords = self.canvas.coords(wall.rect)
            if not wall_coords or len(wall_coords) < 4:
                continue  # Пропускаем удалённые объекты

            wall_x1, wall_y1, wall_x2, wall_y2 = wall_coords

            if (next_x2 > wall_x1 and next_x1 < wall_x2 and
                    next_y2 > wall_y1 and next_y1 < wall_y2):
                return True  # Столкновение со стеной

        return False  # Нет столкновения

    def check_bullet_collision(self):
        """Проверяет попадание пули в игрока"""
        player_coords = self.canvas.coords(self.player.rect)

        for bullet in Bullet.bullets[:]:  # Копируем список, чтобы безопасно удалять элементы
            bullet_coords = self.canvas.coords(bullet.rect)

            if not bullet_coords or len(bullet_coords) < 4:
                Bullet.bullets.remove(bullet)
                continue  # Пропускаем удалённые пули

            if (player_coords[2] > bullet_coords[0] and player_coords[0] < bullet_coords[2] and
                    player_coords[3] > bullet_coords[1] and player_coords[1] < bullet_coords[3]):

                self.player.health -= 5  # Уменьшаем здоровье от попадания пули
                self.int.itemconfig(self.health_text, text=f"Здоровье: {self.player.health}")
                print(f"Игрок получил урон от пули! Здоровье: {self.player.health}")

                Bullet.bullets.remove(bullet)  # Убираем пулю из списка
                self.canvas.delete(bullet.rect)  # Удаляем пулю с Canvas

                if self.player.health <= 0:
                    self.game_over()

    def check_enemy_collision(self):
        """Проверка столкновения игрока с врагами"""
        player_coords = self.canvas.coords(self.player.rect)

        if not player_coords or len(player_coords) < 4:
            return  # Если у игрока нет координат, пропускаем проверку

        for enemy in self.current_room.enemies:
            enemy_coords = self.canvas.coords(enemy.rect)

            if not enemy_coords or len(enemy_coords) < 4:
                continue  # Пропускаем удалённых врагов

            if (player_coords[2] > enemy_coords[0] and player_coords[0] < enemy_coords[2] and
                    player_coords[3] > enemy_coords[1] and player_coords[1] < enemy_coords[3]):
                self.player.health -= 10  # Уменьшаем здоровье игрока
                self.int.itemconfig(self.health_text, text=f"Здоровье: {self.player.health}")
                print(f"Игрок получил урон от врага! Здоровье: {self.player.health}")

                if self.player.health <= 0:
                    self.game_over()

    def check_attack_collision(self, ax1, ay1, ax2, ay2):
        """Проверяет попадание удара меча в врагов"""
        for enemy in self.current_room.enemies[:]:  # Копируем список, чтобы безопасно удалять врагов
            enemy_coords = self.canvas.coords(enemy.rect)

            if len(enemy_coords) < 4:
                continue  # Пропускаем, если объект удалён

            ex1, ey1, ex2, ey2 = enemy_coords

            # Проверяем, пересекаются ли зоны удара и врага
            if not (ax2 <= ex1 or ax1 >= ex2 or ay2 <= ey1 or ay1 >= ey2):
                enemy.health -= 50  # Уменьшаем здоровье врага
                print(f"Враг получил урон! Осталось {enemy.health} HP")

                if enemy.health <= 0:  # Если враг умирает
                    self.canvas.delete(enemy.rect)  # Удаляем объект с холста
                    self.current_room.enemies.remove(enemy)  # Убираем из списка врагов
                    return  # Завершаем проверку после первого попадания

    def game_over(self):
        """Вывод сообщения о проигрыше"""
        self.int.create_text(300, 100, text="Вы проиграли!", font=("Arial", 24), fill="red")
        self.player.remove_sprite()
        self.root.unbind("<KeyPress>")
        self.root.unbind("<KeyRelease>")
