import random
from entities.bullet import Bullet

class Enemy:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10, fill="red")  # Враг — красный круг
        self.dx = random.choice([-3, 3])  # Начальная скорость по X
        self.dy = random.choice([-3, 3])  # Начальная скорость по Y
        self.health = 100
        self.move_enemy()
        self.shoot()

    def move_enemy(self):
        """Передвижение врага, вызывается из `Game.update_enemy_movement()`"""
        self.canvas.move(self.rect, self.dx, self.dy)

    def change_direction(self):
        """Меняет направление врага при столкновении"""
        self.dx = -self.dx
        self.dy = -self.dy

    def shoot(self):
        """Враг стреляет, если он не удалён"""
        if self.rect not in self.canvas.find_all():
            return  # Враг удалён, прекращаем стрельбу

        coords = self.canvas.coords(self.rect)
        if len(coords) < 4:
            print("Ошибка: враг пытается стрелять, но у него нет координат!")
            return
        x1, y1, x2, y2 = coords
        Bullet(self.canvas, (x1 + x2) / 2, (y1 + y2) / 2,
               dx=random.choice([i for i in range(-5,6) if i]),
               dy=random.choice([i for i in range(-5,6) if i]))
        self.canvas.after(2000, self.shoot)  # Запускаем следующий выстрел через 2 секунды
