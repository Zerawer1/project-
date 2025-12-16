import pygame
import math
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Индивидуальное задание №1 — Вариант 18")

CENTER = (WIDTH // 2, HEIGHT // 2)
BASE_OUTER_HALF = 150  # базовый размер внешнего квадрата (половина стороны)
INNER_RATIO = 0.6      # отношение внутреннего ромба к внешнему
SCALE_MIN, SCALE_MAX = 0.5, 2.0

font = pygame.font.SysFont("Arial", 24)
clock = pygame.time.Clock()

def bresenham_line(surface, x1, y1, x2, y2, color=WHITE):

    x1 = int(round(x1)); y1 = int(round(y1))
    x2 = int(round(x2)); y2 = int(round(y2))

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    steep = dy > dx

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
        dx, dy = dy, dx

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    y_step = 1 if y1 < y2 else -1
    error = dx // 2
    y = y1

    # локальные переменные для ускорения
    width, height = surface.get_size()

    for x in range(x1, x2 + 1):
        px, py = (y, x) if steep else (x, y)
        if 0 <= px < width and 0 <= py < height:
            surface.set_at((px, py), color)

        error -= dy
        if error < 0:
            y += y_step
            error += dx


def rotate_points(points, cos_a, sin_a, tx=0.0, ty=0.0):

    out = []
    for x, y in points:
        rx = x * cos_a - y * sin_a + tx
        ry = x * sin_a + y * cos_a + ty
        out.append((rx, ry))
    return out


def make_local_square(half):
    # Возвращает список вершин квадрата (локальные координаты) по часовой.
    return [(-half, -half), (half, -half), (half, half), (-half, half)]


# --- Основная функция рисования фигуры ---
def draw_figure(surface, center, scale=1.0, rotation_deg=0.0):
    cx, cy = center
    # очищаем экран
    surface.fill(BLACK)

    # заранее вычисляем косинус/синус для ускорения
    angle_rad = math.radians(rotation_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    # --- внешняя рамка (квадрат) ---
    outer_half = BASE_OUTER_HALF * scale
    local_outer = make_local_square(outer_half)
    outer_points = rotate_points(local_outer, cos_a, sin_a, cx, cy)

    # --- внутренний ромб (квадрат, повернутый на 45° относительно рамки) ---
    inner_half = outer_half * INNER_RATIO
    # применяем дополнительный поворот +45 градусов: кос и син суммарного угла
    angle_inner_rad = math.radians(rotation_deg + 45)
    cos_i = math.cos(angle_inner_rad)
    sin_i = math.sin(angle_inner_rad)
    local_inner = make_local_square(inner_half)
    inner_points = rotate_points(local_inner, cos_i, sin_i, cx, cy)

    # Блокируем поверхность при множественной записи пикселей для ускорения
    surface.lock()
    try:
        # рисуем стороны внешнего квадрата
        for i in range(4):
            x1, y1 = outer_points[i]
            x2, y2 = outer_points[(i + 1) % 4]
            bresenham_line(surface, x1, y1, x2, y2, WHITE)

        # рисуем стороны внутреннего (ромб)
        for i in range(4):
            x1, y1 = inner_points[i]
            x2, y2 = inner_points[(i + 1) % 4]
            bresenham_line(surface, x1, y1, x2, y2, WHITE)

        # диагонали: как в исходнике
        A, B, C, D = inner_points
        mid_BC = ((B[0] + C[0]) / 2.0, (B[1] + C[1]) / 2.0)
        mid_AD = ((A[0] + D[0]) / 2.0, (A[1] + D[1]) / 2.0)

        bresenham_line(surface, D[0], D[1], mid_BC[0], mid_BC[1], WHITE)
        bresenham_line(surface, B[0], B[1], mid_AD[0], mid_AD[1], WHITE)
    finally:
        surface.unlock()


# --- Переменные состояния анимации ---
scale = 1.0
rotation = 0.0
transformation_mode = 0  # 0 - масштаб, 1 - вращение
moving = False

# --- Главный цикл ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # левая — старт/пауза
                moving = not moving
            elif event.button == 3:  # правая — переключение режима
                transformation_mode = (transformation_mode + 1) % 2

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                moving = not moving
            elif event.key == pygame.K_r:
                rotation = 0
                scale = 1.0

    # анимация
    if moving:
        if transformation_mode == 0:  # масштабируем
            scale += 0.02
            if scale > SCALE_MAX:
                scale = SCALE_MIN
        else:  # вращаем
            rotation = (rotation + 2) % 360

    # рисуем фигуру (на экран напрямую)
    draw_figure(screen, CENTER, scale, rotation)

    # отрисовка HUD (создаётся один текстовый объект на кадр — дешево)
    mode_text = font.render(f"Режим: {'Масштаб' if transformation_mode == 0 else 'Вращение'}", True, WHITE)
    state_text = font.render(f"Состояние: {'Движение' if moving else 'Пауза'}", True, WHITE)
    screen.blit(mode_text, (10, 10))
    screen.blit(state_text, (10, 40))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
