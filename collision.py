def check_collision(game, dx, dy):
    """Проверяет, столкнётся ли игрок со стеной или дверью"""
    player_coords = game.canvas.coords(game.player.rect)
    if not player_coords:
        return False  # Если у игрока нет координат, просто пропускаем

    next_x1, next_y1, next_x2, next_y2 = (
        player_coords[0] + dx, player_coords[1] + dy,
        player_coords[2] + dx, player_coords[3] + dy
    )

    # Проверяем стены
    for wall in game.current_room.walls:
        wall_coords = game.canvas.coords(wall.rect)
        if not wall_coords or len(wall_coords) < 4:
            continue  # Пропускаем удалённые объекты

        wall_x1, wall_y1, wall_x2, wall_y2 = wall_coords

        if (next_x2 > wall_x1 and next_x1 < wall_x2 and
                next_y2 > wall_y1 and next_y1 < wall_y2):
            return True  # Столкновение со стеной

    return False  # Нет столкновения


def check_bullet_collision(game, Bullet):
    """Проверяет попадание пули в игрока"""
    player_coords = game.canvas.coords(game.player.rect)

    for bullet in Bullet.bullets[:]:  # Копируем список, чтобы безопасно удалять элементы
        bullet_coords = game.canvas.coords(bullet.rect)

        if not bullet_coords or len(bullet_coords) < 4:
            Bullet.bullets.remove(bullet)
            continue  # Пропускаем удалённые пули

        if (player_coords[2] > bullet_coords[0] and player_coords[0] < bullet_coords[2] and
                player_coords[3] > bullet_coords[1] and player_coords[1] < bullet_coords[3]):

            game.player.health -= 5  # Уменьшаем здоровье от попадания пули
            game.int.itemconfig(game.health_text, text=f"Здоровье: {game.player.health}")
            print(f"Игрок получил урон от пули! Здоровье: {game.player.health}")

            Bullet.bullets.remove(bullet)  # Убираем пулю из списка
            game.canvas.delete(bullet.rect)  # Удаляем пулю с Canvas

            if game.player.health <= 0:
                game.game_over()

def check_enemy_collision(game):
    '"""Проверка столкновения игрока с врагами"""'
    player_coords = game.canvas.coords(game.player.rect)

    if not player_coords or len(player_coords) < 4:
        return  # Если у игрока нет координат, пропускаем проверку

    for enemy in game.current_room.enemies:
        enemy_coords = game.canvas.coords(enemy.rect)

        if not enemy_coords or len(enemy_coords) < 4:
            continue  # Пропускаем удалённых врагов

        if (player_coords[2] > enemy_coords[0] and player_coords[0] < enemy_coords[2] and
                player_coords[3] > enemy_coords[1] and player_coords[1] < enemy_coords[3]):
            game.player.health -= 10  # Уменьшаем здоровье игрока
            game.int.itemconfig(game.health_text, text=f"Здоровье: {game.player.health}")
            print(f"Игрок получил урон от врага! Здоровье: {game.player.health}")

            if game.player.health <= 0:
                game.game_over()
                
def check_enemy_collision_with_walls(game, enemy):
    """Проверяет, столкнулся ли враг со стенами"""
    enemy_coords = game.canvas.coords(enemy.rect)

    if not enemy_coords or len(enemy_coords) < 4:
        return False  # Если нет координат, пропускаем проверку

    next_x1, next_y1, next_x2, next_y2 = (
        enemy_coords[0] + enemy.dx, enemy_coords[1] + enemy.dy,
        enemy_coords[2] + enemy.dx, enemy_coords[3] + enemy.dy
    )

    for wall in game.current_room.walls:
        wall_coords = game.canvas.coords(wall.rect)
        if not wall_coords or len(wall_coords) < 4:
            continue  # Пропускаем некорректные стены

        wall_x1, wall_y1, wall_x2, wall_y2 = wall_coords

        if (next_x2 > wall_x1 and next_x1 < wall_x2 and
                next_y2 > wall_y1 and next_y1 < wall_y2):
            return True  # Враг столкнулся со стеной

    return False  # Нет столкновения

def check_attack_collision(game, ax1, ay1, ax2, ay2):
    """Проверяет попадание удара меча в врагов"""
    for enemy in game.current_room.enemies[:]:  # Копируем список, чтобы безопасно удалять врагов
        enemy_coords = game.canvas.coords(enemy.rect)

        if len(enemy_coords) < 4:
            continue  # Пропускаем, если объект удалён

        ex1, ey1, ex2, ey2 = enemy_coords

        # Проверяем, пересекаются ли зоны удара и врага
        if not (ax2 <= ex1 or ax1 >= ex2 or ay2 <= ey1 or ay1 >= ey2):
            enemy.health -= 50  # Уменьшаем здоровье врага
            print(f"Враг получил урон! Осталось {enemy.health} HP")

            if enemy.health <= 0:  # Если враг умирает
                game.canvas.delete(enemy.rect)  # Удаляем объект с холста
                game.current_room.enemies.remove(enemy)  # Убираем из списка врагов
                return  # Завершаем проверку после первого попадания