import tkinter as tk
import random
from PIL import Image, ImageTk, ImageFilter, ImageEnhance

from entities.player import Player
from entities.enemy import Enemy
from entities.wall import Wall
from entities.bullet import Bullet
from rooms.room import Room

from collision import check_collision, check_bullet_collision, check_enemy_collision, check_enemy_collision_with_walls, check_attack_collision
from map_generator import generate_rooms

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

        raw_rooms = generate_rooms(5)  # Получаем словарь с данными
        self.rooms = {room_id: Room(self.canvas, room_id, data["connections"]) for room_id, data in raw_rooms.items()}

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

    def load_room(self, room_id, entrance_direction=None):
        """Загружает новую комнату и ставит игрока у соответствующей двери"""
        print(f"Переход в комнату {room_id} (вход с {entrance_direction})")
        self.int.itemconfig(self.room_text, text=f"Комната: {room_id}")

        # Очищаем холст
        self.canvas.delete("all")

        # Загружаем новую комнату
        self.current_room = self.rooms[room_id]
        self.current_room.generate_walls()
        self.current_room.generate_doors()
        self.current_room.spawn_enemies()

        # Запускаем движение врагов
        self.update_enemy_movement()

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
            self.player.attack(key, lambda x1, y1, x2, y2: check_attack_collision(self, x1, y1, x2, y2)) # Атака мечом

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

        check_enemy_collision(self)  # Проверяем столкновение с врагами
        check_bullet_collision(self, Bullet)  # Проверяем попадание пули
        self.check_room_transition()  # Проверяем, вошёл ли игрок в дверь

        self.root.after(16, self.update_movement)

    def move_player(self, dx, dy):
        """Двигает игрока, если нет столкновения"""
        if not check_collision(self, dx, dy):  # Если нет столкновения, двигаем
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

    def update_enemy_movement(self):
        """Обновляет движение всех врагов, проверяя столкновения"""
        for enemy in self.current_room.enemies:
            if check_enemy_collision_with_walls(self, enemy):
                enemy.change_direction()  # Меняем направление, если враг упёрся в стену

            enemy.move_enemy()  # Двигаем врага

        self.root.after(30, self.update_enemy_movement)  # Запускаем обновление движения


    def game_over(self):
        """Вывод сообщения о проигрыше"""
        self.int.create_text(300, 100, text="Вы проиграли!", font=("Arial", 24), fill="red")
        self.player.remove_sprite()
        self.root.unbind("<KeyPress>")
        self.root.unbind("<KeyRelease>")