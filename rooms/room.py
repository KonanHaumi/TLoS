from rooms.door import Door
from entities.wall import Wall
from entities.enemy import Enemy

class Room:
    def __init__(self, canvas, room_id, neighbors, enemies = None):
        self.canvas = canvas
        self.room_id = room_id
        self.neighbors = neighbors
        self.doors = []
        self.walls = []
        self.enemies = []
        self.enemy_positions = enemies if enemies else []  # Сохраняем позиции врагов

    def generate_walls(self):
        """Создаёт стены по краям (кроме мест для дверей)"""
        self.walls = [
            Wall(self.canvas, 50, 50, 550, 70),  # Верхняя стена
            Wall(self.canvas, 50, 530, 550, 550),  # Нижняя стена
            Wall(self.canvas, 50, 70, 70, 530),  # Левая стена
            Wall(self.canvas, 530, 70, 550, 530)  # Правая стена
        ]

    def generate_doors(self):
        """Создаёт двери, если есть соединение с соседней комнатой"""
        door_width = 40  # Увеличиваем ширину двери
        door_height = 40  # Увеличиваем высоту двери

        if "up" in self.neighbors and self.neighbors["up"] is not None:
            self.doors.append(Door(self.canvas, 280, 40, 320, 80, self.neighbors["up"]))  # Верхняя дверь
        if "down" in self.neighbors and self.neighbors["down"] is not None:
            self.doors.append(Door(self.canvas, 280, 520, 320, 560, self.neighbors["down"]))  # Нижняя дверь
        if "left" in self.neighbors and self.neighbors["left"] is not None:
            self.doors.append(Door(self.canvas, 40, 280, 80, 320, self.neighbors["left"]))  # Левая дверь
        if "right" in self.neighbors and self.neighbors["right"] is not None:
            self.doors.append(Door(self.canvas, 520, 280, 560, 320, self.neighbors["right"]))  # Правая дверь

    def spawn_enemies(self):
        """Создаёт объекты врагов на основе заранее заданных координат"""
        self.enemies = [Enemy(self.canvas, x, y) for x, y in self.enemy_positions]