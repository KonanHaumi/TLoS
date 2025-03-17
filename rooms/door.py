class Door:
    def __init__(self, canvas, x1, y1, x2, y2, target_room):
        """
        Дверь, ведущая в другую комнату.
        :param canvas: Холст
        :param x1, y1, x2, y2: Координаты двери
        :param target_room: Номер комнаты, в которую ведёт дверь
        """
        self.canvas = canvas
        self.rect = canvas.create_rectangle(x1, y1, x2, y2, fill="brown")
        self.target_room = target_room

    def check_transition(self, player_coords):
        """Проверяет, зашёл ли игрок в дверь"""
        door_coords = self.canvas.coords(self.rect)
        if (player_coords[2] > door_coords[0] and player_coords[0] < door_coords[2] and
            player_coords[3] > door_coords[1] and player_coords[1] < door_coords[3]):
            return self.target_room
        return None