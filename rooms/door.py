class Door:
    def __init__(self, canvas, x1, y1, x2, y2, target_room, direction, locked=True):
        """
        Дверь, ведущая в другую комнату.
        :param canvas: Холст
        :param x1, y1, x2, y2: Координаты двери
        :param target_room: Номер комнаты, в которую ведёт дверь
        :param direction: Направление, из которого заходит игрок ("up", "down", "left", "right")
        """
        self.canvas = canvas
        self.locked = locked
        self.rect = canvas.create_rectangle(x1, y1, x2, y2, fill=self.get_color(), outline="black", width=3)
        self.target_room = target_room
        self.direction = direction  # Добавляем направление


    def get_color(self):
        return "darkorange" if self.locked else "green"

    def update_color(self):
        self.canvas.itemconfig(self.rect, fill=self.get_color())

    def check_transition(self, player_coords):
        """Проверяет, зашёл ли игрок в дверь"""
        door_coords = self.canvas.coords(self.rect)

        if len(door_coords) < 4:  # Если координаты двери отсутствуют, пропускаем
            return None

        if (player_coords[2] > door_coords[0] and player_coords[0] < door_coords[2] and
                player_coords[3] > door_coords[1] and player_coords[1] < door_coords[3]):
            return self.target_room

        return None