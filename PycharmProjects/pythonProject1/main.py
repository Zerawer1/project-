
from __future__ import annotations

import json
import os
import random
import sys
from typing import List, Optional, Set, Tuple

import pygame

# ------------------------- Constants ---------------------------------------
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE
FPS_DEFAULT: int = 5

# Colours
BOARD_BACKGROUND_COLOR = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Directions
UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)

# Precomputed frequently used values
ALL_CELLS: Set[Tuple[int, int]] = {
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
}
CENTER_POS: Tuple[int, int] = (
    (GRID_WIDTH // 2) * GRID_SIZE,
    (GRID_HEIGHT // 2) * GRID_SIZE
)
HIGHSCORE_FILE = 'snake_highscore.json'

Direction = Tuple[int, int]

# Mapping from keys to direction vectors (pixel deltas)
KEY_TO_DIR = {
    pygame.K_UP: UP,
    pygame.K_w: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_s: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_a: LEFT,
    pygame.K_RIGHT: RIGHT,
    pygame.K_d: RIGHT,
}

# ------------------------- Global Pygame vars -------------------------------
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


# ------------------------- Game classes -----------------------------------
class GameObject:

    def __init__(
        self,
        position: Tuple[int, int] = (0, 0),
        body_color: Tuple[int, int, int] = (255, 255, 255)
    ):

        self.position = position
        self.body_color = body_color

    def draw(self, surface: pygame.Surface) -> None:

        pass

    @staticmethod
    def draw_cell(
        surface: pygame.Surface,
        position: Tuple[int, int],
        color: Tuple[int, int, int]
    ) -> None:

        rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, color, rect)


class Apple(GameObject):


    def __init__(self, avoid: Optional[List[Tuple[int, int]]] = None):

        super().__init__(CENTER_POS, RED)
        self.randomize_position(avoid)

    def randomize_position(
        self, avoid: Optional[List[Tuple[int, int]]] = None
    ) -> None:
        """Place the apple in a random free cell (never on the snake).
        Args:
            avoid: List of positions to avoid when placing apple
        """
        occupied = set(avoid) if avoid else set()
        free_cells = tuple(ALL_CELLS - occupied)
        if not free_cells:
            return
        self.position = random.choice(free_cells)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the apple on the given surface.
        Args:
            surface: Pygame surface to draw on
        """
        self.draw_cell(surface, self.position, self.body_color)


class Snake(GameObject):
    """Snake implemented as an ordered list of grid-aligned segments."""

    def __init__(
        self,
        start_pos: Tuple[int, int] = CENTER_POS,
        body_color: Tuple[int, int, int] = GREEN
    ):
        """Initialize Snake at starting position.
        Args:
            start_pos: Starting position as (x, y) tuple
            body_color: RGB color tuple for snake body
        """
        super().__init__(start_pos, body_color)
        self.length: int = 1
        self.positions: List[Tuple[int, int]] = [start_pos]
        self.direction: Direction = RIGHT
        self.next_direction: Optional[Direction] = None

    def get_head_position(self) -> Tuple[int, int]:
        """Return the position of the snake's head.
        Returns:
            Head position as (x, y) tuple
        """
        return self.positions[0]

    def set_next_direction(self, direction: Direction) -> None:
        """Set the next direction for the snake to move.
        Args:
            direction: Direction tuple (dx, dy)
        """
        self.next_direction = direction

    def update_direction(self) -> None:
        """Update the snake's current direction based on next_direction."""
        if self.next_direction is None:
            return
        ndx, ndy = self.next_direction
        dx, dy = self.direction
        if ndx == -dx and ndy == -dy:
            self.next_direction = None
            return
        self.direction = self.next_direction
        self.next_direction = None

    def move(self) -> None:
        """Move the snake one step in the current direction."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head_x + dx) % SCREEN_WIDTH,
            (head_y + dy) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def grow(self) -> None:
        """Increase the snake's length by one segment."""
        self.length += 1

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the snake on the given surface.
        Args:
            surface: Pygame surface to draw on
        """
        for pos in self.positions:
            self.draw_cell(surface, pos, self.body_color)

    def collides_with_self(self) -> bool:
        """Check if the snake's head collides with its body.
        Returns:
            True if collision detected, False otherwise
        """
        if len(self.positions) < 4:
            return False
        head = self.get_head_position()
        return head in self.positions[1:]

    def trim_to_head(self) -> None:
        head = self.get_head_position()
        self.positions = [head]
        self.length = 1
        self.next_direction = None

    def reset(self) -> None:
        """Reset snake to initial state at center."""
        self.length = 1
        self.positions = [CENTER_POS]
        self.direction = RIGHT
        self.next_direction = None


def load_highscore() -> int:

    if not os.path.exists(HIGHSCORE_FILE):
        return 1
    try:
        with open(HIGHSCORE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return int(data.get('highscore', 1))
    except Exception:
        return 1


def save_highscore(value: int) -> None:
    """Save highscore to file.
    Args:
        value: Highscore value to save
    """
    try:
        with open(HIGHSCORE_FILE, 'w', encoding='utf-8') as f:
            json.dump({'highscore': int(value)}, f)
    except Exception:
        pass


def handle_keys(snake: Snake) -> None:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key in KEY_TO_DIR:
                snake.set_next_direction(KEY_TO_DIR[event.key])


def main() -> None:
    highscore = load_highscore()
    pygame.display.set_caption(f'Изгиб Питона — рекорд: {highscore}')

    snake = Snake()
    apple = Apple(avoid=snake.positions)
    fps = FPS_DEFAULT

    while True:
        clock.tick(fps)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(avoid=snake.positions)
            if snake.length > highscore:
                highscore = snake.length
                save_highscore(highscore)
                pygame.display.set_caption(
                    f'Изгиб Питона — рекорд: {highscore}'
                )

        # Self-collision
        if snake.collides_with_self():
            snake.trim_to_head()
            if apple.position == snake.get_head_position():
                apple.randomize_position(avoid=snake.positions)

        # Draw
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
