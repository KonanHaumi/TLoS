import random
from rooms.room import Room  # Импортируем класс Room

def generate_rooms(number=5, canvas=None):
    """Генерирует карту с комнатами в правильном формате"""
    raw_rooms = bfs_generation(number)  # Генерируем структуру комнат
    generate_enemies(raw_rooms)  # Добавляем случайных врагов

    # Преобразуем в объект Room с нужным форматом
    rooms = {
        room_id: Room(canvas, room_id, data["neighbors"], enemies=data["enemies"])
        for room_id, data in raw_rooms.items()
    }

    print_structure(rooms)
    return rooms


def print_structure(rooms):
    """Вывод структуры комнат в консоль"""
    for room_id, room in rooms.items():
        print(f"Комната {room_id}, соединения: {room.neighbors}, враги: {room.enemy_positions}")


def bfs_generation(number):
    """Генерирует случайные комнаты, создавая связи"""
    rooms = {
        0: {"neighbors": {}, "enemies": []}  # Стартовая комната без врагов
    }
    queue = [0]
    room_id = 1
    directions = ["right", "left", "up", "down"]

    while queue and room_id < number:
        current = queue.pop(0)
        random.shuffle(directions)

        connections_added = 0
        for direction in directions:
            if room_id >= number or connections_added >= 2:  # Ограничиваем связи
                break

            if direction in rooms[current]["neighbors"]:
                continue

            # Создаём новую комнату с пустыми врагами
            rooms[current]["neighbors"][direction] = room_id
            rooms[room_id] = {"neighbors": {opposite_direction(direction): current}, "enemies": []}
            queue.append(room_id)

            room_id += 1
            connections_added += 1

    return rooms

def generate_enemies(rooms):
    """Добавляет случайных врагов в комнаты"""
    for room_id, data in rooms.items():
        if room_id == 0:  # В начальной комнате врагов нет
            continue

        num_enemies = random.randint(1, 4)  # Количество врагов (1-4)
        enemy_positions = [(random.randint(80, 500), random.randint(80, 500)) for _ in range(num_enemies)]

        data["enemies"] = enemy_positions  # Сохраняем врагов в нужном формате


def opposite_direction(direction):
    """Определяет противоположное направление"""
    opposites = {"right": "left", "left": "right", "up": "down", "down": "up"}
    return opposites[direction]