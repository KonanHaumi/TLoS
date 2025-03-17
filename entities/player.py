class Player:
    def __init__(self, canvas, x, y, image):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10, fill = "black")
        self.sprite = canvas.create_image(x, y, image=image)
        self.image = image  # Сохраняем изображение, чтобы оно не удалилось
        self.keys_pressed = set()
        self.health = 100  # Количество жизней

    def update_sprite_position(self):
        """Синхронизирует спрайт с позицией хитбокса (прямоугольника)"""
        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        self.canvas.coords(self.sprite, center_x, center_y)

    def remove_sprite(self):
        """Удаляет спрайт с холста"""
        self.canvas.delete(self.sprite)