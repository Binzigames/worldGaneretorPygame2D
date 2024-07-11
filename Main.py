import pygame
import random
import os

# Ініціалізація Pygame
pygame.init()

# Розміри вікна гри
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
BLOCK_SIZE = 20  # Розмір блоку

# Розрахунок розмірів світу на основі розмірів екрану
MAP_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
MAP_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
WIDTH, HEIGHT = MAP_WIDTH * BLOCK_SIZE, MAP_HEIGHT * BLOCK_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Factorio-like Game")

# Числові представлення блоків
EMPTY = 0
GRASS = 1
DIRT = 2
STONE = 3
WATER = 4
SAND = 5
TREE = 6

# Завантаження текстури для дерев'яних блоків
tree_texture = pygame.image.load(os.path.join('Tree.png')).convert()

# Шаблони чанків з різними комбінаціями блоків
chunk_templates = [
    [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
    ],
    [
        [5, 5, 5, 5, 5],
        [5, 4, 4, 4, 5],
        [5, 4, 4, 4, 5],
        [5, 4, 4, 4, 5],
        [5, 5, 5, 5, 5],
    ],
    [
        [1, 1, 1, 1, 1],
        [1, 1, 4, 1, 1],
        [1, 4, 4, 4, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 3, 3, 1],
        [3, 3, 1, 3, 1],
        [3, 1, 1, 1, 3],
        [1, 3, 1, 1, 3],
        [1, 1, 3, 3, 1],
    ],
    [
        [1, 1, 1, 1, 1],
        [1, 1, 6, 1, 1],
        [1, 6, 6, 6, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
    ],
]

# Клас для світу
class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[EMPTY for _ in range(width)] for _ in range(height)]

    def generate_world(self):
        chunk_size = len(chunk_templates[0])  # Розмір чанка (припустимо, що вони квадратні)
        for chunk_x in range(0, self.width, chunk_size):
            for chunk_y in range(0, self.height, chunk_size):
                template = random.choice(chunk_templates)
                for y in range(chunk_size):
                    for x in range(chunk_size):
                        if chunk_x + x < self.width and chunk_y + y < self.height:
                            self.grid[chunk_y + y][chunk_x + x] = template[y][x]

    def save_world(self, filename):
        with open(filename, 'w') as f:
            for row in self.grid:
                f.write(' '.join(map(str, row)) + '\n')

    def load_world(self, filename):
        with open(filename, 'r') as f:
            for y, line in enumerate(f):
                for x, value in enumerate(line.split()):
                    self.grid[y][x] = int(value)

    def draw(self, screen, block_size):
        for y in range(self.height):
            for x in range(self.width):
                block = self.grid[y][x]
                if block == EMPTY:
                    color = (0, 0, 0)  # Чорний колір для порожніх блоків
                elif block == GRASS:
                    color = (0, 255, 0)  # Зелений колір для трав'яних блоків
                elif block == DIRT:
                    color = (139, 69, 19)  # Коричневий колір для земляних блоків
                elif block == STONE:
                    color = (128, 128, 128)  # Сірий колір для кам'яних блоків
                elif block == WATER:
                    color = (0, 0, 255)  # Синій колір для водяних блоків
                elif block == SAND:
                    color = (255, 255, 0)  # Жовтий колір для піскових блоків
                elif block == TREE:
                    screen.blit(tree_texture, (x * block_size, y * block_size))

                pygame.draw.rect(screen, color, (x * block_size, y * block_size, block_size, block_size))


# Ініціалізація світу та генерація
world = World(MAP_WIDTH, MAP_HEIGHT)
world.generate_world()

# Головний цикл гри
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обробка подій та оновлення графіки
    WIN.fill((0, 0, 0))
    world.draw(WIN, BLOCK_SIZE)
    pygame.display.flip()

pygame.quit()
