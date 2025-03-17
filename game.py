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
            0: Room(self.canvas, 0, {"right": 1}),  # Комната 0 → направо в 1
            1: Room(self.canvas, 1, {"left": 0, "right": 2, "up": 3}),  # Комната 1 → влево в 0, направо в 2
            2: Room(self.canvas, 2, {"left": 1}),  # Комната 2 → влево в 1
            3: Room(self.canvas, 1, {"down": 1}),  # Комната 1 → влево в 0, направо в 2
        }
        self.current_room = self.rooms[0]  # Начальная комната
        self.load_room(0)

        # Создаём стены
        self.walls = [
            #Wall(self.canvas, 100, 100, 200, 120),
            #Wall(self.canvas, 400, 200, 500, 220),
            #Wall(self.canvas, 250, 400, 350, 420)
        ]
        # Создаём врагов
        self.enemies = [
            #Enemy(self.canvas, 150, 150),
            #Enemy(self.canvas, 450, 450),
            #Enemy(self.canvas, 50, 50),
            #Enemy(self.canvas, 500, 450)
        ]

        self.bullets = []


        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)
        self.update_movement()  # Запускаем обновление движения
        self.check_bullet_collision()

    def load_room(self, room_id):
        """Загружает новую комнату"""
        print(f"Переход в комнату {room_id}")
        self.int.itemconfig(self.room_text, text=f"Комната: {room_id}")

        # Очищаем холст
        self.canvas.delete("all")

        # Обнуляем список врагов перед созданием новой комнаты
        self.current_room.enemies.clear()
        # Загружаем новую комнату
        self.current_room = self.rooms[room_id]
        self.current_room.generate_walls()
        self.current_room.generate_doors()  # Двери создаются снова
        self.current_room.spawn_enemies()

        # Создаём нового игрока в центре комнаты
        self.player.rect = self.canvas.create_rectangle(290, 290, 310, 310, fill="cyan")

        # Перерисовываем двери
        for door in self.current_room.doors:
            door_coords = self.canvas.coords(door.rect)
            if len(door_coords) == 4:
                self.canvas.create_rectangle(*door_coords, fill="brown")
            else:
                print(f"Ошибка: дверь {door} не имеет координат!")

    def key_press(self, event):
        key = event.keysym.lower()
        if key in ("w", "a", "s", "d"):  # Обрабатываем нажатие W, A, S, D
            self.player.keys_pressed.add(key)

    def key_release(self, event):
        key = event.keysym.lower()
        self.player.keys_pressed.discard(key)

    def update_movement(self):
        """Обновляет движение игрока и проверяет переходы"""
        for key in self.player.keys_pressed:
            if key == "w":
                self.move_player(0, -5)
            elif key == "s":
                self.move_player(0, 5)
            elif key == "a":
                self.move_player(-5, 0)
            elif key == "d":
                self.move_player(5, 0)
        self.check_room_transition()  # Проверяем, зашёл ли игрок в дверь
        self.root.after(16, self.update_movement)

    def move_player(self, dx, dy):
        self.canvas.move(self.player.rect, dx, dy)
        if self.check_collision():
            # Если столкновение, возвращаем игрока назад
            self.canvas.move(self.player.rect, -dx, -dy)
        else:
            self.player.update_sprite_position()

    def check_room_transition(self):
        """Проверяет, зашёл ли игрок в дверь и меняет комнату"""
        player_coords = self.canvas.coords(self.player.rect)

        for door in self.current_room.doors:
            target_room = door.check_transition(player_coords)
            if target_room is not None:
                self.load_room(target_room)

    def check_collision(self):
        """Проверка на столкновение игрока со стенами"""
        player_coords = self.canvas.coords(self.player.rect)
        for wall in self.walls:
            wall_coords = self.canvas.coords(wall.rect)
            if (player_coords[2] > wall_coords[0] and player_coords[0] < wall_coords[2] and
                player_coords[3] > wall_coords[1] and player_coords[1] < wall_coords[3]):
                return True
        return False

    def check_bullet_collision(self):
        """Проверяет попадание пули в игрока"""
        player_coords = self.canvas.coords(self.player.rect)

        for bullet in Bullet.bullets[:]:  # Копируем список для безопасного удаления
            bullet_coords = self.canvas.coords(bullet.rect)

            if len(bullet_coords) < 4:  # Если пуля удалена, пропускаем её
                Bullet.bullets.remove(bullet)
                continue

            if (player_coords[2] > bullet_coords[0] and player_coords[0] < bullet_coords[2] and
                    player_coords[3] > bullet_coords[1] and player_coords[1] < bullet_coords[3]):
                print("Игрок получил урон от пули!")
                self.player.health -= 10
                self.int.itemconfig(self.health_text, text=f"Здоровье: {self.player.health}")
                Bullet.bullets.remove(bullet)  # Убираем пулю из списка
                self.canvas.delete(bullet.rect)  # Удаляем пулю с Canvas

                if self.player.health <= 0:
                    self.game_over()


    def check_enemy_collision(self):
        """Проверка столкновения игрока с врагами"""
        player_coords = self.canvas.coords(self.player.rect)
        for enemy in self.enemies:
            enemy_coords = self.canvas.coords(enemy.rect)
            if (player_coords[2] > enemy_coords[0] and player_coords[0] < enemy_coords[2] and
                    player_coords[3] > enemy_coords[1] and player_coords[1] < enemy_coords[3]):
                if self.player.health <= 0:
                    self.game_over()
                else:
                    self.player.health -= 1  # Уменьшаем здоровье
                    self.int.itemconfig(self.health_text, text=f"Здоровье: {self.player.health}")

    def game_over(self):
        """Вывод сообщения о проигрыше"""
        self.int.create_text(300, 100, text="Вы проиграли!", font=("Arial", 24), fill="red")
        self.player.remove_sprite()
        self.root.unbind("<KeyPress>")
        self.root.unbind("<KeyRelease>")
