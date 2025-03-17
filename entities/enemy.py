import random
from entities.bullet import Bullet



class Enemy:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10, fill="red")  # Враг — красный круг
        self.dx = random.choice([-3, 3])  # Начальная скорость по X
        self.dy = random.choice([-3, 3])  # Начальная скорость по Y
        self.move_enemy()
        self.shoot()

    def move_enemy(self):
        #Передвижение врага
        self.canvas.move(self.rect, self.dx, self.dy)
        x1, y1, x2, y2 = self.canvas.coords(self.rect)

        # Проверка на границы поля
        if x1 <= 0 or x2 >= 600:
            self.dx = -self.dx  # Меняем направление по X
        if y1 <= 0 or y2 >= 600:
            self.dy = -self.dy  # Меняем направление по Y

        self.canvas.after(30, self.move_enemy)  # Каждые 50 мс обновляем положение

    def shoot(self):
        """Враг стреляет каждые 2 секунды"""
        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        Bullet(self.canvas, (x1 + x2) / 2, (y1 + y2) / 2,
               dx=random.choice([i for i in range(-5,6) if i]),
               dy=random.choice([i for i in range(-5,6) if i]))
        self.canvas.after(2000, self.shoot)  # Запускаем следующий выстрел через 2 секунды
