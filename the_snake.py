from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (14, 49, 113)

# Цвет яблока
APPLE_COLOR = (49, 196, 74)

# Цвет змейки
SNAKE_COLOR = (245, 247, 43)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Тут опишите все классы игры.
class GameObject:
    """Базовый класс, который устанавливает параметры объекта игры."""
    def __init__(self) -> None:
        self.position = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        pass


class Apple(GameObject):
    """Этот класс унаследован от класса GameObject.
    Он описывает параметры яблочка и действия с ним."""
    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Этот метод устанавливает
        случайное положение яблочка на игровом поле"""
        random_num_1 = randint(0, GRID_WIDTH * GRID_SIZE)
        random_num_2 = randint(0, GRID_HEIGHT * GRID_SIZE)
        position = (random_num_1, random_num_2)
        return position

    def draw(self):
        """Этот метод отвечает за иллюстрирование
        яблочка на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Этот класс унаследован от класса GameObject.
    Он описывает параметры змейки и действия с ней."""
    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Этот метод описывает изменение
        направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


    def move(self):
        """Данный метод описывает движение змейки на игровом поле."""
        self.get_head_position()
        if self.direction == RIGHT:
            self.positions.insert(
                0, (self.positions[0][0], self.positions[0][1] + GRID_SIZE))
        elif self.direction == LEFT:
            self.positions.insert(
                0, (self.positions[0][0], self.positions[0][1] - GRID_SIZE))
        elif self.direction == UP:
            self.positions.insert(
                0, (self.positions[0][0] + GRID_SIZE, self.positions[0][1]))
        elif self.direction == DOWN:
            self.positions.insert(
                0,(self.positions[0][0] - GRID_SIZE, self.positions[0][1]))
        if self.positions[0][0] > SCREEN_WIDTH:
            self.positions[0][0] == 0
        if self.positions[0][0] < 0:
            self.positions[0][0] == SCREEN_WIDTH
        if self.positions[0][1] > SCREEN_HEIGHT:
            self.positions[0][1] == 0
        if self.positions[0][1] < 0:
            self.positions[0][1] == SCREEN_HEIGHT

        if len(self.positions) >= self.length:
            self.positions.pop(-1)


    def increase(self):
        """Данный метод описывает увеличение длины змейки."""
        if self.position in self.positions:
            self.length += 1



    def draw(self):
        """Этот метод отвечает за иллюстрирование
        змейки на игровом поле."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        """Этот метод отвечает за обновление
        направления движения змейки."""
        if self.positions[0] in self.positions[1:]:
            directions = [RIGHT, UP, DOWN, LEFT]
            self.length = 1
            self.positions = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
            self.direction = choice(directions)


def handle_keys(game_object):
    """Эта функция отвечает за обработку действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                 game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                 game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                 game_object.next_direction = RIGHT




def main():
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        if apple.position == snake.get_head_position():
            snake.increase()
            apple.position = apple.position

        head_snake = snake.get_head_position()
        body_snake = snake.positions[1:]
        if len(snake.positions) > 2 and head_snake in body_snake:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        # Тут опишите основную логику игры.
    apple.draw()
    snake.draw()
    snake.move()
    pygame.display.update()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
#def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
