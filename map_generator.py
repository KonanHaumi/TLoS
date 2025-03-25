import random

def generate_rooms(n):
    rooms = bfs_generation(n)  # Генерация 10 случайных комнат
    print_structure(rooms)
    return rooms


def print_structure(rooms):
    """Вывод структуры в консоль"""
    for room_id, data in rooms.items():
        print(f"Комната {room_id}, соединения: {data['connections']}")


def bfs_generation(number):
    """Генерирует случайную карту комнат с BFS (обход в ширину)"""
    rooms = {0: {"connections": {}}}
    queue = [0]
    room_id = 1
    directions = ["right", "left", "up", "down"]

    while queue and room_id < number:
        current = queue.pop(0)
        random.shuffle(directions)  # Перемешиваем направления

        connections_added = 0  # Ограничиваем количество дверей в комнату
        for direction in directions:
            if room_id >= number or connections_added >= 2:  # Ограничиваем 2 связи на комнату
                break

            # Проверяем, нет ли уже комнаты в этом направлении
            if direction in rooms[current]["connections"]:
                continue

            # Создаём новую комнату и связываем её
            rooms[current]["connections"][direction] = room_id
            rooms[room_id] = {"connections": {opposite_direction(direction): current}}
            queue.append(room_id)

            room_id += 1
            connections_added += 1  # Учитываем добавленную связь

    return rooms


def opposite_direction(direction):
    """Определяет противоположное направление"""
    opposites = {"right": "left", "left": "right", "up": "down", "down": "up"}
    return opposites[direction]