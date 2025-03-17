from rooms.door import Door
from entities.enemy import Enemy
from entities.wall import Wall

class Room:
    def __init__(self, canvas, room_id, neighbors):
        """
        Комната.
        :param canvas: Холст, на котором рисуется комната
        :param room_id: Уникальный номер комнаты
        :param neighbors: Список комнат, в которые можно перейти (словари с направлением)
        """
        self.canvas = canvas
        self.room_id = room_id
        self.neighbors = neighbors  # {'up': 1, 'down': 2, 'left': None, 'right': 3}
        self.doors = []  # Двери в соседние комнаты
        self.walls = []  # Добавляем список стен
        self.enemies = []  # Добавляем список врагов

    def generate_doors(self):
        """Создаёт двери только в доступных направлениях"""
        if "up" in self.neighbors and self.neighbors["up"] is not None:
            self.doors.append(Door(self.canvas, 290, 50, 310, 70, self.neighbors["up"]))  # Верхняя дверь
        if "down" in self.neighbors and self.neighbors["down"] is not None:
            self.doors.append(Door(self.canvas, 290, 530, 310, 550, self.neighbors["down"]))  # Нижняя дверь
        if "left" in self.neighbors and self.neighbors["left"] is not None:
            self.doors.append(Door(self.canvas, 50, 290, 70, 310, self.neighbors["left"]))  # Левая дверь
        if "right" in self.neighbors and self.neighbors["right"] is not None:
            self.doors.append(Door(self.canvas, 530, 290, 550, 310, self.neighbors["right"]))  # Правая дверь

    def spawn_enemies(self):
        """Создаёт врагов в комнате"""
        self.enemies = [
            Enemy(self.canvas, 150, 150),
            Enemy(self.canvas, 450, 450)
        ]

    def generate_walls(self):
        """Создаёт стены по краям комнаты (кроме мест для дверей)"""
        self.walls = [
            Wall(self.canvas, 50, 50, 550, 70),  # Верхняя
            Wall(self.canvas, 50, 530, 550, 550),  # Нижняя
            Wall(self.canvas, 50, 70, 70, 530),  # Левая
            Wall(self.canvas, 530, 70, 550, 530)  # Правая
        ]