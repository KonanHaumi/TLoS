class Player:
    def __init__(self, canvas, x, y, image):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10, fill = "black")
        self.sprite = canvas.create_image(x, y, image=image)
        self.image = image  # Сохраняем изображение, чтобы оно не удалилось
        self.keys_pressed = set()
        self.health = 100  # Количество жизней
        self.attack_shape = None  # Для хранения удара меча

    def update_sprite_position(self):
        """Синхронизирует спрайт с позицией хитбокса (прямоугольника)"""
        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        self.canvas.coords(self.sprite, center_x, center_y)

    def remove_sprite(self):
        """Удаляет спрайт с холста"""
        self.canvas.delete(self.sprite)

    def attack(self, direction, check_attack_collision):
        """Рисует удар мечом и проверяет попадание"""
        if self.attack_shape:
            self.canvas.delete(self.attack_shape)

        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        ATTACK_WIDTH = 20  # Ширина удара
        ATTACK_LENGTH = 40  # Длина удара
        ATTACK_OFFSET = 10  # Отступ удара от игрока
        ATTACK_DURATION = 200  # Время, в течение которого удар отображается (мс)
        ATTACK_DAMAGE = 20  # Урон меча

        if direction == "up":
            attack_x1, attack_y1 = center_x - ATTACK_WIDTH // 2, y1 - ATTACK_OFFSET - ATTACK_LENGTH // 2
            attack_x2, attack_y2 = center_x + ATTACK_WIDTH // 2, y1 - ATTACK_OFFSET + ATTACK_LENGTH // 2
        elif direction == "down":
            attack_x1, attack_y1 = center_x - ATTACK_WIDTH // 2, y2 + ATTACK_OFFSET - ATTACK_LENGTH // 2
            attack_x2, attack_y2 = center_x + ATTACK_WIDTH // 2, y2 + ATTACK_OFFSET + ATTACK_LENGTH // 2
        elif direction == "left":
            attack_x1, attack_y1 = x1 - ATTACK_OFFSET - ATTACK_LENGTH // 2, center_y - ATTACK_WIDTH // 2
            attack_x2, attack_y2 = x1 - ATTACK_OFFSET + ATTACK_LENGTH // 2, center_y + ATTACK_WIDTH // 2
        elif direction == "right":
            attack_x1, attack_y1 = x2 + ATTACK_OFFSET - ATTACK_LENGTH // 2, center_y - ATTACK_WIDTH // 2
            attack_x2, attack_y2 = x2 + ATTACK_OFFSET + ATTACK_LENGTH // 2, center_y + ATTACK_WIDTH // 2
        else:
            return

        self.attack_shape = self.canvas.create_rectangle(attack_x1, attack_y1, attack_x2, attack_y2, fill="red")

        # Проверяем попадание по врагам
        check_attack_collision(attack_x1, attack_y1, attack_x2, attack_y2)

        # Убираем удар через `ATTACK_DURATION` мс
        self.canvas.after(ATTACK_DURATION, self.clear_attack)

    def clear_attack(self):
        """Удаляет визуальный эффект атаки"""
        if self.attack_shape:
            self.canvas.delete(self.attack_shape)
            self.attack_shape = None