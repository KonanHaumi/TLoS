from rooms.door import Door
from entities.wall import Wall
from entities.enemy import Enemy

class Room:
    def __init__(self, canvas, room_id, neighbors):
        self.canvas = canvas
        self.room_id = room_id
        self.neighbors = neighbors
        self.doors = []
        self.walls = []
        self.enemies = []  # Обязательно создаём пустой список врагов!

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
        if "up" in self.neighbors and self.neighbors["up"] is not None:
            self.doors.append(Door(self.canvas, 290, 50, 310, 70, self.neighbors["up"]))  # Верхняя дверь
        if "down" in self.neighbors and self.neighbors["down"] is not None:
            self.doors.append(Door(self.canvas, 290, 530, 310, 550, self.neighbors["down"]))  # Нижняя дверь
        if "left" in self.neighbors and self.neighbors["left"] is not None:
            self.doors.append(Door(self.canvas, 50, 290, 70, 310, self.neighbors["left"]))  # Левая дверь
        if "right" in self.neighbors and self.neighbors["right"] is not None:
            self.doors.append(Door(self.canvas, 530, 290, 550, 310, self.neighbors["right"]))  # Правая дверь

    def spawn_enemies(self):
        """Создаёт врагов в комнате (можно задавать вручную)"""
        if self.room_id == 1:
            self.enemies = [
                Enemy(self.canvas, 400, 300)
            ]
        elif self.room_id == 2:
            self.enemies = [
                Enemy(self.canvas, 300, 200),
                Enemy(self.canvas, 300, 400)
            ]
        else:
            self.enemies = []