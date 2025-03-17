class Bullet:
    bullets = []

    def __init__(self, canvas, x, y, dx, dy):
        self.canvas = canvas
        self.rect = canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="yellow")
        self.dx = dx
        self.dy = dy
        self.alive = True
        Bullet.bullets.append(self)
        self.move_bullet()

    def move_bullet(self):
        if not self.alive:
            return  # Если пуля уже уничтожена — не продолжаем движение

        self.canvas.move(self.rect, self.dx, self.dy)
        coords = self.canvas.coords(self.rect)

        if len(coords) < 4:
            return

        x1, y1, x2, y2 = coords

        if x2 < 0 or x1 > 600 or y2 < 0 or y1 > 600:
            self.destroy()
        else:
            self.canvas.after(30, self.move_bullet)

    def destroy(self):
        if self in Bullet.bullets:
            Bullet.bullets.remove(self)
        self.alive = False
        self.canvas.delete(self.rect)