"""Импортируемые библиотеки."""
from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
ALL_CELLS = ((GRID_WIDTH - 1) * (GRID_HEIGHT - 1))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [RIGHT, LEFT, UP, DOWN]

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (14, 49, 113)

# Цвет яблока
APPLE_COLOR = (49, 196, 74)

# Цвет змейки
SNAKE_COLOR = (245, 247, 43)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Родительский класс, который устанавливает параметры объекта игры.
    Атрибуты:
    body_color (tuple or None): цвет объекта,
    который переопределяется в другом классе.
    position (tuple): Позиция яблочка на экране,
    начальная позиция - центр экрана.
    """

    def __init__(self) -> None:
        self.position = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.body_color = None
        self.positions = None

    def draw(self):
        """Этот метод отвечает за иллюстрирование
        объектов на игровом поле.
        """


class Apple(GameObject):
    """Этот класс унаследован от класса GameObject.
    Он описывает параметры яблочка и действия с ним.
    """

    def __init__(self, occupied_cells=None):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.occupied_cells = occupied_cells
        self.position = self.randomize_position()

    def randomize_position(self):
        """Этот метод устанавливает случайное
        положение яблочка на игровом поле.
        """
        random_num_1 = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        random_num_2 = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (random_num_1, random_num_2)

        while self.position in self.occupied_cells:
            random_num_1 = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            random_num_2 = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return random_num_1, random_num_2

    def draw(self):
        """Этот метод отвечает за иллюстрирование
        яблочка на игровом поле.
        """
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Этот класс унаследован от класса GameObject.
    Он описывает параметры змейки и действия с ней.
    """

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Этот метод описывает изменение
        направления движения змейки.
        """
        if self.next_direction:
            self.direction = self.next_direction
        self.next_direction = None

    def move(self):
        """Данный метод описывает движение змейки на игровом поле."""
        x, y = self.get_head_position()
        self.update_direction()

        x = (x + GRID_SIZE * self.direction[0]) % SCREEN_WIDTH
        y = (y + GRID_SIZE * self.direction[1]) % SCREEN_HEIGHT

        new_position = (x, y)
        self.positions.insert(0, new_position)

        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.pop(-1)

    def increase(self):
        """Данный метод описывает увеличение длины змейки."""
        self.length += 1
        self.positions.append(self.last)

    def draw(self):
        """Этот метод отвечает за иллюстрирование
        змейки на игровом поле.
        """
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Этот метод возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Этот метод отвечает за обновление
        направления движения змейки.
        """
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice(DIRECTIONS)


def handle_keys(game_object):
    """Эта функция отвечает за обработку действий пользователя."""
    keydown_directions = {
        (LEFT, pg.K_UP): UP,
        (RIGHT, pg.K_DOWN): DOWN,
        (UP, pg.K_RIGHT): RIGHT,
        (DOWN, pg.K_LEFT): LEFT
    }
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            for key in keydown_directions:
                if event.key == key[1]:
                    game_object.next_direction = keydown_directions[key]


def main():
    """Эта функция отвечает за описание действий игры."""
    # Инициализация PyGame:
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        if apple.position == snake.get_head_position():
            snake.increase()
            apple.position = apple.randomize_position()

        head_snake = snake.get_head_position()
        body_snake = snake.positions[1:]
        if len(snake.positions) > 2 and head_snake in body_snake:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        # Тут опишите основную логику игры.
        apple.draw()
        snake.draw()
        snake.move()
        pg.display.update()


if __name__ == '__main__':
    main()
